import os
import requests
import time
import streamlit as st
import time 
from dotenv import load_dotenv
import json

st.title("My Chatbot")

# Initialization 
if 'model' not in st.session_state:
    st.session_state.model = None

if 'groq_messages' not in st.session_state:
    st.session_state.groq_messages = []

if 'lm_messages' not in st.session_state:
    st.session_state.lm_messages = []

load_dotenv()
# Sidebar
with st.sidebar:
    st.header("Settings")
    choices = ["Select model", "GROQ", "LM-Studio"]
    st.session_state.model = st.selectbox("Select choice", choices)
# if model == "GORQ":
#     st.session_state.model = "GROQ"
#     st.rerun()   
# elif model == "LM-Studio":
#     st.session_state.model = "LM-Studio" 
#     st.rerun()
if not st.session_state.model == "Select model":
    st.header(st.session_state.model)
else:
    st.write("Welcome to My Chatbot!!")
user_prompt = st.chat_input("Ask anything")

# Functions
def groq_connection():
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(url, data=json.dumps(data), headers = headers)
    return response


def lm_connection():
    api_key = os.getenv("LM_API_KEY")
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemma-3-12b",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, data=json.dumps(data), headers = headers)
    return response


if user_prompt:
    if st.session_state.model == "GROQ":
        response = groq_connection()
        result = response.json()
        assistant_msg = result["choices"][0]["message"]["content"]

        st.session_state.groq_messages.append(user_prompt)
        st.session_state.groq_messages.append(assistant_msg)
        
        # msglist = st.session_state.groq_messages
        # for idx, msg in enumerate(msglist):
        #     role = "human" if idx % 2 == 0 else "ai"
        #     with st.chat_message(role):
        #         st.write(msg)

        
    if st.session_state.model == "LM-Studio":
        response = lm_connection()
        result = response.json()
        assistant_msg = result["choices"][0]["message"]["content"]
        st.session_state.lm_messages.append(user_prompt)
        st.session_state.lm_messages.append(assistant_msg)
        
        # msglist = st.session_state.lm_messages
        # for idx, msg in enumerate(msglist):
        #     role = "human" if idx % 2 == 0 else "ai"
        #     with st.chat_message(role):
        #         st.write(msg)
        

if st.session_state.model == "GROQ":
    msglist = st.session_state.groq_messages
    for idx, msg in enumerate(msglist):
        role = "human" if idx % 2 == 0 else "ai"
        with st.chat_message(role):
            st.write(msg)
elif st.session_state.model == "LM-Studio":
    msglist = st.session_state.lm_messages
    for idx, msg in enumerate(msglist):
        role = "human" if idx % 2 == 0 else "ai"
        with st.chat_message(role):
            st.write(msg)