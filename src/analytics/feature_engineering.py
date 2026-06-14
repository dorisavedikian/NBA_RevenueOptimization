"""
Purpose:
    Build a game-level modeling dataset for segmentation and forecasting.

Inputs:
    data/processed/nba_revenue_optimization.sqlite

Outputs:
    data/processed/model_dataset.csv
    SQL table: model_dataset
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import sqlite3
import pandas as pd
from src.config import DATABASE_PATH, MODEL_DATASET_PATH

DB_PATH = DATABASE_PATH
OUTPUT_PATH = MODEL_DATASET_PATH


def build_model_dataset():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run src/etl/load.py first.")

    query = """
    SELECT
        g.game_id,
        g.game_date,
        g.opponent,
        g.day_of_week,
        g.is_weekend,
        g.opponent_strength,
        g.arena_capacity,

        COUNT(t.transaction_id) AS total_transactions,
        SUM(t.seats_purchased) AS tickets_sold,
        SUM(t.revenue) AS total_revenue,
        AVG(t.ticket_price) AS avg_ticket_price,
        AVG(t.seats_purchased) AS avg_seats_per_order,
        AVG(t.revenue) AS avg_order_value,

        COUNT(DISTINCT t.customer_id) AS unique_customers,
        1.0 * SUM(CASE WHEN t.promotion_id != 0 THEN 1 ELSE 0 END)
            / COUNT(t.transaction_id) AS promotion_usage_rate,

        g.arena_capacity - SUM(t.seats_purchased) AS inventory_remaining,
        1.0 * SUM(t.seats_purchased) / g.arena_capacity AS sell_through_rate,

        COUNT(ws.session_id) AS web_sessions,
        SUM(ws.added_to_cart) AS cart_adds,
        SUM(ws.checkout_started) AS checkouts,
        SUM(ws.purchased) AS web_purchases,

        1.0 * SUM(ws.added_to_cart) / COUNT(ws.session_id) AS cart_rate,
        1.0 * SUM(ws.checkout_started) / NULLIF(SUM(ws.added_to_cart), 0) AS checkout_rate,
        1.0 * SUM(ws.purchased) / COUNT(ws.session_id) AS purchase_rate,
        1.0 - (1.0 * SUM(ws.purchased) / NULLIF(SUM(ws.added_to_cart), 0)) AS cart_abandonment_rate

    FROM dim_games g
    LEFT JOIN fact_ticket_transactions t
        ON g.game_id = t.game_id
    LEFT JOIN fact_web_sessions ws
        ON g.game_id = ws.game_id
    GROUP BY
        g.game_id,
        g.game_date,
        g.opponent,
        g.day_of_week,
        g.is_weekend,
        g.opponent_strength,
        g.arena_capacity
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

        # Fill any missing values from divisions or sparse data.
        numeric_cols = df.select_dtypes(include="number").columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        df.to_csv(OUTPUT_PATH, index=False)
        df.to_sql("model_dataset", conn, if_exists="replace", index=False)

    print(f"Created modeling dataset with {len(df)} games.")
    print(f"Saved CSV to {OUTPUT_PATH}")
    print("Saved SQL table: model_dataset")


if __name__ == "__main__":
    build_model_dataset()