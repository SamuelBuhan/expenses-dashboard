import pdfplumber
import pandas as pd
import re
import os
#import sqlite3
#from sqlalchemy import create_engine

# ---------- CONFIGURATIONS ----------
PDF_FOLDER = "statements"  # Folder containing PDFs
DB_NAME = "finance.db"  # SQLite Database
TABLE_NAME = "transactions"  # SQL Table

# ---------- FUNCTIONS ----------
def extract_transactions(pdf_path):
    """Extracts transactions from a bank statement PDF."""
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    transaction = parse_transaction(line)
                    if transaction:
                        transactions.append(transaction)

    return transactions

def parse_transaction(line):
    """Extracts date, description, and amount from a line."""
    match = re.search(r"([A-Za-z]{3} \d{1,2}, \d{4})\s+(.+?)\s+€([\d,.]+)", line)
    if match:
        return {
            "date": match.group(1),
            "description": match.group(2),
            "amount": float(match.group(3).replace(",", "."))  # Convert to float
        }
    return None

# def save_to_sql(df, db_name, table_name):
#     """Saves the DataFrame to an SQL database."""
#     engine = create_engine(f"sqlite:///{db_name}")  # SQLite connection
#     df.to_sql(table_name, engine, if_exists="append", index=False)
#     print(f"✅ Data saved to {db_name} -> Table: {table_name}")

# ---------- MAIN EXECUTION ----------
def process_pdfs(pdf_folder, db_name, table_name):
    all_transactions = []
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            print(f"📄 Processing: {pdf_path}")
            transactions = extract_transactions(pdf_path)
            all_transactions.extend(transactions)

    if all_transactions:
        df = pd.DataFrame(all_transactions)
        print(df)
        #save_to_sql(df, db_name, table_name)

if __name__ == "__main__":
    process_pdfs("/Users/sbuhan/workspace/projects/python/expenses-dashboard/input_data/test/"
                 , DB_NAME, TABLE_NAME)