"""
Runs the full NBA Revenue Intelligence pipeline.
"""

import subprocess
import sys

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
    print(f"\nRunning {step}...")
    result = subprocess.run([sys.executable, "-m", step])

    if result.returncode != 0:
        print(f"Pipeline failed at {step}")
        sys.exit(result.returncode)

print("\nNBA Revenue Intelligence pipeline completed successfully.")