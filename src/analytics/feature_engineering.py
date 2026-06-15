"""
Purpose:
    Build a game-level modeling dataset for segmentation and forecasting.

Inputs:
    data/processed/nba_revenue_optimization.sqlite

Outputs:
    data/processed/model_dataset.csv
    SQL table: model_dataset
"""
import logging
import sqlite3

import pandas as pd

from src.config import DATABASE_PATH, MODEL_DATASET_PATH
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

DB_PATH = DATABASE_PATH
OUTPUT_PATH = MODEL_DATASET_PATH


def build_model_dataset():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run src/etl/load.py first.")

    query = """
    WITH ticket_metrics AS (
        SELECT
            game_id,
            COUNT(transaction_id) AS total_transactions,
            SUM(seats_purchased) AS tickets_sold,
            SUM(revenue) AS total_revenue,
            AVG(ticket_price) AS avg_ticket_price,
            AVG(seats_purchased) AS avg_seats_per_order,
            AVG(revenue) AS avg_order_value,
            COUNT(DISTINCT customer_id) AS unique_customers,
            1.0 * SUM(CASE WHEN promotion_id != 0 THEN 1 ELSE 0 END)
                / COUNT(transaction_id) AS promotion_usage_rate
        FROM fact_ticket_transactions
        GROUP BY game_id
    ),

    web_metrics AS (
        SELECT
            game_id,
            COUNT(session_id) AS web_sessions,
            SUM(added_to_cart) AS cart_adds,
            SUM(checkout_started) AS checkouts,
            SUM(purchased) AS web_purchases,
            1.0 * SUM(added_to_cart) / COUNT(session_id) AS cart_rate,
            1.0 * SUM(checkout_started) / NULLIF(SUM(added_to_cart), 0) AS checkout_rate,
            1.0 * SUM(purchased) / COUNT(session_id) AS purchase_rate,
            1.0 - (1.0 * SUM(purchased) / NULLIF(SUM(added_to_cart), 0)) AS cart_abandonment_rate
        FROM fact_web_sessions
        GROUP BY game_id
    )

    SELECT
        g.game_id,
        g.game_date,
        g.opponent,
        g.day_of_week,
        g.is_weekend,
        g.opponent_strength,
        g.arena_capacity,

        COALESCE(t.total_transactions, 0) AS total_transactions,
        COALESCE(t.tickets_sold, 0) AS tickets_sold,
        COALESCE(t.total_revenue, 0) AS total_revenue,
        COALESCE(t.avg_ticket_price, 0) AS avg_ticket_price,
        COALESCE(t.avg_seats_per_order, 0) AS avg_seats_per_order,
        COALESCE(t.avg_order_value, 0) AS avg_order_value,
        COALESCE(t.unique_customers, 0) AS unique_customers,
        COALESCE(t.promotion_usage_rate, 0) AS promotion_usage_rate,

        g.arena_capacity - COALESCE(t.tickets_sold, 0) AS inventory_remaining,
        1.0 * COALESCE(t.tickets_sold, 0) / g.arena_capacity AS sell_through_rate,

        COALESCE(w.web_sessions, 0) AS web_sessions,
        COALESCE(w.cart_adds, 0) AS cart_adds,
        COALESCE(w.checkouts, 0) AS checkouts,
        COALESCE(w.web_purchases, 0) AS web_purchases,
        COALESCE(w.cart_rate, 0) AS cart_rate,
        COALESCE(w.checkout_rate, 0) AS checkout_rate,
        COALESCE(w.purchase_rate, 0) AS purchase_rate,
        COALESCE(w.cart_abandonment_rate, 0) AS cart_abandonment_rate

    FROM dim_games g
    LEFT JOIN ticket_metrics t
        ON g.game_id = t.game_id
    LEFT JOIN web_metrics w
        ON g.game_id = w.game_id
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

        # Fill any missing values from divisions or sparse data.
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        df.to_csv(OUTPUT_PATH, index=False)
        df.to_sql("model_dataset", conn, if_exists="replace", index=False)

    logger.info(f"Created modeling dataset with {len(df)} games.")
    logger.info(f"Saved CSV to {OUTPUT_PATH}")
    logger.info("Saved SQL table: model_dataset")


if __name__ == "__main__":
    build_model_dataset()
