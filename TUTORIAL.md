# Master Class: Building an Agentic Solutions Architect

Welcome to the **Consulting Delivery Copilot** tutorial. This guide will walk you through the four key pillars of modern AI Engineering: Orchestration, Memory, Tools, and Evaluation.

---

## 🏗️ Phase 1: Stateful Orchestration (LangGraph)
*Goal: Move beyond single-prompt LLMs to a robust state machine.*

In `backend/graph.py`, we define our "Solutions Architect" as a **StateGraph**.
- **The Concept**: Instead of one long prompt, we break the task into nodes (**Analyst -> RAG -> Tooling -> Architect**).
- **The State**: We use a `TypedDict` to pass data (constraints, context, tool outputs) between nodes.
- **Key Implementation**: Look for the `resilient_node` decorator. This handles error recovery—a critical production feature.

## 🧠 Phase 2: Semantic Memory (ChromaDB & RAG)
*Goal: Ground the model in "Ground Truth" to prevent hallucinations.*

Check `backend/ingest.py` and the `rag_node` in `graph.py`.
- **Ingestion**: We don't just search text; we use **Embeddings** (`nomic-embed-text`) to find the *meaning* of the client's needs.
- **Retrieval**: The `rag_node` performs a similarity search in **ChromaDB** to find relevant reference architectures.

## 🛠️ Phase 3: Real-World Connectivity (MCP Tools)
*Goal: Allow the agent to interact with external systems.*

We use the **Model Context Protocol (MCP)** pattern in `backend/tools/mcp/`.
- **Governance Tool**: The agent calls `check_data_governance_rules` to verify if a proposed region (like `us-east-1`) has specific compliance requirements (like HIPAA).
- **Codebase Tool**: The `search_internal_codebase` tool allows the agent to "read" existing code to find architectural patterns.

## 🧪 Phase 4: Scientific Evaluation (Ragas)
*Goal: Prove the system works with mathematical certainty.*

Look at `backend/evals/regression/test_architecture.py`.
- **The Problem**: How do you know the agent isn't lying?
- **The Solution**: We use **Ragas** metrics. We calculate **Faithfulness** (alignment with the knowledge base) and **Answer Relevancy** (alignment with client needs).
- **Guardrails**: We use a large 27B model (Gemma 2) as a "Judge" to score a smaller "Student" model.

---

## 🚀 How to Follow Along
1.  **Study the Ingestion**: Run `python ingest.py` and see how data is chunked.
2.  **Inspect the Logic**: Open `graph.py` and follow the `workflow.add_edge` paths.
3.  **Run the Tests**: Execute `pytest` to see the Ragas scores in action.
4.  **Explore the UI**: Use the Vite frontend to watch the "Reasoning Chain" light up.

*This system is built for transparency. Every decision is logged, and every output is verified.*
