import logging
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .types import MarketFrame, MarketMetadata

logger = logging.getLogger(__name__)


def structure_and_clean(raw_df: pd.DataFrame, metadata: MarketMetadata) -> MarketFrame:
    """Transforms raw multi-asset API payloads into structured relational tracks."""
    if raw_df.empty:
        return MarketFrame(
            prices=pd.DataFrame(), metadata=metadata, diagnostics=("No market data found.",)
        )

    structured_records: List[pd.DataFrame] = []
    logs: List[str] = []
    is_multi: bool = isinstance(raw_df.columns, pd.MultiIndex)

    for symbol in metadata.symbols:
        try:
            if is_multi:
                if (
                    symbol not in raw_df["Close"].columns
                    or raw_df["Close"][symbol].dropna().empty
                ):
                    logs.append(f"{symbol}: Excluded due to empty price series.")
                    continue
                ticker_df = pd.DataFrame(
                    {
                        "Open": raw_df["Open"][symbol],
                        "High": raw_df["High"][symbol],
                        "Low": raw_df["Low"][symbol],
                        "Close": raw_df["Close"][symbol],
                        "Volume": raw_df["Volume"][symbol],
                    }
                )
            else:
                ticker_df = raw_df[["Open", "High", "Low", "Close", "Volume"]].copy()

            ticker_df = ticker_df.dropna(subset=["Close"]).reset_index()
            ticker_df.rename(columns={ticker_df.columns[0]: "Date"}, inplace=True)
            ticker_df["Ticker"] = symbol
            structured_records.append(ticker_df)

        except Exception as e:
            logs.append(f"{symbol}: Structural cleanup breakdown ({str(e)}).")

    prices = pd.concat(structured_records, ignore_index=True) if structured_records else pd.DataFrame()
    return MarketFrame(prices=prices, metadata=metadata, diagnostics=tuple(logs))


def resample_market_frame(frame: MarketFrame, frequency: str) -> MarketFrame:
    """Chops and aggregates market dates aligned cleanly with financial reporting calendars."""
    if frame.is_empty or frequency == "Daily":
        return frame

    freq_map = {"Weekly": "W-FRI", "Monthly": "ME", "Yearly": "YE"}
    target_freq = freq_map.get(frequency, "W-FRI")

    resampled_groups: List[pd.DataFrame] = []
    for symbol, group in frame.prices.groupby("Ticker"):
        group = group.set_index("Date")
        agg_df = (
            group.resample(target_freq)
            .agg(
                {
                    "Open": "first",
                    "High": "max",
                    "Low": "min",
                    "Close": "last",
                    "Volume": "sum",
                }
            )
            .dropna(subset=["Close"])
            .reset_index()
        )
        agg_df["Ticker"] = symbol
        resampled_groups.append(agg_df)

    prices = pd.concat(resampled_groups, ignore_index=True) if resampled_groups else pd.DataFrame()
    new_meta = MarketMetadata(
        symbols=frame.metadata.symbols,
        frequency=frequency,
        start=frame.metadata.start,
        end=frame.metadata.end,
        benchmark_symbol=frame.metadata.benchmark_symbol,
    )
    return MarketFrame(prices=prices, metadata=new_meta, diagnostics=frame.diagnostics)


def compute_log_returns(frame: MarketFrame) -> MarketFrame:
    """Computes continuous log returns without internal python loops or lambdas."""
    if frame.is_empty:
        return frame

    df = frame.prices.copy()
    df.sort_values(["Ticker", "Date"], inplace=True)

    log_close = np.log(df["Close"])
    df["Log Returns"] = log_close.groupby(df["Ticker"]).diff()

    return MarketFrame(prices=df, metadata=frame.metadata, diagnostics=frame.diagnostics)


def extract_kpi_summary(frame: MarketFrame) -> Dict[str, Tuple[float, float]]:
    """Passes single-block aggregators through vector blocks to calculate performance metrics."""
    if frame.is_empty:
        return {}

    valid = frame.prices.dropna(subset=["Close"])
    if valid.empty:
        return {}

    firsts = valid.groupby("Ticker")["Close"].first()
    lasts = valid.groupby("Ticker")["Close"].last()
    returns = np.where(firsts != 0, ((lasts - firsts) / firsts) * 100, 0.0)

    return {
        str(ticker): (float(ret), float(last_val))
        for ticker, ret, last_val in zip(firsts.index, returns, lasts, strict=True)
    }