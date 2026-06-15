from src.config import SCHEMA_DIR


def test_schema_exists():
    assert (SCHEMA_DIR / "create_views.sql").exists()
