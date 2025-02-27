import pandas as pd
import sql.database_management as dbm


def process_csv(file_path):
    """Processes a CSV file and returns a DataFrame."""
    # Load CSV file into a DataFrame
    df = pd.read_csv(file_path)

    dbm.create_db()

    for index, row in df.iterrows():
        name = row["Description"]
        date = row["Completed Date"]
        type = row["Type"]
        value = row["Amount"]
        dbm.insert_data(name, date, type, value)

    # Display first few rows
    print(df.head())

    return df


if __name__ == "__main__":
    file_path = ""
    process_csv(file_path)
