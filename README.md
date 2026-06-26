# Wall Street Terminal

*A quantitative market analytics workspace built with Python, Pandas, Plotly, and Streamlit.*


Wall Street Terminal is an interactive quantitative market analytics workspace built with Python. It provides tools for exploring historical market data, comparing multiple assets, and visualizing financial metrics through an interactive dashboard.

The long-term goal of the project is to evolve beyond a market dashboard into a modular quantitative finance toolkit covering portfolio analytics, market risk, derivatives pricing, and financial engineering.

> **Work in Progress:** This project is actively developed as a long-term quantitative finance portfolio. New analytics, pricing models, and risk management features will continue to be added.


---

## Why I Built This

Most beginner finance dashboards stop at plotting stock prices.

The goal of this project is different:

* build a reusable quantitative analytics platform,
* practice production-quality Python engineering,
* implement financial models from first principles,
* and create a portfolio project that can continuously grow as I learn more quantitative finance.

---

## Technology Stack

### Core

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- yfinance

### Development

- Pytest
- Ruff
- Hatch

---
## Architecture

The application follows a modular architecture separating:

- Data acquisition
- Quantitative analytics
- Visualization
- User interface

Detailed design documentation is available in `docs/architecture.md`.

---
## Project Structure

```text
src/
└── wall_street_terminal/
    ├── data.py        # Data acquisition
    ├── quant.py       # Financial calculations
    ├── viz.py         # Visualization
    ├── types.py       # Shared data structures
    └── ui/
        └── app.py     # Streamlit interface
```

Additional documentation is available in the `docs/` directory.

---

## Running the Project

```bash
git clone https://github.com/bobbyybg/MarketInsight-Engine.git
cd MarketInsight-Engine

pip install -e .

streamlit run src/wall_street_terminal/ui/app.py
```

---

## Current Features

- [x] Historical market data
- [x] Interactive dashboard
- [x] Multi-asset comparison
- [x] Log returns
- [x] Base-100 normalization
- [x] Performance KPI cards
- [x] Multiple resampling frequencies
- [x] Interactive Plotly visualizations

## Planned Features

### Risk Analytics
- [ ] Rolling volatility
- [ ] Sharpe Ratio
- [ ] Sortino Ratio
- [ ] Maximum Drawdown
- [ ] Value at Risk (VaR)
- [ ] Conditional VaR (CVaR)

### Portfolio Analytics
- [ ] Correlation matrix
- [ ] Beta
- [ ] CAPM
- [ ] Efficient Frontier
- [ ] Portfolio Optimization

### Derivatives
- [ ] Black-Scholes option pricing
- [ ] Greeks calculator
- [ ] Binomial Tree pricing

### Simulation
- [ ] Monte Carlo portfolio simulation
- [ ] Geometric Brownian Motion

### Fixed Income
- [ ] Bond pricing
- [ ] Duration
- [ ] Convexity

---

## Usage


You're welcome to:

- Clone the repository
- Run it locally
- Modify it for your own learning
- Share feedback or suggestions

> [!IMPORTANT]
> **Portfolio Usage Notice**
>
> This repository is shared for learning, experimentation, and technical review.
>
> Please do **not** present this project, or substantially similar derivatives, as your own work for academic submissions, employment applications, or portfolio purposes without clear attribution to the original repository.


## Copyright

Copyright © 2026 bobbyybg.

This project is published as a portfolio and learning resource. All rights are reserved.

Please refer to the **Portfolio Usage Notice** above regarding acceptable use.