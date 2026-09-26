from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv

import os
import requests


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = init_chat_model(
   "openai/gpt-oss-20b",
    model_provider="groq",
    api_key=GEMINI_API_KEY
)
api_key=os.getenv("api_key")
@tool
def get_weather(location : str)->str:
    """Get the current weather for a location."""
    url=f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
    response=requests.get(url)
    data=response.json()

    city = data["name"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    return (
        f"Location: {city}\n"
        f"Temperature: {temperature}°C\n"
        f"Feels like: {feels_like}°C\n"
        f"Condition: {weather}\n"
        f"Humidity: {humidity}%\n"
        f"Wind speed: {wind_speed} m/s"
    )

@tool
def get_quote()->str:
    """Get a random inspirational quote."""
    url = "https://dummyjson.com/quotes/random"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return f"{data['quote']} — {data['author']}"


user_content = HumanMessage(
    content="Give me random quote."
)

model_bind = model.bind_tools([get_quote,get_weather])

response = model_bind.invoke([user_content])
print(response)
print(response.tool_calls)


tool_messages = []
tools = {
    "get_weather": get_weather,
    "get_quote": get_quote
}
for tool_call in response.tool_calls:
    select_tool=tools[tool_call["name"]]

    result=select_tool.invoke(tool_call["args"])
    tool_messages.append(
        ToolMessage(
             content=str(result),
            tool_call_id=tool_call["id"]
        )
    )

final_response = model.invoke(
    [
        user_content,
        response,
        *tool_messages
    ]
)
print(final_response.content)