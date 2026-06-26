import logging
from typing import Tuple

import pandas as pd
import streamlit as st
import yfinance as yf

logger = logging.getLogger(__name__)


@st.cache_data(ttl=300)
def fetch_raw_market_data(symbols: Tuple[str, ...], start_date: str, end_date: str) -> pd.DataFrame:
    """Pure data acquisition gateway. Returns an empty DataFrame on failure instead of None."""
    if not symbols:
        return pd.DataFrame()

    try:
        df: pd.DataFrame = yf.download(
            tickers=list(symbols),
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
            group_by="column",
        )
        if df.empty:
            logger.warning("API returned empty dataframe payload.")
            return pd.DataFrame()

        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df
    except Exception as e:
        logger.error(f"Network Gateway Failure: {str(e)}")
        return pd.DataFrame()