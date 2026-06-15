from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
EXTERNAL_DIR = DATA_DIR / "external"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
ANALYTICS_DIR = DATA_DIR / "analytics"

SQL_DIR = ROOT_DIR / "sql"
SCHEMA_DIR = SQL_DIR / "schema"
ANALYTICS_SQL_DIR = SQL_DIR / "analytics"
TEST_SQL_DIR = SQL_DIR / "tests"

DOCS_DIR = ROOT_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"

OUTPUT_DIR = ROOT_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"

DATABASE_PATH = WAREHOUSE_DIR / "nba_revenue_optimization.sqlite"

DIM_GAMES_PATH = WAREHOUSE_DIR / "dim_games.csv"
DIM_CUSTOMERS_PATH = WAREHOUSE_DIR / "dim_customers.csv"
DIM_SECTIONS_PATH = WAREHOUSE_DIR / "dim_sections.csv"
DIM_PROMOTIONS_PATH = WAREHOUSE_DIR / "dim_promotions.csv"
FACT_TICKET_TRANSACTIONS_PATH = WAREHOUSE_DIR / "fact_ticket_transactions.csv"
FACT_WEB_SESSIONS_PATH = WAREHOUSE_DIR / "fact_web_sessions.csv"

MODEL_DATASET_PATH = ANALYTICS_DIR / "model_dataset.csv"
GAME_SEGMENTS_PATH = ANALYTICS_DIR / "game_segments.csv"
REVENUE_FORECASTS_PATH = ANALYTICS_DIR / "revenue_forecasts.csv"
EXECUTIVE_KPIS_PATH = ANALYTICS_DIR / "executive_kpis.csv"
EXECUTIVE_RECOMMENDATIONS_PATH = ANALYTICS_DIR / "executive_recommendations.csv"

for directory in [
    DATA_DIR,
    RAW_DIR,
    EXTERNAL_DIR,
    WAREHOUSE_DIR,
    ANALYTICS_DIR,
    SQL_DIR,
    SCHEMA_DIR,
    ANALYTICS_SQL_DIR,
    TEST_SQL_DIR,
    DOCS_DIR,
    IMAGES_DIR,
    OUTPUT_DIR,
    FIGURES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
