"""
Purpose:
    Load generated warehouse CSV files into the SQLite dimensional warehouse.

Inputs:
    data/warehouse/*.csv

Outputs:
    data/warehouse/nba_revenue_optimization.sqlite
"""
import logging
import sqlite3

import pandas as pd

from src.config import (
    DATABASE_PATH,
    DIM_CUSTOMERS_PATH,
    DIM_GAMES_PATH,
    DIM_PROMOTIONS_PATH,
    DIM_SECTIONS_PATH,
    FACT_TICKET_TRANSACTIONS_PATH,
    FACT_WEB_SESSIONS_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

TABLES = {
    "dim_games": DIM_GAMES_PATH,
    "dim_customers": DIM_CUSTOMERS_PATH,
    "dim_sections": DIM_SECTIONS_PATH,
    "dim_promotions": DIM_PROMOTIONS_PATH,
    "fact_ticket_transactions": FACT_TICKET_TRANSACTIONS_PATH,
    "fact_web_sessions": FACT_WEB_SESSIONS_PATH,
}


def load_csv_to_sql():
    """Load all warehouse CSVs into SQLite."""

    conn = sqlite3.connect(DATABASE_PATH)

    for table_name, csv_path in TABLES.items():
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"Loaded {table_name}")

    conn.close()

    logger.info("SQLite warehouse created:")
    logger.info(DATABASE_PATH)


def main():
    load_csv_to_sql()


if __name__ == "__main__":
    main()
