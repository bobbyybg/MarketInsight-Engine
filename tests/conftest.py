import datetime as dt

import pandas as pd
import pytest

from wall_street_terminal.types import MarketFrame, MarketMetadata


@pytest.fixture
def sample_market_metadata():
    return MarketMetadata(
        symbols=("AAPL", "MSFT"),
        frequency="Daily",
        start=dt.date(2025, 1, 1),
        end=dt.date(2025, 1, 5),
    )


@pytest.fixture
def sample_market_frame(sample_market_metadata):
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"] * 2),
            "Ticker": ["AAPL"] * 3 + ["MSFT"] * 3,
            "Open": [150.0, 152.0, 151.0, 300.0, 305.0, 302.0],
            "High": [153.0, 154.0, 152.0, 306.0, 308.0, 304.0],
            "Low": [149.0, 150.0, 148.0, 298.0, 300.0, 299.0],
            "Close": [151.0, 153.0, 150.0, 302.0, 304.0, 301.0],
            "Volume": [1000, 1100, 1050, 500, 600, 550],
        }
    )
    return MarketFrame(prices=df, metadata=sample_market_metadata)