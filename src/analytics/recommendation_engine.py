"""
Purpose:
    Generate executive recommendations from model outputs.

Inputs:
    data/processed/nba_revenue_optimization.sqlite

Outputs:
    SQL table: executive_recommendations
    data/processed/executive_recommendations.csv
"""
import logging
import sqlite3

import pandas as pd

from src.config import (
    DATABASE_PATH,
    EXECUTIVE_RECOMMENDATIONS_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

DB_PATH = DATABASE_PATH
OUTPUT_PATH = EXECUTIVE_RECOMMENDATIONS_PATH


def build_recommendations():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        m.game_id,
        m.game_date,
        m.opponent,
        m.total_revenue,
        m.sell_through_rate,
        m.cart_abandonment_rate,
        f.predicted_revenue,
        f.sellout_probability,
        s.segment_name
    FROM model_dataset m
    LEFT JOIN revenue_forecasts f
        ON m.game_id = f.game_id
    LEFT JOIN game_segments s
        ON m.game_id = s.game_id
    """

    df = pd.read_sql(query, conn)

    recommendations = []

    for _, row in df.iterrows():
        recommendation = ""
        priority = "Medium"

        if row.segment_name == "Premium Demand":
            recommendation = "Increase premium seating prices 5-10% and release additional premium inventory."
            priority = "High"

        elif row.segment_name == "Promotion Opportunity":
            recommendation = (
                "Launch targeted promotions such as Student Night or Family Pack."
            )

        elif row.segment_name == "Inventory Risk":
            recommendation = "Increase marketing spend and improve checkout conversion."

        else:
            recommendation = "Maintain current pricing strategy and monitor sales pace."

        if row.cart_abandonment_rate > 0.45:
            recommendation += " Investigate checkout abandonment."

        if row.sellout_probability > 0.95:
            recommendation += " Consider dynamic pricing."

        recommendations.append(
            {
                "game_id": row.game_id,
                "opponent": row.opponent,
                "segment": row.segment_name,
                "predicted_revenue": row.predicted_revenue,
                "sellout_probability": row.sellout_probability,
                "priority": priority,
                "recommendation": recommendation,
            }
        )

    recommendations = pd.DataFrame(recommendations)

    recommendations.to_csv(OUTPUT_PATH, index=False)

    recommendations.to_sql(
        "executive_recommendations",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    logger.info(recommendations.head())

    logger.info("\nExecutive recommendations created.")


if __name__ == "__main__":
    build_recommendations()
