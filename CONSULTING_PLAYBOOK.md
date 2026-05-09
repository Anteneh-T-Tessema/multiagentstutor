# Consulting Delivery Copilot: Engineering Playbook

## 📖 Introduction
This playbook is for the engineering team to understand, maintain, and extend the Agentic Solution Architecture Assistant.

## 🛠️ Extending the Governance MCP Server
The system's compliance intelligence lives in `backend/tools/mcp/governance_server.py`. 
To add new rules:
1.  Open `governance_server.py`.
2.  Add a new key to the `rules` dictionary (e.g., `Azure` or `GDPR`).
3.  Define the `status`, `reason`, and `action_required`.
4.  **Note**: The Architect agent is instructed to prioritize these rules over its internal knowledge.

## 🧪 Scaling the Evaluation Suite
The system uses **Ragas** for scientific evaluation. If you find the agent is hallucinating on new cloud services:
1.  Add a new test case to `backend/evals/regression/test_architecture.py`.
2.  Update the `critical_requirement` in the Golden Dataset.
3.  Run `pytest` to see the new **Faithfulness** scores.

## 🧱 The Safety Kernel (HITL)
If the system is pausing too frequently for Human Review, you can adjust the threshold in `backend/graph.py` within the `route_after_tooling` function. Currently, any 'Warning' triggers an interrupt.

## ⚠️ Known Gotchas
- **Ollama Latency**: If running on hardware without a dedicated GPU, the 27B model may take up to 60 seconds per node. For faster development, swap to `llama3.2` (3B).
- **ChromaDB Persistence**: Ensure `backend/ingest.py` is run whenever new `.md` files are added to the `knowledge/` directory.

---
*Built with the "Servant Leadership" mentality in mind.*
