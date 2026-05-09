import pytest
import json
from graph import app
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize the Judge LLM
judge_llm = ChatOllama(model="gemma4:26b", temperature=0)

# 1. Define the Golden Dataset
GOLDEN_DATASET = [
    {
        "input": "We need a HIPAA compliant payment system on AWS for under $5k.",
        "expected_themes": ["HIPAA", "AWS", "Encryption", "Budget Constraint"],
        "critical_requirement": "Customer Managed Keys (CMK)"
    },
    {
        "input": "Build a secure data lake in Azure for European users.",
        "expected_themes": ["Azure", "GDPR", "Data Residency"],
        "critical_requirement": "Data Processing Agreement"
    }
]

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from datasets import Dataset

@pytest.mark.parametrize("case", GOLDEN_DATASET)
def test_architecture_with_ragas(case):
    """Scientific evaluation using Ragas metrics."""
    
    # Run the full agentic pipeline
    inputs = {"discovery_doc": case["input"]}
    result = app.invoke(inputs)
    
    # Prepare data for Ragas
    data = {
        "question": [case["input"]],
        "contexts": [[result["rag_context"]]],
        "answer": [result["final_proposal"]],
        "ground_truth": [case["critical_requirement"]]
    }
    dataset = Dataset.from_dict(data)
    
    # Run Evaluation
    # We use our local Gemma 2 as the critic for Ragas
    results = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=judge_llm
    )
    
    print(f"\n--- Ragas Results for '{case['input'][:20]}...' ---")
    print(results)
    
    # Assertions based on Ragas scores (0.0 to 1.0)
    assert results["faithfulness"] > 0.7, "Low faithfulness - hallucination detected!"
    assert results["answer_relevancy"] > 0.7, "Low relevancy - architect missed the point!"

if __name__ == "__main__":
    print("Run this test using: pytest evals/regression/test_architecture.py")
