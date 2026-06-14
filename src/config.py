"""
Central project configuration for NBA Revenue Intelligence.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"

SQL_DIR = ROOT_DIR / "sql"
SCHEMA_DIR = SQL_DIR / "schema"
ANALYTICS_SQL_DIR = SQL_DIR / "analytics"
TEST_SQL_DIR = SQL_DIR / "tests"

DOCS_DIR = ROOT_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "Images"

OUTPUT_DIR = ROOT_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"

DATABASE_PATH = PROCESSED_DIR / "nba_revenue_optimization.sqlite"

MODEL_DATASET_PATH = PROCESSED_DIR / "model_dataset.csv"
GAME_SEGMENTS_PATH = PROCESSED_DIR / "game_segments.csv"
REVENUE_FORECASTS_PATH = PROCESSED_DIR / "revenue_forecasts.csv"
EXECUTIVE_KPIS_PATH = PROCESSED_DIR / "executive_kpis.csv"
EXECUTIVE_RECOMMENDATIONS_PATH = PROCESSED_DIR / "executive_recommendations.csv"

for directory in [DATA_DIR, RAW_DIR, PROCESSED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)