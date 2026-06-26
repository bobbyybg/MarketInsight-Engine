import pytest

from wall_street_terminal.quant import compute_log_returns, extract_kpi_summary


def test_compute_log_returns(sample_market_frame):
    res = compute_log_returns(sample_market_frame)
    assert "Log Returns" in res.prices.columns
    assert (
        pytest.approx(res.prices[res.prices["Ticker"] == "AAPL"]["Log Returns"].iloc[0]) is not None
    )


def test_extract_kpi_summary(sample_market_frame):
    kpis = extract_kpi_summary(sample_market_frame)
    assert "AAPL" in kpis
    assert "MSFT" in kpis

    expected_aapl_return = ((150.0 - 151.0) / 151.0) * 100
    assert kpis["AAPL"][0] == pytest.approx(expected_aapl_return)