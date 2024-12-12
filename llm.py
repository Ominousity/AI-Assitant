import os
from autogen import ConversableAgent, UserProxyAgent, register_function
from tools import get_weather_data, add_to_todoList, get_todoList, clear_todoList
from dotenv import load_dotenv

load_dotenv(".env")

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
    max_consecutive_auto_reply=0,
    code_execution_config={"use_docker": False},
)

tool_functions = [
    {"function": get_weather_data, "name": "get_weather_data", "description": "Get weather data for a city. the days argument can max be 7. Translate to english if needed."},
    {"function": add_to_todoList, "name": "add_to_todoList", "description": "Add an item to the todo list."},
    {"function": get_todoList, "name": "get_todoList", "description": "Get the todo list."},
    {"function": clear_todoList, "name": "clear_todoList", "description": "Clear the todo list."}
]

for tool in tool_functions:
    register_function(
        tool["function"],
        caller=assistant,
        executor=user,
        name=tool["name"],
        description=tool["description"],
    )


def ask_llm(user_message: str) -> str:
    assistant_response = user.initiate_chat(
        recipient=assistant,
        message={"content": user_message, "role": "user"}
    )
    assistant_response_latest = assistant_response.chat_history.pop()

    for tool in tool_functions:
        if not assistant_response_latest.get('tool_calls'):
            break

        if tool["name"] in assistant_response_latest['tool_calls'][0]['function']['name']:
            tool_call_id = assistant_response_latest['tool_calls'][0]['id']
            tool_call_arguments = assistant_response_latest['tool_calls'][0]['function']['arguments']
            
            tool_response = user.execute_function(
                func_call={"name": tool["name"], "tool_call_id": tool_call_id, "arguments": tool_call_arguments},
            )
            
            user.send(recipient=assistant, message={"content": tool_response[1]["content"], "role": "tool", "tool_call_id": tool_call_id})

            assistant_reply = list(user.chat_messages.values())[0][-1]
            return assistant_reply['content']
        
    return assistant_response_latest['content']

