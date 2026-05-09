import autogen

# 1. Configuration for Local LLM (Ollama)
config_list = [
    {
        "model": "gemma4:26b",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama", # Placeholder for local use
    }
]

def run_autogen_discovery(notes: str):
    print("🤖 Starting AutoGen Peer-to-Peer Discovery...")

    # 2. Define the Agents
    assistant = autogen.AssistantAgent(
        name="Architect_Agent",
        llm_config={"config_list": config_list},
        system_message="You are a Solutions Architect. Your goal is to refine discovery notes and propose a solution."
    )

    user_proxy = autogen.UserProxyAgent(
        name="Client_Proxy",
        human_input_mode="NEVER", # Fully autonomous for this demo
        max_consecutive_auto_reply=2,
        code_execution_config={"work_dir": "scratch", "use_docker": False}
    )

    # 3. Start the Conversation
    user_proxy.initiate_chat(
        assistant,
        message=f"I have these discovery notes: {notes}. Can you help me architect a solution?"
    )
    
    return user_proxy.last_message()["content"]

if __name__ == "__main__":
    test_notes = "Need a secure payment gateway on AWS."
    print(run_autogen_discovery(test_notes))
