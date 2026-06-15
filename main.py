"""
Runs the full NBA Revenue Intelligence pipeline.
"""
import logging
import subprocess
import sys

from src.utils.logger import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

steps = [
    "src.simulation.ticket_sales",
    "src.etl.load",
    "src.warehouse.create_views",
    "src.analytics.feature_engineering",
    "src.models.kmeans",
    "src.models.regression",
    "src.analytics.kpi_engine",
    "src.analytics.recommendation_engine",
    "src.warehouse.create_views",
]

for step in steps:
    logger.info(f"\nRunning {step}...")
    result = subprocess.run([sys.executable, "-m", step])

    if result.returncode != 0:
        logger.error(f"Pipeline failed at {step}")
        sys.exit(result.returncode)

logger.info("\nNBA Revenue Intelligence pipeline completed successfully.")
