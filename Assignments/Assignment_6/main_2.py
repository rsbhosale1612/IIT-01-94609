import os
import requests
import time
import streamlit as st
import time 
from dotenv import load_dotenv
import json

st.title("My Chatbot")
load_dotenv()

# Initialization 
if 'model' not in st.session_state:
    st.session_state.model = None

if 'groq_conversation' not in st.session_state:
    st.session_state.groq_conversation = []

if 'lm_conversation' not in st.session_state:
    st.session_state.lm_conversation = []

# Sidebar
with st.sidebar:
    st.header("Settings")
    choices = ["Select model", "GROQ", "LM-Studio"]
    st.session_state.model = st.selectbox("Select choice", choices)

# Display page header
if not st.session_state.model == "Select model":
    st.header(st.session_state.model)
else:
    st.write("Welcome to My Chatbot!!")

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
        "messages": get_conversation()
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
        # "model": "meta-llama-3.1-8b-instruct",
        "messages": get_conversation()
    }

    response = requests.post(url, data=json.dumps(data), headers = headers)
    return response

def get_conversation():
    if st.session_state.model == "GROQ":
        return st.session_state.groq_conversation
    elif st.session_state.model == "LM-Studio":
        return st.session_state.lm_conversation

# User Input
user_prompt = st.chat_input("Ask anything")

if user_prompt:
    if st.session_state.model == "GROQ":
        st.session_state.groq_conversation.append(
            {"role": "user", "content": user_prompt}
        )
        response = groq_connection()
        result = response.json()
        assistant_msg = result["choices"][0]["message"]["content"]
        st.session_state.groq_conversation.append(
            {"role": "assistant", "content": assistant_msg}
        )
           
    if st.session_state.model == "LM-Studio":
        st.session_state.lm_conversation.append(
            {"role": "user", "content": user_prompt}
        )
        response = lm_connection()
        result = response.json()
        assistant_msg = result["choices"][0]["message"]["content"]

        st.session_state.lm_conversation.append(
            {"role": "assistant", "content": assistant_msg}
        )

# Display message history
if st.session_state.model == "GROQ":
    msglist = st.session_state.groq_conversation
    for msg in msglist:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
elif st.session_state.model == "LM-Studio":
    msglist = st.session_state.lm_conversation
    for msg in msglist:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])





