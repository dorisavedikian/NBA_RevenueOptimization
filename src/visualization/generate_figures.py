"""
Generate portfolio-ready figures from analytics outputs.

Outputs:
    output/figures/revenue_by_opponent.png
    output/figures/forecast_vs_actual.png
    output/figures/game_segments.png
    output/figures/checkout_funnel.png
"""

import logging
import matplotlib.pyplot as plt
import pandas as pd
from src.config import (
    REVENUE_FORECASTS_PATH,
    EXECUTIVE_RECOMMENDATIONS_PATH,
    FIGURES_DIR,
    MODEL_DATASET_PATH,
)
from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def save_revenue_by_opponent(df: pd.DataFrame) -> None:
    revenue = (
        df.groupby("opponent", as_index=False)["total_revenue"]
        .sum()
        .sort_values("total_revenue", ascending=True)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(revenue["opponent"], revenue["total_revenue"])
    plt.title("Total Revenue by Opponent")
    plt.xlabel("Total Revenue")
    plt.ylabel("Opponent")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "revenue_by_opponent.png", dpi=200)
    plt.close()


def save_forecast_vs_actual(df: pd.DataFrame) -> None:
    if "predicted_revenue" not in df.columns:
        logger.warning("Skipping forecast_vs_actual.png; predicted_revenue missing.")
        return

    plt.figure(figsize=(8, 6))
    plt.scatter(df["total_revenue"], df["predicted_revenue"])
    plt.title("Forecast vs Actual Revenue")
    plt.xlabel("Actual Revenue")
    plt.ylabel("Predicted Revenue")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "forecast_vs_actual.png", dpi=200)
    plt.close()


def save_game_segments(df: pd.DataFrame) -> None:
    if "segment_name" not in df.columns:
        logger.warning("Skipping game_segments.png; segment_name missing.")
        return

    counts = df["segment_name"].value_counts().sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(counts.index, counts.values)
    plt.title("Games by Demand Segment")
    plt.xlabel("Number of Games")
    plt.ylabel("Segment")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "game_segments.png", dpi=200)
    plt.close()


def save_checkout_funnel(df: pd.DataFrame) -> None:
    funnel = {
        "Sessions": df["web_sessions"].sum(),
        "Cart Adds": df["cart_adds"].sum(),
        "Checkouts": df["checkouts"].sum(),
        "Purchases": df["web_purchases"].sum(),
    }

    plt.figure(figsize=(8, 6))
    plt.bar(funnel.keys(), funnel.values())
    plt.title("Ticket Purchase Funnel")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "checkout_funnel.png", dpi=200)
    plt.close()


def build_figure_dataset() -> pd.DataFrame:
    model_df = pd.read_csv(MODEL_DATASET_PATH)

    if EXECUTIVE_RECOMMENDATIONS_PATH.exists():
        rec_df = pd.read_csv(EXECUTIVE_RECOMMENDATIONS_PATH)
        keep_cols = ["game_id", "segment"]
        if all(col in rec_df.columns for col in keep_cols):
            rec_df = rec_df[keep_cols].rename(columns={"segment": "segment_name"})
            model_df = model_df.merge(rec_df, on="game_id", how="left")

    return model_df


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = build_figure_dataset()

    save_revenue_by_opponent(df)

    forecast_df = pd.read_csv(REVENUE_FORECASTS_PATH)
    save_forecast_vs_actual(forecast_df)

    save_game_segments(df)
    save_checkout_funnel(df)

    logger.info("Generated portfolio figures in %s", FIGURES_DIR)


if __name__ == "__main__":
    main()
