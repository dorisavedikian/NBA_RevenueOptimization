"""
Purpose:
    Build executive KPI tables for NBA Revenue Intelligence.

Inputs:
    data/processed/nba_revenue_optimization.sqlite

Outputs:
    SQL table: executive_kpis
    data/processed/executive_kpis.csv
"""
import logging
import sqlite3

import pandas as pd

from src.config import (
    DATABASE_PATH,
    EXECUTIVE_KPIS_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

DB_PATH = DATABASE_PATH
OUTPUT_PATH = EXECUTIVE_KPIS_PATH


def build_executive_kpis():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run run_pipeline.py first.")

    query = """
    SELECT
        COUNT(DISTINCT d.game_id) AS total_games,
        SUM(d.tickets_sold) AS total_tickets_sold,
        SUM(d.total_revenue) AS total_revenue,
        AVG(d.avg_ticket_price) AS avg_ticket_price,
        AVG(d.sell_through_rate) AS avg_sell_through_rate,
        SUM(d.inventory_remaining) AS total_inventory_remaining,

        SUM(d.web_sessions) AS total_web_sessions,
        SUM(d.cart_adds) AS total_cart_adds,
        SUM(d.checkouts) AS total_checkouts,
        SUM(d.web_purchases) AS total_web_purchases,
        AVG(d.purchase_rate) AS avg_purchase_rate,
        AVG(d.cart_abandonment_rate) AS avg_cart_abandonment_rate,

        AVG(f.predicted_tickets_sold) AS avg_predicted_tickets_sold,
        AVG(f.predicted_revenue) AS avg_predicted_revenue,
        AVG(f.sellout_probability) AS avg_sellout_probability,

        COUNT(CASE WHEN s.segment_name = 'Premium Demand' THEN 1 END) AS premium_demand_games,
        COUNT(CASE WHEN s.segment_name = 'Standard Demand' THEN 1 END) AS standard_demand_games,
        COUNT(CASE WHEN s.segment_name = 'Promotion Opportunity' THEN 1 END) AS promotion_opportunity_games,
        COUNT(CASE WHEN s.segment_name = 'Inventory Risk' THEN 1 END) AS inventory_risk_games

    FROM model_dataset d
    LEFT JOIN revenue_forecasts f
        ON d.game_id = f.game_id
    LEFT JOIN game_segments s
        ON d.game_id = s.game_id
    """

    with sqlite3.connect(DB_PATH) as conn:
        kpis = pd.read_sql_query(query, conn)

        kpis["revenue_per_game"] = kpis["total_revenue"] / kpis["total_games"]
        kpis["tickets_per_game"] = kpis["total_tickets_sold"] / kpis["total_games"]
        kpis["revenue_per_ticket"] = kpis["total_revenue"] / kpis["total_tickets_sold"]

        kpis.to_csv(OUTPUT_PATH, index=False)
        kpis.to_sql("executive_kpis", conn, if_exists="replace", index=False)

    logger.info("Executive KPI table created.")
    logger.info(f"Saved CSV to {OUTPUT_PATH}")
    logger.info("Saved SQL table: executive_kpis")

    logger.info("\nExecutive KPI Summary:")
    logger.info(kpis.T)


if __name__ == "__main__":
    build_executive_kpis()
