import pdfplumber
import pandas as pd
import re
import os
import sql.database_management as dbm

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

# ---------- MAIN EXECUTION ----------
def process_pdfs(pdf_folder, db_name="", table_name=""):
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

def process_pdf(pdf_path):
    all_transactions = []
    print(f"📄 Processing: {pdf_path}")
    transactions = extract_transactions(pdf_path)
    all_transactions.extend(transactions)

    if all_transactions:
        df = pd.DataFrame(all_transactions)
        
        # Display first few rows
        print(df.head())

        dbm.create_db()

        for index, row in df.iterrows():
            name = row["description"]
            date = row["date"]
            # TODO: extract the type from pdf
            type = "expenses"
            value = row["amount"]
            dbm.insert_data(name, date, type, value)




if __name__ == "__main__":
    process_pdfs("/Users/sbuhan/workspace/projects/python/expenses-dashboard/input_data/test/"
                 , DB_NAME, TABLE_NAME)