import datetime
import logging
import sys
from typing import List

import pandas as pd
from packaging.version import parse
import streamlit as st

from wall_street_terminal.data import fetch_raw_market_data
from wall_street_terminal.presentation import normalize_base_100
from wall_street_terminal.quant import (
    compute_log_returns,
    extract_kpi_summary,
    resample_market_frame,
    structure_and_clean,
)
from wall_street_terminal.types import MarketMetadata
from wall_street_terminal.viz import generate_terminal_chart

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
STREAMLIT_SUPPORTS_SELECTION = parse(st.__version__) >= parse("1.35.0")

st.set_page_config(page_title="Institutional Analytics Terminal", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body, [data-testid="stAppViewContainer"], .main { font-family: 'Inter', sans-serif !important; background-color: #0B0E11 !important; color: #F8F9FA !important; }
        [data-testid="stSidebar"] { background-color: #141821 !important; border-right: 1px solid #242B3D; }
        h1 { font-weight: 800 !important; color: #FFFFFF !important; border-bottom: 2px solid #00A651; padding-bottom: 10px; }
        h3 { font-weight: 600 !important; color: #E4E7EB !important; }
        .stDataFrame, div[data-testid="stTable"] { border: 1px solid #242B3D !important; background-color: #11151F !important; }
        .info-banner { background-color: #141821 !important; color: #FFFFFF !important; padding: 12px 20px; border: 1px solid #242B3D; border-left: 4px solid #00FFFF; font-weight: 600; margin-top: 10px; font-size: 14px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Financial Analytics Terminal")

st.sidebar.markdown("### System Parameters")
ticker_raw = st.sidebar.text_input("Ticker Symbols", value="^FCHI, ^GSPC, ^NSEI")
tickers: List[str] = [t.strip().upper() for t in ticker_raw.split(",") if t.strip()]

if not tickers:
    st.sidebar.error("Input Error: Please provide at least one valid ticker symbol.")
    st.stop()

min_date = datetime.date(2005, 1, 1)
max_date = datetime.date.today()
one_year_ago = max_date - datetime.timedelta(days=365)

col_start, col_end = st.sidebar.columns(2)
with col_start:
    start_date = st.date_input(
        "Start Date", value=one_year_ago, min_value=min_date, max_value=max_date
    )
with col_end:
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

if start_date >= end_date:
    st.error("Timeline Error: Start Date must precede End Date.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### Display Preferences")
frequency = st.sidebar.selectbox("Data Frequency", ["Daily", "Weekly", "Monthly", "Yearly"])
metric_to_isolate = st.sidebar.selectbox(
    "Isolate Metric", ["Close", "Open", "High", "Low", "Volume", "Log Returns"]
)
plot_type = st.sidebar.radio("Chart Layout", ["Time Series (Line)", "Bar Plot"], horizontal=True)
scaling_mode = st.sidebar.radio(
    "Axis Scaling Strategy",
    ["Standard (Raw Values)", "Logarithmic Scale", "Normalized (Base 100)"],
)

metadata = MarketMetadata(
    symbols=tuple(tickers), frequency=frequency, start=start_date, end=end_date
)
raw_payload = fetch_raw_market_data(metadata.symbols, str(start_date), str(end_date))

frame = structure_and_clean(raw_payload, metadata)
frame = resample_market_frame(frame, frequency)
frame = compute_log_returns(frame)
frame = normalize_base_100(frame)

for log_msg in frame.diagnostics:
    st.sidebar.warning(log_msg)

st.write("---")

if not frame.is_empty:
    kpis = extract_kpi_summary(frame)
    st.subheader("Window Performance Summary")
    kpi_cols = st.columns(len(tickers))

    for idx, symbol in enumerate(tickers):
        if symbol in kpis:
            ret, last_close = kpis[symbol]
            color_hex = "#00A651" if ret >= 0 else "#E03A3E"
            with kpi_cols[idx]:
                st.markdown(
                    f"""
                    <div style="background-color: #141821; padding: 15px; border-radius: 4px; border-left: 4px solid {color_hex};">
                        <span style="font-size: 12px; color: #8A93A6; font-weight: 600; text-transform: uppercase;">{symbol} Total Return</span>
                        <h2 style="margin: 5px 0 0 0; color: {color_hex}; font-weight: 800; font-size: 26px;">{ret:+.2f}%</h2>
                        <span style="font-size: 12px; color: #F8F9FA;">Last Close: {last_close:,.2f}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

    st.write("---")

    target_metric = (
        f"{metric_to_isolate}_Normalized"
        if (
            scaling_mode == "Normalized (Base 100)"
            and metric_to_isolate in ["Close", "Open", "High", "Low"]
        )
        else metric_to_isolate
    )

    if target_metric in frame.prices.columns:
        pivot_df = frame.prices.pivot(
            index="Date", columns="Ticker", values=target_metric
        ).reset_index()

        st.subheader(f"Market Workspace: {metric_to_isolate} Comparison")
        info_placeholder = st.empty()

        banner_msg = (
            "✨ CLICK ANY TRACK TRACE LINE TO ENGAGE TARGET FOCUS CAPTURE INSPECTOR"
            if STREAMLIT_SUPPORTS_SELECTION
            else "⚡ UPGRADE STREAMLIT PAST v1.35 TO ENABLE OUTSIDE FOCUS RERUN CAPTURES"
        )
        info_placeholder.markdown(
            f'<div class="info-banner">{banner_msg}</div>', unsafe_allow_html=True
        )

        chart_kwargs = {"width": "stretch", "config": {"displayModeBar": False}}
        if STREAMLIT_SUPPORTS_SELECTION:
            chart_kwargs["on_select"] = "rerun"

        fig = generate_terminal_chart(frame.prices, target_metric, plot_type)
        if scaling_mode == "Logarithmic Scale" and metric_to_isolate != "Log Returns":
            fig.update_layout(yaxis_type="log")

        chart_event = st.plotly_chart(fig, **chart_kwargs)

        if (
            STREAMLIT_SUPPORTS_SELECTION
            and isinstance(chart_event, dict)
            and "selection" in chart_event
        ):
            points = chart_event["selection"].get("points", [])
            if points:
                pt = points[0]
                val = pt.get("y", 0.0)
                ticker_tag = pt.get("customdata", "Asset")
                raw_x = pt.get("x", "N/A")
                dt_str = (
                    pd.to_datetime(raw_x, unit="ms").strftime("%Y-%m-%d")
                    if isinstance(raw_x, (int, float))
                    else str(raw_x)[:10]
                )

                info_placeholder.markdown(
                    f'<div class="info-banner">📊 LOCKED FOCUS: <span style="color: #00FF66;">{ticker_tag}</span> | '
                    f'DATE: <span style="color: #00FFFF;">{dt_str}</span> | '
                    f'VALUE: <span style="color: #FFFF33;">{val:,.2f}</span></div>',
                    unsafe_allow_html=True,
                )

        st.subheader("Core Data Matrices")
        tab1, tab2 = st.tabs(["Isolated Pivot Matrix", "Full Stacked Records"])
        with tab1:
            st.dataframe(pivot_df.set_index("Date"), width="stretch")
        with tab2:
            st.dataframe(frame.prices, width="stretch")
else:
    st.error("System Gateway Offline. No executable market tracks compiled.")