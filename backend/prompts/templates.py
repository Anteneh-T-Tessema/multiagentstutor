from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Analyst Prompt (Few-Shot & Structured Extraction)
ANALYST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Technical Consultant. Your task is to extract clear, actionable constraints from messy discovery notes.
    
    ### Guidelines:
    - Identify Infrastructure needs (Cloud, On-prem).
    - Identify Compliance needs (HIPAA, SOC2, GDPR).
    - Identify Budgetary limits.
    - If a requirement is ambiguous, mark it as 'Clarification Needed'.
    
    ### Example:
    Input: 'Startup needs a basic web app. HIPAA is a concern. $2k budget.'
    Output: {{'infra': 'Web App', 'compliance': 'HIPAA', 'budget': '$2k', 'risk': 'Low'}}
    """),
    MessagesPlaceholder(variable_name="history"),
    ("user", "Notes: {discovery_doc}")
])

# 2. Architect Prompt (Chain-of-Thought & Context Grounding)
ARCHITECT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Principal Solutions Architect. Synthesize a professional Technical Solution Proposal.
    
    ### Reasoning Chain:
    1. ANALYZE the extracted constraints.
    2. REFERENCE the provided Knowledge Base context.
    3. JUSTIFY every architectural choice.
    4. REVIEW for security gaps.
    
    ### Formatting:
    Use professional Markdown with H1, H2, and Bullet points.
    """),
    ("user", """
    ### Extracted Constraints:
    {constraints}
    
    ### Knowledge Base Context:
    {rag_context}
    
    ### Conversation Memory:
    {memory}
    
    PROPOSE SOLUTION:
    """)
])
