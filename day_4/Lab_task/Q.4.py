import streamlit as st
import pandas as pd
from datetime import datetime
import os

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["userid", "password"]).to_csv("users.csv", index=False)

if not os.path.exists("userfiles.csv"):
    pd.DataFrame(columns=["userid", "filename", "upload_time"]).to_csv("userfiles.csv", index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "userid" not in st.session_state:
    st.session_state.userid = ""

st.sidebar.title("Menu")

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Navigation", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigation", ["Explore CSV", "See History", "Logout"])

if menu == "Home":
    st.title("Home")
    st.write("Welcome! Please Login or Register.")

elif menu == "Register":
    st.title("Register")

    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Register"):
        users = pd.read_csv("users.csv")

        if user in users["userid"].values:
            st.error("User already exists")
        else:
            users.loc[len(users)] = [user, pwd]
            users.to_csv("users.csv", index=False)
            st.success("Registration successful")

elif menu == "Login":
    st.title("Login")

    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv("users.csv")
        match = users[(users["userid"] == user) & (users["password"] == pwd)]

        if not match.empty:
            st.session_state.logged_in = True
            st.session_state.userid = user
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif menu == "Explore CSV":
    st.title("Explore CSV")

    file = st.file_uploader("Upload CSV File", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)

        history = pd.read_csv("userfiles.csv")
        history.loc[len(history)] = [
            st.session_state.userid,
            file.name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        history.to_csv("userfiles.csv", index=False)

        st.success("CSV uploaded & history saved")

elif menu == "See History":
    st.title("Upload History")

    history = pd.read_csv("userfiles.csv")
    user_history = history[history["userid"] == st.session_state.userid]

    if user_history.empty:
        st.info("No upload history found")
    else:
        st.dataframe(user_history)

elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.userid = ""
    st.success("Logged out successfully")
    st.rerun()
