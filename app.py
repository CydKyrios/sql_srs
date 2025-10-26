# pylint: disable=missing-module-docstring
import io

import ast
import streamlit as st
import pandas as pd
import duckdb


con = duckdb.connect(database="data/exercise_sql_tables.duckdb", read_only=False)


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ["cross_joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

st.header("Enter your SQL query:")
sql_query = st.text_area(label="Input sql query...", key="user_input")

if sql_query:
    result = con.execute(sql_query).df()
    st.dataframe(result)
#
#     try:
#         result = result[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing!")
#
#     if result.shape[0] != solution_df.shape[0]:
#         st.write("Some lines are missing!")
#
#

#
tab1, tab2 = st.tabs(["Tables", "Solution"])
#
with tab1:
    exercises_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercises_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
with tab2:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        ANSWER_FROM_FILE = f.read()
    st.write(ANSWER_FROM_FILE)
