import pandas as pd  # read csv, df manipulation
import sqlite3


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

if __name__ == "__main__":
    print("-----> create database")
    create_db()

    print("-----> insert data")
    insert_data("test1", "02/05/2025", "expense", 10)
    insert_data("test2", "03/05/2025", "expense", 20)
    insert_data("test3", "04/05/2025", "expense", 30)
    df = get_data()
    print(df)

    print(f"-----> remove data id {df['id'].iloc[0]}")
    remove_entry(int(df['id'].iloc[0]))
    df = get_data()
    print(df)

    print("-----> reset database")
    reset_database()
    df = get_data()
    print(df)