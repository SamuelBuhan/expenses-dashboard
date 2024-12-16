import streamlit as st
import pandas as pd  # read csv, df manipulation
import plotly.express as px 

main_data = {}

def main_page():
    st.title("Expenses Dashboard")
    col1, col2 = st.columns([2,1])
    with col1:
        st.header("Summary expenses")
        col_name, col_type, col_number = st.columns(3)
        with col_name:
            st.number_input("name")
        with col_type:
            st.selectbox("type", {"income","expense"})
        with col_number:
            st.number_input(label="value")


    with col2:
        st.header("charts")
        st.button("no")









if __name__ == "__main__":
    st.set_page_config(
    page_title="Expenses Dashboard",
    layout="wide")
    main_page()