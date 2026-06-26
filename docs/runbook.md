# Operations Runbook: Development, Quality Assurance & Deployment

This operations manual provides step-by-step instructions for initializing, testing, and running the Wall Street Terminal source code locally.

---

## Step 1: Environment Initialization

The project uses a standard `src/` layout package schema managed via `pyproject.toml`. Follow these commands to isolate and build the environment:

```bash
# 1. Navigate to your local project directory root
cd wall-street-terminal

# 2. Allocate a clean Python virtual environment
python -m venv venv

# 3. Engage the isolated environment instance
# On macOS / Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# 4. Perform an editable installation including development dependencies
pip install -e .[dev]
```

---

## Step 2: Code Quality Control & Static Analysis

Before submitting pull requests or merging code, you must pass linting and static typing checks to satisfy CI gate requirements:

### 1. Code Quality Linting
We use Ruff to verify structural style conventions and identify code anomalies:

```bash
ruff check src/ tests/
```

### 2. Auto-Formatting Checks
Ensure that formatting adheres to the line-length standards (100 characters):

```bash
ruff format --check src/ tests/
```

### 3. Static Type Invariant Checks
Verify that parameter signatures align across application boundaries using Mypy:

```bash
mypy src/
```

---

## Step 3: Run Automated Regression Tests

The test suite validates data ingestion resilience, vectorized calculations, and edge cases (such as handling missing data points during normalization).

```bash
# Execute the suite and output a detailed statement coverage analysis report
pytest --cov=wall_street_terminal --cov-report=term-missing tests/
```

### Target Coverage Invariant
Any pull request dropping total system statement coverage below 85% will be automatically blocked by the GitHub Actions check runner.

---

## Step 4: Interface Deployment

Once quality controls pass successfully, launch the reactive presentation layer locally:

```bash
streamlit run src/wall_street_terminal/ui/app.py
```

The terminal interface will initialize, assign system logs directly to stdout, and automatically open your default browser tracking loop at `http://localhost:8501`.

---

## Phase 7: Automation Build Workflow (`.github/`)

Navigate to your **`.github/workflows/`** folder and save this final setup file.
