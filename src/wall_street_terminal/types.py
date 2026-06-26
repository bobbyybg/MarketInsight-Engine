from dataclasses import dataclass, field
import datetime as dt
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class MarketMetadata:
    symbols: tuple[str, ...]
    frequency: str
    start: dt.date
    end: dt.date
    benchmark_symbol: Optional[str] = None
    timezone: str = "UTC"
    adjusted: bool = True


@dataclass(frozen=True)
class MarketFrame:
    """Shallowly frozen container holding market prices, metadata structures, and logs.

    IMMUTABILITY & PERFORMANCE CONTRACT:
    The container class is explicitly frozen. The contained Pandas DataFrame is
    mutable and must be treated as immutable by convention by external callers.
    Internal pipeline functions may selectively mutate DataFrame columns in-place
    to reduce redundant memory allocations during high-frequency transformations.
    """

    prices: pd.DataFrame
    metadata: MarketMetadata
    diagnostics: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_empty(self) -> bool:
        return self.prices.empty