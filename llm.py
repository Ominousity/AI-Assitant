import os
from autogen import ConversableAgent, UserProxyAgent, register_function
from tools import weather_api

config_list = [
    {
        "model": "open-mistral-nemo",
        "api_key": os.getenv("MistralAPI"),
        "api_type": "mistral",
        "max_tokens": 1000,
        "api_rate_limit": 0.5,
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.1,
}

assistant = ConversableAgent(
    name="Assistant",
    llm_config=llm_config,
    system_message="You are a personal assistant, made to please your user.",
)

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0
)

tool_functions = {
    "weather_api": weather_api,
}

for tool_name, tool_function in tool_functions.items():
    register_function(
        tool_function,
        caller=assistant,
        executor=user,
        name=tool_name,
        description=f"Execute the {tool_name} function.",
    )


def ask_llm(user_message: str) -> str:
    assistant_response = user.initiate_chat(
        recipient=assistant,
        message={"content": user_message, "role": "user"}
    )
    assistant_response_latest = assistant_response.chat_history.pop()

    for tool_name in tool_functions.keys():
        if not assistant_response_latest.get('tool_calls'):
            break

        if tool_name in assistant_response_latest['tool_calls'][0]['function']['name']:
            tool_call_id = assistant_response_latest['tool_calls'][0]['id']
            
            tool_response = user.execute_function(
                func_call={"name": tool_name, "tool_call_id": tool_call_id},
            )
            
            user.send(recipient=assistant, message={"content": tool_response[1]["content"], "role": "tool", "tool_call_id": tool_call_id})

            assistant_reply = list(user.chat_messages.values())[0][-1]
            return assistant_reply['content']
        
    return assistant_response_latest['content']

