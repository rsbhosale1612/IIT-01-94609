from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Solve arithmetic expressions with numbers only."""
    try:
        return str(eval(expression))
    except:
        return "Error"


llm = init_chat_model(
    model="llama-3.1-8b-instant",   # ⚡ much faster than Gemma
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt=(
        "You are a calculator assistant. "
        "If the input is a math expression, call the calculator tool. "
        "Otherwise, reply briefly."
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

    ai_msg = result["messages"][-1]
    print("AI:", ai_msg.content)
