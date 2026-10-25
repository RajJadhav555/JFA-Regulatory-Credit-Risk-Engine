import sqlite3
import pandas as pd

DB_NAME = "jfa_risk.db"

def init_db():
    df = pd.read_csv("master_risk_ledger.csv")
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql("portfolio_ledger", conn, if_exists="replace", index=False)
    print("Database Initialized portfolio_ledger table created successfully.")

def load_portfolio():
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql("SELECT * FROM portfolio_ledger", conn)

if __name__ == "__main__":
    init_db()
    test_df = load_portfolio()
    print(f"Verified: Successfully loaded {len(test_df)} rows from SQLite.")