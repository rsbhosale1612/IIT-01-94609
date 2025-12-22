import streamlit as st
import pandas as pd
from csv_agent import get_schema, run_sql, english_to_sql
from web_agent import screape_sunbeam, answer_que
from csv_agent import run_sql_query


st.set_page_config(page_title= "Intelligent Agents App")

st.title("🤖 Intelligent Agents using Streamlit")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.sidebar.selectbox(
    "Choose Agent",
    ["CSV Question Answering Agent", "Sunbeam Web Scraping Agent"]
)

if agent == "CSV Question Answering Agent":
    st.header("📊 CSV Question Answering Agent")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### CSV Preview")
        st.dataframe(df.head())

        st.write("### CSV Schema")
        schema = get_schema(df)
        st.json(schema)

        question = st.text_input("Ask a question about the CSV")

        if st.button("Ask"):
            sql = english_to_sql(question)
            result = run_sql_query(df, sql)

            st.write("### SQL Query Used")
            st.code(sql)

            st.write("### Answer")
            st.dataframe(result)

            st.session_state.chat_history.append(
                ("User", question)
            )
            st.session_state.chat_history.append(
                ("Agent", f"Query executed and result displayed.")
            )


if agent == "Sunbeam Web Scraping Agent":
    st.header("🌐 Sunbeam Web Scraping Agent")

    data = screape_sunbeam()

    question = st.text_input("Ask about Sunbeam internships or batches")

    if st.button("Ask"):
        answer = answer_que(question, data)

        st.write("### Answer")
        st.success(answer)

        st.session_state.chat_history.append(
            ("User", question)
        )
        st.session_state.chat_history.append(
            ("Agent", answer)
        )

st.sidebar.header("💬 Chat History")

for role, msg in st.session_state.chat_history:
    st.sidebar.write(f"**{role}:** {msg}")