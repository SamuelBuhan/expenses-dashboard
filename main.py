import streamlit as st
import pandas as pd  # read csv, df manipulation
import plotly.express as px 
import sqlite3


# page setting
st.set_page_config(page_title="Expenses Dashboard",
                        layout="wide")

# Gloabal variable
NORMAL_SIZE = 1
INPUT_SIZE = 3
GRAPH_SIZE = 6

NAME_LABEL = "Name"
DATE_LABEL = "Date"
TYPE_LABEL = "Type"
VALUE_LABEL = "Value"

SQL_DATABASE = "database.db"


# SQL
def create_db():
    conn = sqlite3.connect(SQL_DATABASE)  
    cursor = conn.cursor()

    # Create the correct table if it doesn't exist
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {NAME_LABEL} TEXT,
        {DATE_LABEL} TEXT,
        {TYPE_LABEL} TEXT,
        {VALUE_LABEL} INTEGER)
    ''')

    conn.commit()
    conn.close()

def reset_database():
    conn = sqlite3.connect(SQL_DATABASE)
    cursor = conn.cursor()

    # Delete all entries from the table
    cursor.execute("DELETE FROM entries")

    # Check the number of rows after deletion
    cursor.execute("SELECT COUNT(*) FROM entries")

    conn.commit()
    conn.close()

# Function to connect to database
def get_db_connection():
    conn = sqlite3.connect(SQL_DATABASE)
    #conn.row_factory = sqlite3.Row
    return conn

# Insert data into the database
def insert_data(name, date, type, number):
    conn = get_db_connection()
    cursor = conn.cursor()
    data_to_store = f"{NAME_LABEL}, {DATE_LABEL}, {TYPE_LABEL}, {VALUE_LABEL}"
    cursor.execute(f"INSERT INTO entries ({data_to_store}) VALUES (?, ?, ?, ?)",
                    (name, date, type, number))
    conn.commit()
    conn.close()

def remove_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

# Retrieve data from database
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM entries")
    count = cursor.fetchone()[0]  # Get the count value

    # check if any entries
    if count == 0:
        conn.close()
        return None 
    
    df = pd.read_sql("SELECT * FROM entries", conn)
    conn.close()
    return df


'''


'''
    
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
    insert_data(exp_name, exp_date, exp_type, exp_number)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

def input_data_tab():
    st.header("Insert new data")

    # TODO: implement this feature later
    # st.markdown(''' You can choose to create a dataframe of expenses
    # or to import an existing CSV file. To see the results of these data,
    # click on the tab called "Analysis".         
    # ''')

    # st.subheader("Import your CSV file")
    # uploaded_csv = st.file_uploader("Import CSV files", type="primary", 
    #                                 accept_multiple_files=False)
    # if uploaded_csv is not None:
    #     process_csv(uploaded_csv)
    # st.divider()

    #st.subheader("Create your CSV file")
    col_name, col_date, col_type, col_number, col_add = st.columns([INPUT_SIZE, INPUT_SIZE, INPUT_SIZE,
                                                                    INPUT_SIZE, NORMAL_SIZE])

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
                insert_data(exp_name, exp_date, exp_type, exp_number)
            else:
                st.write("it miss at least one argument for expense")

    st.subheader("View here the expense added:")
    col_view_data, col_id_rm,_, _= st.columns([INPUT_SIZE, NORMAL_SIZE, NORMAL_SIZE, 
                                                  NORMAL_SIZE])

    with col_view_data:
        df_data = get_data()
        if df_data is not None:
            st.dataframe(df_data, use_container_width=True)
            st.download_button(
                label="Download data as CSV",
                data=convert_df(df_data),
                file_name="personal_finance.csv",
                mime="text/csv",
            )

    with col_id_rm:
        df_data = get_data()
        if df_data is not None:
            entry_to_remove = st.selectbox("Select an entry to remove", df_data["id"].tolist())
            if st.button("Remove", type='primary', use_container_width=False):
                remove_entry(entry_to_remove)
                st.warning(f"Entry {entry_to_remove} removed!")
                # rerun all script for update
                st.rerun()
    


def main_page():
    st.title("Expenses Dashboard")

    tab_input_data, tab_analysis = st.tabs(["Input data", "Analysis"])
    with tab_input_data:
        input_data_tab()
    with tab_analysis:
        analysis_tab()


if __name__ == "__main__":
    create_db()
    main_page()
    