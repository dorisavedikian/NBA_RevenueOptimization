"""
Purpose:
    Create SQL reporting views for Power BI dashboarding.

Inputs:
    data/processed/nba_revenue_optimization.sqlite
    sql/create_views.sql

Outputs:
    SQL views for revenue, customers, funnel, and executive dashboard reporting.
"""

from pathlib import Path
import sqlite3

DB_PATH = Path("data/processed/nba_revenue_optimization.sqlite")
SQL_PATH = Path("sql/schema/create_views.sql")


def create_views():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run src/03_load_sql.py first.")

    with sqlite3.connect(DB_PATH) as conn:
        sql = SQL_PATH.read_text()
        conn.executescript(sql)

    print("SQL reporting views created successfully.")


if __name__ == "__main__":
    create_views()