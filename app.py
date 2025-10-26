# pylint: disable=missing-module-docstring
import os
import logging
import duckdb
import streamlit as st
import pandas as pd


if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercise_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())


def compare_df_to_sol(q_input : str)->None:
    '''
    Compare df from qery to solution of exercise
    :param q_input: input query
    :return: None
    '''
    result = con.execute(q_input).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing!")
    if result.shape[0] != solution_df.shape[0]:
        st.write("Some lines are missing!")

con = duckdb.connect(database="data/exercise_sql_tables.duckdb", read_only=False)


with st.sidebar:
    list_theme = con.execute("SELECT theme FROM memory_state").df()["theme"].tolist()
    theme = st.selectbox(
        "What would you like to review?",
        list_theme,
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write("You selected:", theme)
        select_ex_q = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else:
        select_ex_q = f"SELECT * FROM memory_state"
    exercise = (
        con.execute(select_ex_q)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer_from_file = f.read()

    solution_df = con.execute(f"{answer_from_file}").df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

st.header("Enter your SQL query:")
sql_query = st.text_area(label="Input sql query...", key="user_input")

if sql_query:
    compare_df_to_sol(sql_query)

tab1, tab2 = st.tabs(["Tables", "Solution"])
#
with tab1:
    # print("hello")
    # exercises_tables = ast.literal_eval(exercise.loc[0, "tables"])
    exercises_tables = exercise.loc[0, "tables"]
    for table in exercises_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
with tab2:
    st.write(answer_from_file)
