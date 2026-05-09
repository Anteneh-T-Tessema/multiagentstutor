# System Architecture & Technical Deep-Dive

This document provides a visual and technical breakdown of the **Consulting Delivery Copilot**. Our architecture is designed for **high-trust consulting**, prioritizing security, transparency, and scientific evaluation.

---

## 1. System Orchestration (The Brain)

![Orchestration Concept](/Users/antenehtessema/.gemini/antigravity/brain/38d654b0-fc3d-4c07-b4b7-1fde1a992123/system_orchestration_concept_1778366382400.png)

The system is powered by **LangGraph**, a stateful orchestration framework that moves beyond simple prompts to a deterministic state machine.

```mermaid
graph TD
    A[Client Discovery Notes] --> B{PII Gateway}
    B -->|Masked| C[Analyst Node]
    C -->|Constraints| D[RAG Node]
    D -->|Context| E[Tooling Node]
    E -->|Compliance Check| F{Risk Detected?}
    F -->|Yes| G[Human Review]
    F -->|No| H[Architect Node]
    G --> H
    H --> I[Final Proposal]
```

---

## 2. The RAG Pipeline (Semantic Memory)

![RAG Pipeline Concept](/Users/antenehtessema/.gemini/antigravity/brain/38d654b0-fc3d-4c07-b4b7-1fde1a992123/rag_pipeline_concept_1778366394061.png)

We use a **ChromaDB** vector store to ground the agent in "Ground Truth" data, preventing hallucinations.

```mermaid
sequenceDiagram
    participant User
    participant Ingest
    participant ChromaDB
    participant Agent
    User->>Ingest: Upload .md Standards
    Ingest->>Ingest: Recursive Chunking
    Ingest->>ChromaDB: Store Embeddings
    Agent->>ChromaDB: Semantic Search (Query)
    ChromaDB-->>Agent: Top K Relevant Context
```

---

## 3. MCP Tool Integration (Live Connectivity)

![MCP Tooling Concept](/Users/antenehtessema/.gemini/antigravity/brain/38d654b0-fc3d-4c07-b4b7-1fde1a992123/mcp_tooling_concept_1778366406640.png)

The **Model Context Protocol (MCP)** allows our agent to safely interact with external governance rules and local codebases.

```mermaid
graph LR
    Agent[Agent Node] --- MCP[MCP Protocol]
    MCP --> Gov[Governance Server]
    MCP --> Code[Codebase Search]
    Gov -->|Flag| Agent
    Code -->|Snippet| Agent
```

---

## 4. Security & Evaluation (The Safety Kernel)

![Evaluation Rigor Concept](/Users/antenehtessema/.gemini/antigravity/brain/38d654b0-fc3d-4c07-b4b7-1fde1a992123/evaluation_rigor_concept_1778366418384.png)

We don't just "hope" the system works; we measure it using **Ragas** and protect it with **Guardrails**.

```mermaid
graph TD
    Input[User Input] --> Guard[PII Guardrail]
    Guard --> Workflow[Agent Workflow]
    Workflow --> Output[Draft Proposal]
    Output --> Judge[Gemma 2 Critic]
    Judge --> Score[Ragas Score: Faithfulness/Relevancy]
    Score -->|Pass| Client[Client Delivery]
    Score -->|Fail| Refine[Auto-Refinement]
```

---

## 5. Detailed Interaction (Sequence Diagram)

This diagram tracks the lifecycle of a single request as it traverses the full-stack ecosystem.

```mermaid
sequenceDiagram
    participant UI as Vite Frontend
    participant API as FastAPI Backend
    participant Guard as Security Gateway
    participant Graph as LangGraph Orchestrator
    participant MCP as MCP Server
    participant DB as ChromaDB

    UI->>API: POST /generate-proposal (Raw Notes)
    API->>Guard: validate_input_integrity()
    Guard-->>API: Validated
    API->>Graph: app.invoke(state)
    
    Graph->>Guard: pii_masking_gateway()
    Graph->>DB: similarity_search()
    DB-->>Graph: Reference Docs
    
    Graph->>MCP: check_data_governance()
    MCP-->>Graph: Compliance Report
    
    Note over Graph: IF Risk Detected -> INTERRUPT for HITL
    
    Graph->>API: Final Proposal State
    API-->>UI: JSON Response (Proposal + Transparency Log)
```

---

## 6. Data Structure (Class Diagram)

The system's core is defined by the `AgentState` and the modular node functions. This diagram visualizes the "Contract" between different parts of the system.

```mermaid
classDiagram
    class AgentState {
        +string discovery_doc
        +List~string~ constraints
        +List~string~ rag_context
        +dict tool_data
        +string final_proposal
        +List~string~ steps
    }

    class SecurityGateway {
        +pii_masking_gateway(text)
        +validate_input_integrity(text)
        +sanitize_output(text)
    }

    class NodeFunctions {
        +analyst_node(state)
        +rag_node(state)
        +tooling_node(state)
        +architect_node(state)
        +human_review_node(state)
    }

    class ResilienceLayer {
        +resilient_node(func)
    }

    NodeFunctions --> AgentState : Reads/Writes
    ResilienceLayer ..> NodeFunctions : Decorates
    SecurityGateway --> NodeFunctions : Protects
```

---

## 7. Workflow Lifecycle (State Diagram)

This diagram focuses on the LangGraph transitions and the critical "Human-in-the-Loop" decision point.

```mermaid
stateDiagram-v2
    [*] --> Analyst
    Analyst --> RAG
    RAG --> Tooling
    
    state Tooling_Decision <<choice>>
    Tooling --> Tooling_Decision
    
    Tooling_Decision --> HumanReview : If Warning/Manual Review
    Tooling_Decision --> Architect : If Status Passed
    
    HumanReview --> Architect : Consultant Approved
    Architect --> [*]
    
    state Analyst {
        [*] --> ValidateInput
        ValidateInput --> MaskPII
        MaskPII --> ExtractConstraints
    }
```

---

## 8. Multi-Orchestration Parity

The system is designed with a **Pluggable Engine Architecture**, allowing you to choose the orchestration framework that best fits the client's problem.

| Framework | Paradigm | Best For... |
| :--- | :--- | :--- |
| **LangGraph** | Stateful / Cyclical | High-trust, deterministic enterprise workflows with strict safety kernel. |
| **CrewAI** | Role-Based / Sequential | Collaborative, persona-driven tasks requiring high creativity (e.g., Marketing + Architecture). |
| **AutoGen** | Conversational / P2P | Interactive discovery sessions where the agent must negotiate with a human or another agent. |

### A. CrewAI: Role-Based Workflow
In `backend/engines/crew_engine.py`, we define a **Senior Analyst** and a **Principal Architect** who work as a team.

```mermaid
graph LR
    A[Analyst Agent] -->|JSON Report| B[Architect Agent]
    B -->|Draft| C[Quality Review Task]
    C -->|Deliverable| D[Technical Proposal]
```

### B. AutoGen: Conversational Discovery
In `backend/engines/autogen_engine.py`, the agent and the client "negotiate" the architecture through a peer-to-peer chat.

```mermaid
sequenceDiagram
    participant Client as User Proxy
    participant AI as Architect Agent
    Client->>AI: Here are my messy notes.
    AI->>Client: I noticed a gap in the DB requirements. Clarify?
    Client->>AI: Oh, we need PostgreSQL.
    AI->>Client: Perfect. Here is the final AWS design.
```

---
*Generated by the Consulting Delivery Copilot Architectural Suite.*
