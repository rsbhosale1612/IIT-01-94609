import pandas as pd
import streamlit as st 
import duckdb

st.title("CSV File SQL Query")

datafile = st.file_uploader("Upload CSV File", type=["csv"])

if datafile is not None :

    df = pd.read_csv(datafile)
    st.subheader("Uploaded CSV Data")
    st.dataframe(df)

    st.subheader("Enter SQL Query")
    query = st.text_area ("Write SQL query (use table name as df)",
        placeholder="Example: SELECT * FROM df WHERE column_name > 10")
    
    if st.button("Run Query"):
        try:

            result = duckdb.query(query).to_df()
            st.subheader("Query Result")
            st.dataframe(result)
        except Exception as e:
            st.error(f"Error {e}")