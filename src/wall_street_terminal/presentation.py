import numpy as np
import pandas as pd

from .types import MarketFrame


def normalize_base_100(frame: MarketFrame) -> MarketFrame:
    """Presentation layer logic mapping price elements to a normalized baseline scale."""
    if frame.is_empty:
        return frame

    df = frame.prices.copy()
    for col in ["Close", "Open", "High", "Low"]:

        def _safe_scale(series: pd.Series) -> pd.Series:
            valid_obs = series.dropna()
            if valid_obs.empty or valid_obs.iloc[0] == 0:
                return pd.Series(np.nan, index=series.index)
            return (series / valid_obs.iloc[0]) * 100

        df[f"{col}_Normalized"] = df.groupby("Ticker")[col].transform(_safe_scale)

    return MarketFrame(prices=df, metadata=frame.metadata, diagnostics=frame.diagnostics)