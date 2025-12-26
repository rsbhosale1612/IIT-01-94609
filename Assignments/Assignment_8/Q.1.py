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

@tool
def read_file(filepath: str) -> str:
    """
    Read and return the contents of a text file.
    """
    try:
        if not os.path.exists(filepath):
            return "Error: File not found"
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Error: Cannot read file"

@tool
def knowledge_lookup(topic: str) -> str:
    """
    Return basic knowledge about a topic.
    """
    knowledge_base = {
        "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
        "machine learning": "Machine learning is a subset of AI that learns from data.",
        "python": "Python is a high-level programming language.",
        "langchain": "LangChain is a framework for building LLM-powered applications."
    }
    return knowledge_base.get(topic.lower(), "Knowledge not found")

llm = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file, knowledge_lookup],
    system_prompt=(
        "You are a helpful assistant. "
        "Use calculator for math, weather tool for weather queries, "
        "file reader for reading files, and knowledge lookup for definitions. "
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
