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
    """
    Solve arithmetic expressions using +, -, *, /, and parentheses.
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Cannot solve expression"


@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a given city.
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: API key not found"

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            return "Error: City not found"

        result = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }

        return json.dumps(result)

    except Exception as e:
        return f"Error: {str(e)}"



llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)


agent = create_agent(
    model=llm,
    tools=[calculator, get_weather],
    system_prompt=(
        "You are a helpful assistant. "
        "If a calculation is required, use the calculator tool. "
        "If weather is asked, use the weather tool. "
        "Reply briefly."
    )
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

    tool_answer = None
    for msg in messages:
        if msg.__class__.__name__ == "ToolMessage":
            tool_answer = msg.content

    if tool_answer:
        print("AI:", tool_answer)
    else:
        print("AI:", messages[-1].content)
