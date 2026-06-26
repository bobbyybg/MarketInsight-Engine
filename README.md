# Wall Street Terminal

## Quickstart

Get your local environment up and running in less than two minutes:

```bash
# 1. Clone the repository and install in editable development mode
pip install -e .[dev]

# 2. Run the automated regression test matrix with coverage metrics
pytest --cov=wall_street_terminal tests/

# 3. Launch the terminal dashboard workspace
streamlit run src/wall_street_terminal/ui/app.py
```

---

## System Documentation

To understand the core design principles, runtime operations, or to contribute to this repository, consult the dedicated documentation trees:

* **System Architecture & ADRs:** In-depth overview of the core architectural invariants, framework caching mechanics, execution flows, and formal Architecture Decision Records.
* **Operations Runbook:** Step-by-step developer guide for local environment initialization, lint execution, static typing checks, and running testing infrastructure.

---

## Main Dependencies

> [!NOTE]
> Ensure your local Python environment satisfies these version requirements before initializing the installation script.

* **Pandas 2.0+** — High-performance vector execution engine.
* **Numpy** — Continuous numerical array allocations.
* **Plotly** — Low-latency, hardware-accelerated charting canvas.
* **Streamlit** — Dynamic UI reactive state management framework.
