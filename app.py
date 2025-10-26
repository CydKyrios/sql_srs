# pylint: disable=missing-module-docstring
import io
import streamlit as st
import pandas as pd
import duckdb


CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

st.header("Enter your SQL query:")
sql_query = st.text_area(label="Input sql query...", key="user_input")
if sql_query:
    result = duckdb.sql(sql_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing!")

    if result.shape[0] != solution_df.shape[0]:
        st.write("Some lines are missing!")


with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab2:
    st.write(answer_str)
