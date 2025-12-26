import streamlit as st
import pandas as pd

from csv_agent import get_schema, english_to_sql, run_sql_query

from web_agent import scrape_sunbeam, answer_question


st.set_page_config(
    page_title=" Intelligent Agents App",
    layout="wide"
)

st.title(" Intelligent Agents using Streamlit")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "sunbeam_data" not in st.session_state:
    st.session_state.sunbeam_data = None


st.sidebar.header(" Agent Selector")

agent = st.sidebar.selectbox(
    "Choose Agent",
    [
        "CSV Question Answering Agent",
        "Sunbeam Web Scraping Agent"
    ]
)

st.sidebar.divider()

st.sidebar.subheader(" Complete Chat History")
for source, q, a in reversed(st.session_state.chat_history):
    st.sidebar.markdown(f"**[{source}] Q:** {q}")
    st.sidebar.markdown(f" {a}")
    st.sidebar.divider()


if agent == "CSV Question Answering Agent":
    st.header(" CSV Question Answering Agent")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("CSV Preview")
            st.dataframe(df.head())

        with col2:
            st.subheader("CSV Schema")
            st.json(get_schema(df))

        question = st.text_input(
            "Ask a question about the CSV (avg, sum, max, min, count)"
        )

        if st.button("Ask CSV Agent"):
            sql, error = english_to_sql(question, df)

            if error:
                st.error(error)
            else:
                st.markdown("**Generated SQL Query:**")
                st.code(sql, language="sql")

                result = run_sql_query(df, sql)
                st.subheader("Result")
                st.write(result)

                st.session_state.chat_history.append(
                    ("CSV", question, result)
                )


elif agent == "Sunbeam Web Scraping Agent":
    st.header(" Sunbeam Web Scraping Agent (Selenium)")

    if st.session_state.sunbeam_data is None:
        with st.spinner("Scraping Sunbeam website using Selenium..."):
            st.session_state.sunbeam_data = scrape_sunbeam()

    question = st.text_input(
        "Ask about Sunbeam internship or batch information"
    )

    if st.button("Ask Web Agent"):
        answer = answer_question(
            st.session_state.sunbeam_data,
            question
        )

        st.subheader("Answer")
        st.write(answer)

        st.session_state.chat_history.append(
            ("WEB", question, answer)
        )
