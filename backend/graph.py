from typing import Annotated, TypedDict, List, Union
import operator
import json
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize the Local LLM
llm = ChatOllama(model="gemma4:26b", temperature=0)

import time
from functools import wraps

# Resilience Decorator for Error Recovery
def resilient_node(func):
    @wraps(func)
    def wrapper(state: AgentState, *args, **kwargs):
        max_retries = 2
        for attempt in range(max_retries):
            try:
                return func(state, *args, **kwargs)
            except Exception as e:
                print(f"⚠️ Error in {func.__name__} (Attempt {attempt+1}): {str(e)}")
                if attempt == max_retries - 1:
                    # Final Fallback State
                    print(f"🛑 {func.__name__} failed after {max_retries} attempts. Pivoting to fallback.")
                    return {"steps": [f"{func.__name__}_fallback"]}
                time.sleep(1) # Backoff
        return func(state, *args, **kwargs)
    return wrapper

# 1. Define the State
# In LangGraph, the 'State' is a shared object that all nodes can read and write to.
# This replaces the 'one-shot' prompt with a structured memory.
class AgentState(TypedDict):
    discovery_doc: str  # Original client input
    constraints: List[str]  # Extracted by the Analyst
    rag_context: List[str]  # Retrieved from the Vector DB
    tool_data: dict  # Results from MCP tool calls
    final_proposal: str  # The final delivery artifact
    steps: Annotated[List[str], operator.add]  # Tracking the reasoning chain

# 2. Define Node Functions

from gateway.guardrails import pii_masking_gateway, validate_input_integrity, sanitize_output

@resilient_node
def analyst_node(state: AgentState):
    """Extracts technical constraints with a PII-Masking Gateway."""
    print("\n[Node: Analyst] Analyzing discovery notes (PII Gateway Active)...")
    
    # 1. Validate Integrity
    if not validate_input_integrity(state['discovery_doc']):
        return {"steps": ["analyst_failed"], "constraints": ["ERROR: Invalid or Malicious Input Detected"]}
    
    # 2. Mask PII
    masked_notes, _ = pii_masking_gateway(state['discovery_doc'])
    
    prompt = f"""
    You are a Senior Solutions Architect. Extract all technical, business, and compliance constraints from the following notes.
    Return the result as a JSON list of strings.
    
    Notes:
    {masked_notes}
    
    JSON Output:
    """
    
    response = llm.invoke([
        SystemMessage(content="You extract technical constraints into JSON list format. No conversational filler."),
        HumanMessage(content=prompt)
    ])
    
    try:
        # Simple cleanup in case the LLM adds markdown backticks
        content = response.content.strip().replace("```json", "").replace("```", "")
        extracted_constraints = json.loads(content)
    except:
        extracted_constraints = [response.content]

    return {
        "constraints": extracted_constraints,
        "steps": ["analyst"]
    }

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

@resilient_node
def rag_node(state: AgentState):
    """Semantic RAG: Performs vector search on ChromaDB."""
    print(f"[Node: RAG] Performing semantic search for constraints...")
    
    # Initialize Embeddings and Vector Store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_db = Chroma(persist_directory="backend/chroma_db", embedding_function=embeddings)
    
    # Use the extracted constraints as query terms
    query = " ".join(state['constraints'])
    docs = vector_db.similarity_search(query, k=2)
    
    retrieved_context = [f"Source: {doc.metadata.get('source')}\n{doc.page_content}" for doc in docs]

    return {
        "rag_context": retrieved_context if retrieved_context else ["No specific reference architecture found."],
        "steps": ["rag"]
    }

from tools.mcp.governance_server import check_data_governance_rules

@resilient_node
def tooling_node(state: AgentState):
    """MCP Tooling: Dynamically checks governance based on extracted constraints."""
    print("[Node: MCP Tooling] Calling Governance Server...")
    
    # Identify region and standard from constraints
    # (In a production app, we'd use the LLM to extract these parameters)
    region = "us-east-1"  # Default for demo
    compliance_standard = "SOC2" # Default
    
    for c in state['constraints']:
        if "HIPAA" in c.upper():
            compliance_standard = "HIPAA"
        if "Azure" in c:
            region = "east-us" # Simulating mapping
            
    # Simulate MCP Call
    governance_results = check_data_governance_rules(region, compliance_standard)
    
    print(f"--- Governance Check for {compliance_standard} in {region}: {governance_results['status']} ---")
    
    return {
        "tool_data": {
            "compliance_report": governance_results,
            "region_checked": region,
            "standard_checked": compliance_standard
        },
        "steps": ["tooling"]
    }

@resilient_node
def human_review_node(state: AgentState):
    """
    HITL (Human-in-the-Loop) Node.
    Strategic Rationale: For high-stakes architectural consulting, an AI 
    should never be 100% autonomous. This node allows a consultant to 
    review the agent's reasoning before the final proposal is drafted.
    """
    print("\n[Node: Human Review] ⚠️ High-risk compliance detected. Awaiting consultant oversight...")
    return {"steps": ["human_review"]}

def architect_node(state: AgentState):
    print("[Node: Architect] Drafting final structured proposal...")
    
    # Check if we passed human review for high-risk cases
    review_status = "Approved by Consultant" if "human_review" in state["steps"] else "Standard Automated Path"
    
    prompt = f"""
    Synthesize a Technical Solution Proposal.
    STATUS: {review_status}
    
    - Constraints: {state['constraints']}
    - Reference Context: {state['rag_context']}
    - Live Tool Data: {state['tool_data']}
    
    Address any 'Warning' or 'Manual Review' flags from the tool data explicitly.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Final Output Sanitization
    final_proposal = sanitize_output(response.content)
    
    return {
        "final_proposal": final_proposal,
        "steps": ["architect"]
    }

# 3. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("analyst", analyst_node)
workflow.add_node("rag", rag_node)
workflow.add_node("tooling", tooling_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("architect", architect_node)

workflow.set_entry_point("analyst")
workflow.add_edge("analyst", "rag")
workflow.add_edge("rag", "tooling")

# Conditional Logic: If Tooling finds a 'Warning' or 'Manual Review', go to Human Review
def route_after_tooling(state: AgentState):
    report = state["tool_data"].get("compliance_report", {})
    if report.get("status") in ["Warning", "Manual Review Required"]:
        return "human_review"
    return "architect"

workflow.add_conditional_edges(
    "tooling",
    route_after_tooling,
    {
        "human_review": "human_review",
        "architect": "architect"
    }
)

workflow.add_edge("human_review", "architect")
workflow.add_edge("architect", END)

# Compile with a checkpointer to enable state persistence and HITL
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])

if __name__ == "__main__":
    # Simulate a messy consulting discovery document
    messy_notes = """
    Met with the CTO today. They need to move the payment processor to the cloud. 
    Must be HIPAA compliant because of the patient data. 
    They prefer AWS but the dev team knows Azure. 
    Budget is tight - need to stay under $10k per month for the pilot.
    Uptime is critical: 99.9%.
    """
    
    inputs = {"discovery_doc": messy_notes}
    print("Starting Solution Architecture Workflow...")
    
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"\n--- Node: {key} Completed ---")
            if key == "architect":
                print(value["final_proposal"])
