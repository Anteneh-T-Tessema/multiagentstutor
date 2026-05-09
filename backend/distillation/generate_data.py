import json
import random
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize the Teacher Model (High Reasoning)
teacher_llm = ChatOllama(model="gemma4:26b", temperature=0.7)

# Seed Scenarios to expand upon
SEEDS = [
    "HIPAA compliant payment gateway on AWS",
    "GDPR compliant data lake on Azure",
    "High-availability fintech API in us-east-1",
    "Secure inventory management for a retail chain"
]

def generate_synthetic_data(count=5):
    print(f"🧠 Distilling knowledge from Teacher model (generating {count} samples)...")
    dataset = []
    
    for i in range(count):
        seed = random.choice(SEEDS)
        print(f"Generating sample {i+1} based on: {seed}")
        
        # 1. Generate a complex, messy discovery note
        prompt_notes = f"Generate a messy, unstructured 200-word markdown file of client discovery notes for this scenario: {seed}. Include budget constraints and a specific compliance need."
        notes_resp = teacher_llm.invoke([HumanMessage(content=prompt_notes)])
        
        # 2. Generate the "Expert" architectural proposal
        prompt_proposal = f"Now, acting as a Principal Solutions Architect at a premier consulting firm, write the perfect, structured architectural proposal for those notes. Use best practices and assume a multi-region cloud setup."
        proposal_resp = teacher_llm.invoke([HumanMessage(content=prompt_proposal)])
        
        dataset.append({
            "instruction": notes_resp.content,
            "output": proposal_resp.content,
            "metadata": {"seed": seed, "distilled_from": "gemma4:26b"}
        })

    # Save for Fine-tuning
    with open("training_data_distilled.jsonl", "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")
            
    print(f"✅ Distillation complete. Saved {len(dataset)} samples to training_data_distilled.jsonl")

if __name__ == "__main__":
    generate_synthetic_data()
