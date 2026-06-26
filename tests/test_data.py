import pandas as pd

from wall_street_terminal.data import fetch_raw_market_data


def test_fetch_raw_market_data_empty_input():
    res = fetch_raw_market_data((), "2025-01-01", "2025-01-05")
    assert isinstance(res, pd.DataFrame)
    assert res.empty