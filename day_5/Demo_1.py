import requests 
import os 
import json 
import time 
from dotenv import load_dotenv 

load_dotenv()
apikey=os.getenv("GROQCLOUD_API_Key_3")
url="https://api.groq.com/openai/v1/chat/completions"

headers={
    "Authorization" : f"Bearer {apikey}",
    "Content-Type" : "application/json"
}

while True:
    user_prompt=input("Prompt here : ")

    if user_prompt=="exit":
        break
    
    req_data={
        "model" : "llama-3.3-70b-versatile",
        "messages" : [
            {"role" : "user" , "content" : user_prompt}
        ],
    }

    time1=time.perf_counter()
    response=requests.post(url,headers=headers,data=json.dumps(req_data))
    time2=time.perf_counter()
    print("Status code : ",response.status_code)

    resp=response.json()

    print(resp["choices"][0]["message"]["content"])
    print(f"Time required : {time2-time1:.2f} seconds")