import os 
import requests 
import json 
import time 
from dotenv import load_dotenv 
import streamlit as st

st.title("My Chatbot")
load_dotenv()

apikey="dummy"
url="http://127.0.0.1:1234/v1/chat/completions"

headers={
    "Authorization" : f"Bearer {apikey}",    
    "Content-Type" : "application/json"
}

user_prompt=st.chat_input("Prompt here...")

if user_prompt:
    req_data = {
        "model" : "meta-llama-3.1-8b-instruct",
        "messages" : [
            {"role" : "user" , "content" : user_prompt}
        ],
    }

    time1=time.perf_counter()
    response=requests.post(url,headers=headers,data=json.dumps(req_data))
    time2=time.perf_counter() 

    resp=response.json()
    st.write(resp["choices"][0]["message"]["content"])
    st.write(f"Time required : {time2-time1:.2f} secs")
