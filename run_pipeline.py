"""
Runs the full NBA Revenue Intelligence pipeline.
"""

import subprocess
import sys

steps = [
    "src/simulation/ticket_sales.py",
    "src/etl/load.py",
    "src/warehouse/create_views.py",
    "src/analytics/feature_engineering.py",
    "src/models/kmeans.py",
    "src/models/regression.py",
    "src/warehouse/create_views.py",
]

for step in steps:
    print(f"\nRunning {step}...")
    result = subprocess.run([sys.executable, step])

    if result.returncode != 0:
        print(f"Pipeline failed at {step}")
        sys.exit(result.returncode)

print("\nNBA Revenue Intelligence pipeline completed successfully.")