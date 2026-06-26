"""Wall Street Terminal core library interface initialization."""

from .data import fetch_raw_market_data
from .presentation import normalize_base_100
from .quant import (
    compute_log_returns,
    extract_kpi_summary,
    resample_market_frame,
    structure_and_clean,
)
from .types import MarketFrame, MarketMetadata
from .viz import generate_terminal_chart

__all__ = [
    "MarketFrame",
    "MarketMetadata",
    "fetch_raw_market_data",
    "structure_and_clean",
    "resample_market_frame",
    "compute_log_returns",
    "extract_kpi_summary",
    "normalize_base_100",
    "generate_terminal_chart",
]