import os 
import requests 
import json 
import time 
import streamlit as st 
from dotenv import load_dotenv 

load_dotenv()

apikey_offline="dummy"
apikey_online=os.getenv("GROQCLOUD_API_Key_3")

url_online="https://api.groq.com/openai/v1/chat/completions"
url_offline="http://127.0.0.1:1234/v1/chat/completions"

st.title("My ChatBot")

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode= None

if "messages_online" not in st.session_state:
    st.session_state.messages_online=[]

if "messages_offline" not in st.session_state:
    st.session_state.messages_offline=[]

if "resp_time_online" not in st.session_state:
    st.session_state.resp_time_online=None

if "resp_time_offline" not in st.session_state:
    st.session_state.resp_time_offline=None

with st.sidebar:
    st.subheader("Settings")
    choices=["Groq-Online","Llama-Offline"]
    mode=st.selectbox("Select Mode",choices)

    st.session_state.chat_mode = "Online" if mode == "Groq-Online" else "Offline"


user_prompt=st.chat_input("Prompt here ...")

if user_prompt:

    if mode=="Groq-Online":

        # st.session_state.chat_mode="Online"

        # if "prompts_online" not in st.session_state:
        #     st.session_state.prompts_online=[]
        # if "responses_online" not in st.session_state:
        #     st.session_state.responses_online=[]

        headers={
            "Authorization" : f"Bearer {apikey_online}",
            "Content-Type" : "application/json"
        }

        req_data={
            "model" : "llama-3.3-70b-versatile",
            "messages" : [
                {"role" : "user" , "content" : user_prompt}
            ]
        }

        time1=time.perf_counter()
        response=requests.post(url_online,headers=headers,data=json.dumps(req_data))
        time2=time.perf_counter()

        resp=response.json()
        bot_resp=resp["choices"][0]["message"]["content"]

        st.session_state.messages_online.append(user_prompt)
        st.session_state.messages_online.append(bot_resp)
        st.session_state.resp_time_online=f"Time taken : {time2-time1:.2f} secs"
        
        # res_list=st.session_state.responses_online
        # for idx,res in enumerate(res_list):
        #     role = "Human" if idx % 2 == 0 else "AI"
        #     with st.chat_message(role):
        #         st.write(res)
        # st.write(f"Time taken : {time2-time1:.2f} secs")

        # st.rerun()

       
    if mode=="Llama-Offline":

        # st.session_state.chat_mode="Offline"

        # if "prompts_offline" not in st.session_state:
        #     st.session_state.prompts_offline=[]
        # if "responses_offline" not in st.session_state:
        #     st.session_state.responses_offline=[]

        headers={
            "Authorization" : f"Bearer {apikey_offline}",
            "Content-Type" : "application/json"            
        }

        req_data={
            "model" : "meta-llama-3.1-8b-instruct",
            "messages" : [
                {"role" : "user" , "content" : user_prompt}
            ],
        }

        time1=time.perf_counter()
        response=requests.post(url_offline,headers=headers,data=json.dumps(req_data))
        time2=time.perf_counter()

        resp=response.json()
        bot_resp=resp["choices"][0]["message"]["content"]

        st.session_state.messages_offline.append(user_prompt)
        st.session_state.messages_offline.append(bot_resp)
        st.session_state.resp_time_offline=f"Time taken : {time2-time1:.2f} secs"

        # res_list=st.session_state.responses_offline
        # for idx,res in enumerate(res_list):
        #     role = "Human" if idx % 2 == 0 else "AI"
        #     with st.chat_message(role):
        #         st.write(res)
        # st.write()

        # st.rerun()

if st.session_state.chat_mode=="Online":
    prompt_list=st.session_state.messages_online
    for idx,msg in enumerate(prompt_list):
        role = "Human" if idx % 2 == 0 else "AI"
        with st.chat_message(role):
            st.write(msg)
            if idx % 2 != 0:
                st.write(st.session_state.resp_time_online)
       
elif st.session_state.chat_mode=="Offline":
    prompt_list=st.session_state.messages_offline
    for idx,msg in enumerate(prompt_list):
        role = "Human" if idx % 2 == 0 else "AI"
        with st.chat_message(role):
            st.write(msg)
            if idx % 2 != 0:
                st.write(st.session_state.resp_time_offline)



