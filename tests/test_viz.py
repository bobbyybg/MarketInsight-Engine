import numpy as np
import pandas as pd
import pytest

from wall_street_terminal.presentation import normalize_base_100
from wall_street_terminal.types import MarketFrame


def test_normalize_base_100_handles_nans(sample_market_metadata):
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
            "Ticker": ["XYZ"] * 3,
            "Open": [np.nan, 10.0, 20.0],
            "High": [np.nan, 15.0, 25.0],
            "Low": [np.nan, 5.0, 15.0],
            "Close": [np.nan, 12.0, 24.0],
        }
    )
    frame = MarketFrame(prices=df, metadata=sample_market_metadata)
    normalized = normalize_base_100(frame)

    assert np.isnan(normalized.prices["Close_Normalized"].iloc[0])
    assert normalized.prices["Close_Normalized"].iloc[1] == pytest.approx(100.0)
    assert normalized.prices["Close_Normalized"].iloc[2] == pytest.approx(200.0)