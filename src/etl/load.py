"""
Purpose:
    Load processed NBA revenue optimization CSV files into a SQLite database
    for SQL analysis and Power BI dashboarding.

Inputs:
    data/processed/dim_games.csv
    data/processed/dim_customers.csv
    data/processed/dim_sections.csv
    data/processed/dim_promotions.csv
    data/processed/fact_ticket_transactions.csv
    data/processed/fact_web_sessions.csv

Outputs:
    data/processed/nba_revenue_optimization.sqlite
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import sqlite3
import pandas as pd
from src.config import DATABASE_PATH, PROCESSED_DIR

DB_PATH = DATABASE_PATH

TABLES = {
    "dim_games": "dim_games.csv",
    "dim_customers": "dim_customers.csv",
    "dim_sections": "dim_sections.csv",
    "dim_promotions": "dim_promotions.csv",
    "fact_ticket_transactions": "fact_ticket_transactions.csv",
    "fact_web_sessions": "fact_web_sessions.csv",
}


def load_csv_to_sql():
    conn = sqlite3.connect(DB_PATH)

    for table_name, file_name in TABLES.items():
        file_path = PROCESSED_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"Loaded {len(df):,} rows into {table_name}")

    conn.close()
    print(f"\nSQLite database created at: {DB_PATH}")


if __name__ == "__main__":
    load_csv_to_sql()