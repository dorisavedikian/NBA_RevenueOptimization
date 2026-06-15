from src.config import ANALYTICS_SQL_DIR


def test_sql_queries_exist():
    files = list(ANALYTICS_SQL_DIR.glob("*.sql"))

    assert len(files) >= 10
