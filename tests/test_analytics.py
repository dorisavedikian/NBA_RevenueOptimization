from src.config import (
    EXECUTIVE_KPIS_PATH,
    EXECUTIVE_RECOMMENDATIONS_PATH,
    GAME_SEGMENTS_PATH,
    MODEL_DATASET_PATH,
    REVENUE_FORECASTS_PATH,
)


def test_analytics_outputs_exist():
    assert MODEL_DATASET_PATH.exists()
    assert GAME_SEGMENTS_PATH.exists()
    assert REVENUE_FORECASTS_PATH.exists()
    assert EXECUTIVE_KPIS_PATH.exists()
    assert EXECUTIVE_RECOMMENDATIONS_PATH.exists()
