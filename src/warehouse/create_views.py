"""
Purpose:
    Create SQL reporting views for Power BI dashboarding.

Inputs:
    data/processed/nba_revenue_optimization.sqlite
    sql/create_views.sql

Outputs:
    SQL views for revenue, customers, funnel, and executive dashboard reporting.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import sqlite3
from src.config import DATABASE_PATH, SCHEMA_DIR

SQL_PATH = SCHEMA_DIR / "create_views.sql"
DB_PATH = DATABASE_PATH


def create_views():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run src/03_load_sql.py first.")

    with sqlite3.connect(DB_PATH) as conn:
        sql = SQL_PATH.read_text()
        conn.executescript(sql)

    print("SQL reporting views created successfully.")


if __name__ == "__main__":
    create_views()