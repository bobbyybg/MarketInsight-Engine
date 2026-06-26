# Wall Street Terminal: System Architecture & Engineering Principles

This document defines the structural architecture, runtime behavior, domain boundaries, and design decisions of the `wall_street_terminal` SDK and its Streamlit presentation layer.

---

## 1. Core Engineering Principles

Future contributors must evaluate all code changes against these seven architectural invariants:

* **Deterministic Transformations:** Quantitative operations must be deterministic. Given identical inputs, pipeline functions must produce identical outputs. Internal implementations are authorized to mutate pipeline-owned DataFrames in-place to optimize memory efficiency, but must never alter external application state or global variables.
* **Quarantined Network I/O:** All external API communications are isolated within `data.py`. No other module is permitted to import network clients or execute HTTP requests.
* **Strict Domain Separation:** Financial mathematics (`quant.py`) must never import presentation libraries. Feature scaling and base-100 normalizations belong to `presentation.py`, while Plotly trace generation belongs strictly to `viz.py`.
* **No Financial Calculations in UI:** The view orchestrator (`ui/app.py`) executes zero financial math. Presentation-layer operations (metric selection routing, axis scaling strategies) are permitted, but analytical formulas belong strictly to quantitative modules.
* **Defensive Immutability:** External callers must treat `MarketFrame.prices` as read-only. Pipeline boundaries issue defensive copies, while internal stages mutate pipeline references to minimize heap allocation.
* **Framework-Level I/O Caching:** Remote API payloads must be cached at the framework boundary using Time-To-Live (TTL) expiration to prevent redundant network requests during UI interaction loops.
* **Single Responsibility Stages:** Every pipeline stage performs one distinct structural transformation (e.g., MultiIndex flattening is strictly separated from chronological resampling).

---

## 2. Repository Structure & Dependency Graph

```text
[ External Systems ]          [ Internal Library Modules ]
  Yahoo Finance API
         │
         ▼
     yfinance ──────────────► data.py (Acquisition Gateway)
                                 │
     pandas / numpy ────────► quant.py (Analytics Domain)
                                 │
     pandas ────────────────► presentation.py (Scaling Domain)
                                 │
     Plotly ────────────────► viz.py (Visualization Domain)
                                 │
     Streamlit ─────────────► ui/app.py (View Orchestrator)
                                 │
     pytest ────────────────► tests/ (Automated Verification)
```
## 3. End-to-End Execution & Error Flow
```text
                       [ User Interaction ]
                                │
                                ▼
                   [ Sidebar Configuration ]
                   (Tickers, Dates, Frequency)
                                │
                                ▼
                       { Input Validation }
                                │
                 ┌──────────────┴──────────────┐
            Valid Input                   Invalid Input
                 │                             │
                 ▼                             ▼
       [ fetch_raw_market_data ]       [ Halt & Render Error ]
                 │
                 ▼
         { Network Gateway }
                 │
     ┌───────────┴───────────┐
Success Payload        Network Failure / Empty
     │                       │
     ▼                       ▼
[ quant.structure ]   [ Populate Diagnostics ]
     │                       │
     ▼                       └────────► [ Sidebar Warning Toast ]
[ quant.resample ]
     │
     ▼
═══════════════════════════════════════════════════════════════
 ANALYTICS DOMAIN (quant.py)
───────────────────────────────────────────────────────────────
 [ quant.compute_log_returns ] ───► [ quant.extract_kpi_summary ]
═══════════════════════════════════════════════════════════════
     │
     ▼
═══════════════════════════════════════════════════════════════
 PRESENTATION DOMAIN (presentation.py & viz.py)
───────────────────────────────────────────────────────────────
                  ┌─────────┴─────────┐
                  ▼                   ▼
          [ Raw View Path ]   [ Base-100 View ]
                  │       (presentation.normalize)
                  │                   │
                  └─────────┬─────────┘
                            ▼
                  [ viz.generate_chart ]
═══════════════════════════════════════════════════════════════
                            │
                            ▼
                [ Render Streamlit Canvas ]
```
## 4. Runtime Lifecycle: The UI Loop
Streamlit executes scripts top-to-bottom on every user interaction. The architecture leverages this behavior to decouple state management from UI reactivity.
```text
─────────────────────────────────────────────────────────────────
 1. USER ACTION      ► User adjusts "Data Frequency" dropdown
 2. FRAMEWORK TRIGGER► Streamlit flushes local variables & reruns app.py
 3. I/O GATEWAY      ► fetch_raw_market_data() intercepted by @st.cache_data
 4. CACHE HIT        ► RAM returns raw DataFrame instantly (0ms network wait)
 5. DETERMINISTIC PIPELINE► quant/presentation functions execute sequentially
 6. CANVAS RENDER    ► Updated Plotly figure pushed to client WebSocket
─────────────────────────────────────────────────────────────────
```
## Cache Invalidation Rules

* **Hashing Mechanism:** The `@st.cache_data(ttl=300)` decorator hashes input arguments (`symbols`, `start_date`, `end_date`).
* **UI Interactivity:** Changing UI parameters (isolating metrics, switching chart types) triggers a fast rerun using cached RAM data.
* **Expiration Policy:** The cache expires strictly via the 300-second TTL. Upstream market data changes or vendor API updates do not proactively invalidate the cache.

---

## 5. Extensibility Matrix

```text
                       ┌─────────────────┐
                       │   MarketFrame   │
                       └────────┬────────┘
                                │
  ┌───────────┬───────────┼───────────┬───────────┬───────────┐
  ▼           ▼           ▼           ▼           ▼           ▼
[Indicators] [Risk]    [Factors]  [Portfolio] [Benchmarks] [Pricing]
 • SMA/EMA    • VaR     • Fama-    • Markowitz • CAPM Alpha • Black-Scholes
 • MACD       • CVaR      French   • Black-    • Beta       • Heston
 • RSI        • Drawdowns         Litterman  • Tracking   • Binomial Tree
```

---

## 6. Continuous Delivery & Quality Assurance

```text
[ Developer Commit ] ──► { Ruff Linting / Formatting } ──► [ GitHub Push ]
                                                                  │
                                                                  ▼
[ Approved Merge ] ◄── { Branch Protection } ◄── [ CI Actions Matrix ]
                                                   ├── Python 3.10 / 3.11 / 3.12
                                                   ├── Mypy Type Verification
                                                   ├── Pytest Regression Suite
                                                   └── Coverage Threshold (>=85%)
```

---

## 7. Architecture Decision Records (ADR)

### ADR-001: Streamlit Selected Over Dash
* **Context:** Need an interactive UI interface for institutional quant analytics.
* **Decision:** Use Streamlit.
* **Consequence:** Faster time-to-market and simpler state management, traded against fine-grained DOM layout control.

### ADR-002: Yahoo Finance Selected Over Polygon/Bloomberg
* **Context:** Need historical daily market data across global indices.
* **Decision:** Use `yfinance` wrapper.
* **Consequence:** Zero licensing costs for development/testing. API is unauthenticated and subject to rate limits; quarantined inside `data.py` for future swap-out.

### ADR-003: Pandas Selected Over Polars
* **Context:** Core dataframe memory engine selection.
* **Decision:** Standardize on Pandas 2.0+.
* **Consequence:** Maximum ecosystem compatibility with `yfinance`, `scipy`, and financial modeling libraries.

### ADR-004: Long-Form Relational Tables Selected Over Wide Tables
* **Context:** How to structure multi-asset price histories in memory.
* **Decision:** Use long-form tables (`Date`, `Ticker`, `Close`, `Volume`).
* **Consequence:** Native compatibility with Plotly Express grouping (`color='Ticker'`) and clean SQL-like aggregations.

### ADR-005: In-Place Mutation Allowed Inside Internal Pipelines
* **Context:** Passing large historical DataFrames through sequential transform functions.
* **Decision:** Allow internal pipeline functions to mutate DataFrame columns in-place.
* **Consequence:** Significantly reduces memory allocation overhead and Garbage Collection pauses during UI rerun loops. External API boundaries remain strictly read-only.
