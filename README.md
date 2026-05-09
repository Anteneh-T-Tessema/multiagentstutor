# Consulting Delivery Copilot: Agentic Solution Architecture Assistant

## 🎯 Overview
This project is an **Agentic AI System** designed to automate the initial phase of a technology consulting engagement. It transforms messy, raw client discovery notes into a structured, compliant, and reference-backed Technical Solution Proposal.

Built as a Solutions Architecture showcase, it demonstrates production-grade rigor using **LangGraph**, **Gemma 2 27B**, and the **Model Context Protocol (MCP)**.

## 🏗️ System Architecture
The system follows a state-machine orchestration pattern (LangGraph) with four specialized nodes:

1.  **The Analyst Node**: Uses `gemma4:26b` to parse unstructured notes into a JSON schema of technical, business, and compliance constraints.
2.  **The RAG Node**: Performs context-aware retrieval from an internal knowledge base of reference architectures and HIPAA/SOC2 case studies.
3.  **The Tooling Node (MCP)**: Connects to a Governance Server to check live cloud service constraints based on the extracted requirements.
4.  **The Architect Node**: Synthesizes all inputs into a professional delivery artifact.

## 🛠️ Tech Stack
- **Orchestration**: LangGraph (Stateful Multi-Agent Workflows)
- **Model**: `gemma4:26b` (via Ollama)
- **Backend**: FastAPI (Python)
- **Frontend**: Vite + React + TypeScript
- **Evaluation**: Pytest with LLM-as-a-judge (Regression Testing)

## ⚖️ Lessons Learned & Trade-offs
### 1. Deterministic vs. Probabilistic
While Llama/Gemma are powerful, their extraction of constraints can vary. I implemented a **JSON Schema Guard** in the Analyst node to ensure the RAG and Tooling nodes always receive predictable data structures.
### 2. Local vs. API-based LLMs
I chose **Gemma 2 27B** running locally to simulate high-trust consulting environments where data residency and PII protection (HIPAA) are non-negotiable.
### 3. The "Evaluation First" Mindset
Consulting requires high accuracy. I built the **Regression Suite** before the UI to ensure that every architectural proposal meets the "Golden Standard" for compliance.

## 🚀 Getting Started
(See individual READMEs in `/backend` and `/frontend` for installation steps.)
