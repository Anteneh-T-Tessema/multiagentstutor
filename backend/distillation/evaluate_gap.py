import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from difflib import SequenceMatcher

# Models
teacher_llm = ChatOllama(model="gemma4:26b", temperature=0)
student_llm = ChatOllama(model="llama3.2:3b", temperature=0)

def calculate_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def evaluate_gap():
    test_notes = """
    Met with client. Need a secure way to store patient records. 
    Must be HIPAA compliant. Use Azure if possible. 
    Budget is $2000/month.
    """
    
    print("👩‍🏫 Teacher (27B) generating proposal...")
    teacher_resp = teacher_llm.invoke([HumanMessage(content=test_notes)]).content
    
    print("👶 Student (3B) generating proposal...")
    student_resp = student_llm.invoke([HumanMessage(content=test_notes)]).content
    
    similarity = calculate_similarity(teacher_resp, student_resp)
    
    print("\n--- Distillation Gap Analysis ---")
    print(f"Content Similarity: {similarity:.2%}")
    print(f"Teacher Length: {len(teacher_resp)} chars")
    print(f"Student Length: {len(student_resp)} chars")
    
    if similarity < 0.6:
        print("🚩 SIGNIFICANT GAP: Student lacks the professional detail of the Teacher. Fine-tuning recommended.")
    else:
        print("✅ LOW GAP: Student is performing well on this task.")

if __name__ == "__main__":
    evaluate_gap()
