import os 
import requests 
import json 
from dotenv import load_dotenv 
import time

load_dotenv()

# apikey=os.getenv("GROQCLOUD_API_Key_3")
apikey="dummy"

# url="https://api.groq.com/openai/v1/chat/completions"
url="http://127.0.0.1:1234/v1/chat/completions"


headers={
    "Authorization" : f"Bearer {apikey}",
    "Content-Type" : "application/json"
}

req_data={
    # "model" : "llama-3.3-70b-versatile", 
    "model" : "meta-llama-3.1-8b-instruct",
    "messages" : [ 
        {"role" : "system" , "content" : "You are an experirnced politician"},
        {"role" : "user" , "content" : "who is pm of bharat"},

        # {"role" : "assistant" , "content" : "Narendra Modi"},
        {"role" : "user" , "content" : "where he born"}
    ],
}

time1=time.perf_counter()
response=requests.post(url,headers=headers,data=json.dumps(req_data))
time2=time.perf_counter()

print("Status code : ",response.status_code)
resp=response.json()
print(resp["choices"][0]["message"]["content"])
print(f"Time : {time2-time1:.2f} secs")