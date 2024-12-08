import os
from autogen import AssistantAgent, UserProxyAgent
from tools import weather_api


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

assistant.register_for_llm(description="a simple api for getting weather data")(weather_api)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    is_termination_msg=lambda x: x.get("content", "").strip().endswith("TERMINATE"),
)


def ask_llm(command: str):
    if "hey buddy" in command.casefold():
        # Initiate the chat
        user.initiate_chat(assistant, message=command)

        # Keep the chat open for continuous conversation
        while True:
            # Get the latest message from the user
            user_message = yield  # Wait for the next user message from the main script
            if user_message.strip().lower() == "exit":
                break

            # Send the user message to the assistant and get the response
            response = user.send(recipient=assistant, message=user_message)
            for msg in response:
                if msg.get("name") == "Assistant":
                    return msg.get("content", "")
