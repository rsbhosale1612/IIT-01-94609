import pandas as pd
from pandasql import sqldf
from pandasql import sqldf

def run_sql_query(df, sql):
    return sqldf(sql, {"df": df})


def get_schema(df):
    schema = []
    for col in df.columns:
        schema.append({
            "column": col,
            "dtype": str(df[col].dtype)
        })
    return schema


def run_sql(df, query):
    pysqldf = lambda q: sqldf(q, {"df" : df})
    return pysqldf(query)

def english_to_sql(question, table_name="df"):
    q = question.lower()

    if "count" in q:
        return f"SELECT COUNT(*) FROM {table_name}"

    if "average" in q or "avg" in q:
        col = q.split("of")[-1].strip()
        return f"SELECT AVG({col}) FROM {table_name}"

    if "maximum" in q or "max" in q:
        col = q.split("of")[-1].strip()
        return f"SELECT MAX({col}) FROM {table_name}"

    if "minimum" in q or "min" in q:
        col = q.split("of")[-1].strip()
        return f"SELECT MIN({col}) FROM {table_name}"

    return f"SELECT * FROM {table_name} LIMIT 5"