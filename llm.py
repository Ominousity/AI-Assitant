import os
from autogen import AssistantAgent, UserProxyAgent

config_list = [
    {
        "model": "open-mistral-nemo",
        "api_key": os.getenv("MistralAPI"),
        "api_type": "mistral",
        "max_tokens": 1000,
        "api_rate_limit": 5,
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.5,
}

assistant = AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
    system_message="You are a personal assistant, made to please your user.",
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE"),
)


def ask_llm(command: str):
    if ("hey buddy") in command.casefold():

        response = user.initiate_chat(assistant, message=command)
        for msg in response.chat_history:
            if msg.get("name") == "Assistant":
                print(msg.get("content", ""))
                return msg.get("content", "")

    else:
        return "did not ask llm"
