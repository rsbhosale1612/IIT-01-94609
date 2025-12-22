from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

llm = init_chat_model(
    model = "llama-3.1-8b-instant",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)

conversation = []

agent = create_agent(model=llm, tools=[], system_prompt="You are a helpful assistant. Answer in short.")

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    conversation.append({"role": "user", "content":user_input})

    result = agent.invoke({"messages":conversation})

    ai_msg = result["messages"][-1]
    print("AI: ",ai_msg.content)

    Connection = result["messages"]