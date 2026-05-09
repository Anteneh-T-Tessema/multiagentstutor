from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama

# 1. Initialize the Local LLM for the Crew
llm = ChatOllama(model="gemma4:26b")

def run_crew_delivery(notes: str):
    print("🚢 Launching the Consulting Crew...")

    # 2. Define Agents with Personas
    analyst = Agent(
        role='Senior Business Analyst',
        goal='Extract clean technical constraints and business needs from messy notes',
        backstory='You are an expert at identifying requirements that others miss.',
        llm=llm,
        allow_delegation=False
    )

    architect = Agent(
        role='Principal Solutions Architect',
        goal='Design a secure, scalable architecture based on extracted constraints',
        backstory='You specialize in AWS and Azure reference architectures.',
        llm=llm,
        allow_delegation=True
    )

    # 3. Define Tasks
    task1 = Task(
        description=f"Analyze these notes and list all technical constraints: {notes}",
        agent=analyst,
        expected_output="A structured JSON list of constraints."
    )

    task2 = Task(
        description="Based on the analyst's report, draft a 3-page Solutions Proposal.",
        agent=architect,
        expected_output="A comprehensive markdown Technical Solution Proposal."
    )

    # 4. Assemble the Crew
    crew = Crew(
        agents=[analyst, architect],
        tasks=[task1, task2],
        process=Process.sequential # Sequential delivery
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
    test_notes = "Met with client. Need HIPAA compliant Azure setup. Budget $5k."
    print(run_crew_delivery(test_notes))
