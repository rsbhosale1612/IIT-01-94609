import os 
import requests 
import json 
import time 
from dotenv import load_dotenv 

load_dotenv()

apikey="dummy_key"
url="http://127.0.0.1:1234/v1/chat/completions"
# url = "http://localhost:11434/v1/chat/completions"


headers={
    "Authorization" : f"Bearer {apikey}",
    "Content-Type" : "application/json"
}

while True:
    user_prompt=input("Propmt here : ")

    if user_prompt=="exit":
        break 

    req_data={
        "model" : "meta-llama-3.1-8b-instruct",
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
    print(f"\nTime taken for response : {time2-time1:.2f} seconds\n")