from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call
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
def get_current_weather(city: str) -> str:
    """Get current weather."""
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


@wrap_model_call
def logging_middleware(request, handler):
    print("\n===== LOGGING MIDDLEWARE =====")
    print("Before model call")

    for msg in request.messages:
        print(f"- Type: {msg.__class__.__name__}")
        print(f"  Content: {msg.content}")
        if hasattr(msg, "name"):
            print(f"  Tool Name: {msg.name}")

    response = handler(request)

    print("\nAfter model call")
    for msg in response.result:
        print(f"- Type: {msg.__class__.__name__}")
        print(f"  Content: {msg.content}")
        if hasattr(msg, "name"):
            print(f"  Tool Name: {msg.name}")

    print("===== END LOG =====\n")
    return response


llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)


agent = create_agent(
    model=llm,
    tools=[calculator, get_current_weather],
    middleware=[logging_middleware],
    system_prompt="Use calculator for math and weather tool for weather. Reply briefly."
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

    print("===== FINAL ANSWER =====")
    if tool_output:
        print("AI:", tool_output)
    else:
        print("AI:", messages[-1].content)
