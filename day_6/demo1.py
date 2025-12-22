import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    print("❌ GROQ_API_KEY not found in environment")
    exit()

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_prompt = input("Ask Anything: ")
    if user_prompt.lower() == "exit":
        break

    req_data = {
        "model": "llama-3.1-8b-instant"
,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    start = time.perf_counter()
    response = requests.post(url, json=req_data, headers=headers)
    end = time.perf_counter()

    print("Status:", response.status_code)

    resp = response.json()

    # ✅ Error-safe handling
    if "choices" in resp:
        print(resp["choices"][0]["message"]["content"])
    else:
        print("❌ API Error:")
        print(resp)

    print(f"Time required: {end - start:.2f} sec\n")
