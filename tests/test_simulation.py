from src.config import (
    DIM_GAMES_PATH,
    DIM_CUSTOMERS_PATH,
    DIM_SECTIONS_PATH,
    DIM_PROMOTIONS_PATH,
    FACT_TICKET_TRANSACTIONS_PATH,
    FACT_WEB_SESSIONS_PATH,
)


def test_simulation_outputs_exist():
    assert DIM_GAMES_PATH.exists()
    assert DIM_CUSTOMERS_PATH.exists()
    assert DIM_SECTIONS_PATH.exists()
    assert DIM_PROMOTIONS_PATH.exists()
    assert FACT_TICKET_TRANSACTIONS_PATH.exists()
    assert FACT_WEB_SESSIONS_PATH.exists()
