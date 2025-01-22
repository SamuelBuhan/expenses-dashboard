import streamlit as st
import pandas as pd  # read csv, df manipulation
import plotly.express as px 

NORMAL_SIZE = 1
INPUT_SIZE = 3
GRAPH_SIZE = 6

main_data = {}

def process_csv(file):
    dataframe = pd.read_csv(file)
    st.write(dataframe)
    
def display_metrics():
    st.header("Summary expenses")
    col_m1, col_m2, col_m3 = st.columns([NORMAL_SIZE,NORMAL_SIZE,NORMAL_SIZE])
    with col_m1:
        st.metric("Revenue", 0.0)
    with col_m2:
        st.metric("Spent", 0.0)
    with col_m3:
        st.metric("Save", 0.0)

def analysis_tab():
    col1, col2 = st.columns([INPUT_SIZE,GRAPH_SIZE])
    with col1:
        display_metrics()

    with col2:
        st.header("Charts")

        tab_scatter, tab_pie = st.tabs(["Scatter","Pie chart"])
        with tab_scatter:
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
            st.write(fig)
        with tab_pie:
            df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
            df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
            fig = px.pie(df, values='pop', names='country', title='Population of European continent')
            st.write(fig)

def input_data_tab():
    st.header("Insert new data")

    st.markdown(''' You can choose to create a dataframe of expenses
    or to import an existing CSV file. To see the results of these data,
    click on the tab called "Analysis".         
    ''')

    st.subheader("Import your CSV file")
    uploaded_csv = st.file_uploader("Import CSV files", type="primary", 
                                    accept_multiple_files=False)
    if uploaded_csv is not None:
        process_csv(uploaded_csv)

    st.divider()

    st.subheader("Create your CSV file")
    col_name, col_type, col_number, col_add, col_remove = st.columns([2, 2, 2, 1, 1])
    name = ""
    with col_name:
        name = st.text_input("name")
    with col_type:
        st.selectbox("type", {"income","expense"})
    with col_number:
        st.number_input(label="value")
    with col_add:
        # workaround to align
        st.write("")
        st.write("")

        if st.button("Add", type='primary', use_container_width=True):
            st.write(f"You add {name}")  
    with col_remove:
         # workaround to align
        st.write("") 
        st.write("")

        if st.button("Remove", type='primary', use_container_width=True):
            st.write(f"You remove {name}")  

def main_page():
    st.title("Expenses Dashboard")

    tab_input_data, tab_analysis = st.tabs(["Input data", "Analysis"])
    with tab_input_data:
        input_data_tab()
    with tab_analysis:
        analysis_tab()



if __name__ == "__main__":
    st.set_page_config(
    page_title="Expenses Dashboard",
    layout="wide")
    main_page()