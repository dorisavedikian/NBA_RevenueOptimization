"""
Purpose:
    Forecast ticket demand and revenue using regression models.

Inputs:
    data/processed/model_dataset.csv

Outputs:
    data/processed/revenue_forecasts.csv
    SQL table: revenue_forecasts
"""
import logging
import sqlite3

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.config import (
    DATABASE_PATH,
    MODEL_DATASET_PATH,
    REVENUE_FORECASTS_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

DB_PATH = DATABASE_PATH
INPUT_PATH = MODEL_DATASET_PATH
OUTPUT_PATH = REVENUE_FORECASTS_PATH


FEATURES = [
    "opponent_strength",
    "is_weekend",
    "avg_ticket_price",
    "promotion_usage_rate",
    "web_sessions",
    "cart_rate",
    "checkout_rate",
    "purchase_rate",
    "cart_abandonment_rate",
]

TARGET_DEMAND = "tickets_sold"
TARGET_REVENUE = "total_revenue"


def evaluate_model(model_name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return {
        "model": model_name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def train_best_model(X, y):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            max_depth=6,
        ),
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
    )

    results = []
    best_model = None
    best_score = float("inf")
    best_name = None

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        metrics = evaluate_model(name, y_test, predictions)
        results.append(metrics)

        if metrics["mae"] < best_score:
            best_score = metrics["mae"]
            best_model = model
            best_name = name

    return best_name, best_model, pd.DataFrame(results)


def run_forecasting():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            "Model dataset not found. Run src/analytics/feature_engineering.py first."
        )

    df = pd.read_csv(INPUT_PATH)

    X = df[FEATURES].fillna(0)

    demand_model_name, demand_model, demand_metrics = train_best_model(
        X,
        df[TARGET_DEMAND],
    )

    revenue_model_name, revenue_model, revenue_metrics = train_best_model(
        X,
        df[TARGET_REVENUE],
    )

    df["predicted_tickets_sold"] = demand_model.predict(X)
    df["predicted_revenue"] = revenue_model.predict(X)

    df["ticket_forecast_error"] = df["tickets_sold"] - df["predicted_tickets_sold"]
    df["revenue_forecast_error"] = df["total_revenue"] - df["predicted_revenue"]

    df["sellout_probability"] = np.clip(
        df["predicted_tickets_sold"] / df["arena_capacity"], 0, 1
    )

    forecasts = df[
        [
            "game_id",
            "game_date",
            "opponent",
            "tickets_sold",
            "predicted_tickets_sold",
            "ticket_forecast_error",
            "total_revenue",
            "predicted_revenue",
            "revenue_forecast_error",
            "sellout_probability",
        ]
    ].copy()

    forecasts.to_csv(OUTPUT_PATH, index=False)

    with sqlite3.connect(DB_PATH) as conn:
        forecasts.to_sql("revenue_forecasts", conn, if_exists="replace", index=False)
        demand_metrics.to_sql(
            "model_metrics_demand", conn, if_exists="replace", index=False
        )
        revenue_metrics.to_sql(
            "model_metrics_revenue", conn, if_exists="replace", index=False
        )

    logger.info("Regression forecasting complete.")
    logger.info(f"Demand model selected: {demand_model_name}")
    logger.info(f"Revenue model selected: {revenue_model_name}")
    logger.info(f"Saved forecasts to {OUTPUT_PATH}")
    logger.info(
        "Saved SQL tables: revenue_forecasts, model_metrics_demand, model_metrics_revenue"
    )

    logger.info("\nDemand model metrics:")
    logger.info(demand_metrics)

    logger.info("\nRevenue model metrics:")
    logger.info(revenue_metrics)


if __name__ == "__main__":
    run_forecasting()
