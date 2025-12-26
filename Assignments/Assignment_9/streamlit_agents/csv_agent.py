from pandasql import sqldf

def get_schema(df):
    schema = {}
    for col in df.columns:
        schema[col] = str(df[col].dtype)
    return schema


def english_to_sql(question, df):
    question = question.lower()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        return None, " No numeric columns found for calculations."

    col = numeric_cols[0]  

    if "average" in question or "avg" in question:
        return f"SELECT AVG({col}) FROM df", None

    if "sum" in question:
        return f"SELECT SUM({col}) FROM df", None

    if "maximum" in question or "max" in question:
        return f"SELECT MAX({col}) FROM df", None

    if "minimum" in question or "min" in question:
        return f"SELECT MIN({col}) FROM df", None

    if "count" in question:
        return "SELECT COUNT(*) FROM df", None

    return None, " Could not understand the question."


def run_sql_query(df, sql):
    try:
        return sqldf(sql, {"df": df})
    except Exception as e:
        return f" SQL Error: {e}"
