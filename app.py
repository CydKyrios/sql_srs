import streamlit as st
import pandas as pd
import duckdb

data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6]
}
df = pd.DataFrame(data)

st.write(df)

sql_query = st.text_area("Input sql query to extract from df:", value="")
q_sql = duckdb.query(f"{sql_query}").df()
st.write(q_sql)
