## CityMind — Copilot / AI contributor instructions

This file gives focused, actionable guidance for an AI coding assistant to be immediately productive in this repository.

- Project type: data-science + small Django API. Key roots: `data/`, `scripts/`, `mlruns/`, `tests/`, and the Django app (`manage.py`, `citymind/`, `api/`, `core/`).

- High-level architecture and data flow
  - Raw CDC data lives in `data/raw/`. Data wrangling produces `data/processed/*` then model inputs `data/processed/{no_social,full_social}`.
  - Scripts in `scripts/` perform wrangling, training and comparisons. Example: `scripts/full_social/04_train_models_full_social.py` reads `data/processed/full_social/model_data_{target}.csv` and writes outputs to `data/interim/full_social/` (e.g. `model_metrics.csv`, `rf_importances_{target}.csv`).
  - A Snakemake pipeline (`Snakefile`) orchestrates end-to-end runs. Prefer to update Snakemake rules when adding new pipeline steps.
  - MLflow experiments are stored under `mlruns/` and scripts may import `scripts/common/11_mlflow_tracking.py` (look for `CityMindTracker` usages).

- Developer workflows (commands you can run from repo root)
  - Create/activate venv (Windows PowerShell): `python -m venv env` then `.\env\Scripts\Activate.ps1` or `.\env\Scripts\Activate.ps1` if the repo already includes `env/`.
  - Install deps: `pip install -r requirements.txt` (Python 3.13+ per README).
  - Run full pipeline: `snakemake --cores 1 --latency-wait 15 -p` (see `README_PIPELINE.md` for details).
  - Run a training script (example):
    - Ensure repo root is working directory and env activated.
    - `python scripts/full_social/04_train_models_full_social.py` — script expects preprocessed CSVs in `data/processed/full_social` and will save metrics into `data/interim/full_social`.
  - Run tests: `pytest -q` (tests live in `tests/`, `conftest.py` available). Test files include `test_model_training.py`, `test_wrangling.py`, and `test_compare_results.py`.
  - Django API (development): `python manage.py runserver`. Project settings live in `citymind/settings.py`. API app code is under `api/` and `core/`.

- Project-specific conventions and patterns
  - Scripts assume you run them from repository root. Prefer relative paths already used (e.g. `Path("data/processed/full_social")`).
  - Models training scripts often follow a pattern: read `model_data_{target}.csv`, dropna on target, split, scale, optionally PCA, train models (LassoCV, RandomForest, XGBoost), save metrics to `data/interim/*` and RF feature importances to `data/interim/*`.
  - When adding or changing scripts, keep outputs under `data/interim/` and avoid changing `data/raw/` in-place.
  - MLflow integration: some scripts optional-import `scripts/common/11_mlflow_tracking.py`. If present, log via `CityMindTracker()`; otherwise scripts continue without MLflow. Look for `try: importlib.util.spec_from_file_location(...)` pattern.

- Integration points & dependencies to be aware of
  - External libs: scikit-learn, xgboost, pandas, numpy, matplotlib, snakemake, mlflow (optional). See `requirements.txt` for exact pins.
  - Local integration: `scripts/common/` contains shared utilities and MLflow helpers — changing its API requires updating all scripts that import it.
  - Persistent artifacts: `mlruns/` (MLflow), `data/interim/`, and `logs/` can grow large; avoid committing generated large artifacts.

- Code patterns/examples (search for these when editing):
  - Model data naming: `model_data_{target}.csv` (e.g. `model_data_depression_crudeprev.csv`) — used by training scripts in `scripts/no_social` and `scripts/full_social`.
  - MLflow loader pattern: `spec = importlib.util.spec_from_file_location("mlflow_tracker", pathlib.Path("scripts/common/11_mlflow_tracking.py"))`.
  - Output conventions: metrics CSVs in `data/interim/*`, importance files named `rf_importances_{target}.csv`.

- When proposing changes, prioritize:
  1. No breaking changes to Snakemake rules — update `Snakefile` first for pipeline steps.
  2. Keep data file naming stable (`model_data_{target}.csv`) or add backward-compatible loaders.
  3. Keep MLflow optional — preserve try/except import style used across scripts.

- Quick checks an AI should run before editing code
  - Confirm tests pass locally: `pytest -q` (use minimal affected test selection when possible).
  - Verify script input paths exist (e.g. `data/processed/full_social/model_data_depression_crudeprev.csv`). If absent, do not hard-fail — suggest data generation step (Snakemake) instead.

If anything here is unclear or you'd like more details (examples for editing `Snakefile`, MLflow contract, or test harness examples), tell me which section to expand.
