"""
Purpose:
    Segment games into demand profiles using K-means clustering.

Inputs:
    data/processed/model_dataset.csv

Outputs:
    data/processed/game_segments.csv
    SQL table: game_segments
"""

import logging
import sqlite3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.config import (
    DATABASE_PATH,
    GAME_SEGMENTS_PATH,
    MODEL_DATASET_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


DB_PATH = DATABASE_PATH
INPUT_PATH = MODEL_DATASET_PATH
OUTPUT_PATH = GAME_SEGMENTS_PATH


FEATURES = [
    "opponent_strength",
    "is_weekend",
    "avg_ticket_price",
    "tickets_sold",
    "total_revenue",
    "sell_through_rate",
    "promotion_usage_rate",
    "purchase_rate",
    "cart_abandonment_rate",
]


def assign_segment_names(df):
    segment_summary = df.groupby("cluster").agg(
        avg_revenue=("total_revenue", "mean"),
        avg_sell_through=("sell_through_rate", "mean"),
        avg_price=("avg_ticket_price", "mean"),
        avg_promo=("promotion_usage_rate", "mean"),
        avg_abandonment=("cart_abandonment_rate", "mean"),
    )

    segment_names = {}

    revenue_median = segment_summary["avg_revenue"].median()
    sellthrough_median = segment_summary["avg_sell_through"].median()
    promo_median = segment_summary["avg_promo"].median()
    abandonment_median = segment_summary["avg_abandonment"].median()

    for cluster, row in segment_summary.iterrows():
        if (
            row["avg_revenue"] >= revenue_median
            and row["avg_sell_through"] >= sellthrough_median
        ):
            segment_names[cluster] = "Premium Demand"
        elif row["avg_promo"] >= promo_median:
            segment_names[cluster] = "Promotion Opportunity"
        elif (
            row["avg_abandonment"] >= abandonment_median
            or row["avg_sell_through"] < sellthrough_median
        ):
            segment_names[cluster] = "Inventory Risk"
        else:
            segment_names[cluster] = "Standard Demand"

    return segment_names


def assign_recommendations(segment_name):
    recommendations = {
        "Premium Demand": "Consider increasing prices for premium sections and releasing inventory earlier.",
        "Standard Demand": "Maintain current pricing strategy and monitor sales pace.",
        "Promotion Opportunity": "Use targeted discounts, family bundles, or student offers to increase conversion.",
        "Inventory Risk": "Increase marketing support, monitor checkout friction, and consider limited-time promotions.",
    }
    return recommendations.get(
        segment_name, "Monitor performance and review pricing strategy."
    )


def run_kmeans():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Model dataset not found. Run src/analytics/feature_engineering.py first."
        )

    df = pd.read_csv(INPUT_PATH)

    X = df[FEATURES].copy()
    X = X.fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    segment_names = assign_segment_names(df)
    df["segment_name"] = df["cluster"].map(segment_names)
    df["business_recommendation"] = df["segment_name"].apply(assign_recommendations)

    output_cols = [
        "game_id",
        "game_date",
        "opponent",
        "cluster",
        "segment_name",
        "business_recommendation",
        "total_revenue",
        "tickets_sold",
        "sell_through_rate",
        "avg_ticket_price",
        "promotion_usage_rate",
        "cart_abandonment_rate",
    ]

    segments = df[output_cols].copy()
    segments.to_csv(OUTPUT_PATH, index=False)

    with sqlite3.connect(DB_PATH) as conn:
        segments.to_sql("game_segments", conn, if_exists="replace", index=False)

    logger.info("K-means segmentation complete.")
    logger.info(f"Saved CSV to {OUTPUT_PATH}")
    logger.info("Saved SQL table: game_segments")
    logger.info("\nSegment counts:")
    logger.info(segments["segment_name"].value_counts())


if __name__ == "__main__":
    run_kmeans()
