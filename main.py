import streamlit as st
import pandas as pd  # read csv, df manipulation
import plotly.express as px 

NORMAL_SIZE = 1
INPUT_SIZE = 3
GRAPH_SIZE = 6

NAME_LABEL = "Name"
DATE_LABEL = "Date"
TYPE_LABEL = "Type"
NUMBER_LABEL = "Number"

def create_empty_data():
    st.session_state["main_data"] = {NAME_LABEL:[],
                                    DATE_LABEL:[],
                                    TYPE_LABEL: [],
                                    NUMBER_LABEL: []}
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

def add_dict_expenses(exp_name, exp_date, exp_type, exp_number):
    st.session_state["main_data"][NAME_LABEL].append(exp_name)
    st.session_state["main_data"][DATE_LABEL].append(exp_date)
    st.session_state["main_data"][TYPE_LABEL].append(exp_type)
    st.session_state["main_data"][NUMBER_LABEL].append(exp_number)

def remove_dict_expenses(exp_name, exp_type, exp_number):
    create_empty_data()

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

def input_data_tab():
    print(st.session_state["main_data"])
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
    col_name, col_date, col_type, col_number, col_add, col_remove = st.columns([INPUT_SIZE, INPUT_SIZE, INPUT_SIZE,
                                                                    INPUT_SIZE, NORMAL_SIZE, NORMAL_SIZE])

    with col_name:
        exp_name = st.text_input("name")
    with col_date:
        exp_date = st.date_input(
            "Select date of expense/income",
            format="MM.DD.YYYY")
    with col_type:
        exp_type = st.selectbox("type", {"income","expense"})
    with col_number:
        exp_number = st.number_input(label="value")
    with col_add:
        # workaround to align
        st.write("")
        st.write("")
        
        expense_filled = (exp_name != "") and (exp_number != "")
        if st.button("Add", type='primary', use_container_width=True):
            if expense_filled:
                st.write(f"You add {exp_name}")
                add_dict_expenses(exp_name, exp_date, exp_type, exp_number)
            else:
                st.write("it miss at least one argument for expense")
    with col_remove:
         # workaround to align
        st.write("") 
        st.write("")

        if st.button("Remove", type='primary', use_container_width=True):
            remove_dict_expenses(exp_name, exp_type, exp_number)
            st.write(f"You remove {exp_name}")  

    st.subheader("View here the expense added:")
    df_data = pd.DataFrame(st.session_state["main_data"])
    st.write(df_data)
    st.download_button(
        label="Download data as CSV",
        data=convert_df(df_data),
        file_name="large_df.csv",
        mime="text/csv",
    )


def main_page():
    st.title("Expenses Dashboard")

    # Main dict share through function
    if "main_data" not in st.session_state:
        create_empty_data()

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