import streamlit as st
import time

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    choices = ["Upper", "Lower", "Toggle"]
    mode = st.selectbox("Select Mode", choices)
    count = st.slider("Message Count", 2, 10, 6, 2)

    st.subheader("Config")
    st.json({"mode": mode, "count": count})


st.title("Ranveer Chatbot 🤖")

def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.3)   

msg = st.chat_input("Say something...")

if msg:
    st.session_state.messages.append(("human", msg))

    if mode == "Upper":
        reply = msg.upper()
    elif mode == "Lower":
        reply = msg.lower()
    else:
        reply = msg.swapcase()

    st.session_state.messages.append(("ai", reply))

for role, message in st.session_state.messages[-count:]:
    with st.chat_message(role):
        if role == "ai":
            st.write_stream(stream_reply(message))
        else:
            st.write(message)
