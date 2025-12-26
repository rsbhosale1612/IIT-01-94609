from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """Solve arithmetic expressions."""
    try:
        return str(eval(expression))
    except:
        return "Error"

@tool
def read_file(filepath: str) -> str:
    """Read and return file content."""
    try:
        if not os.path.exists(filepath):
            return "Error"
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Error"

@tool
def get_current_weather(city: str) -> str:
    """Get current weather for a city."""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("cod") != 200:
            return "Error"
        return json.dumps({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        })
    except:
        return "Error"

llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator, read_file, get_current_weather],
    system_prompt="Use tools when required. Reply briefly."
)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    messages = result["messages"]

    tool_output = None
    for msg in messages:
        if msg.__class__.__name__ == "ToolMessage":
            tool_output = msg.content

    if tool_output:
        print("AI:", tool_output)
    else:
        print("AI:", messages[-1].content)


