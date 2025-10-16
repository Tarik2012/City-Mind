# 🧠 CityMind Project

CityMind is a data science project designed to analyze health indicators and social determinants using the **CDC PLACES 2024 dataset**.  
It predicts *mental health and depression prevalence* across US counties through structured machine learning pipelines.

---

## 🌍 Overview

The project consists of the following core modules:

| Module | Description |
|--------|--------------|
| **Data Wrangling** | Cleans, transforms, and prepares raw CDC data |
| **Feature Selection** | Selects best predictors for mental health and depression |
| **Model Training** | Trains ML models on “No Social” and “Full Social” scenarios |
| **Results Comparison** | Compares model performance between both scenarios |
| **Testing** | Validates all steps automatically with `pytest` |
| **Automation** | Full workflow orchestrated via `Snakemake` |

---

## 📂 Project Structure

```
CityMind/
│
├── data/
│   ├── raw/                 # Raw CDC datasets
│   ├── processed/           # Cleaned data ready for modeling
│   ├── interim/             # Intermediate model outputs and comparisons
│
├── scripts/
│   ├── common/              # Shared scripts (e.g., wrangling)
│   ├── no_social/           # Training without social features
│   ├── full_social/         # Training including social features
│   ├── comparison/          # Model comparison & visualization
│
├── tests/                   # Automated pytest validations
├── logs/                    # Execution logs
├── Snakefile                # Snakemake pipeline definition
└── README_PIPELINE.md       # Pipeline documentation
```

---

## ⚙️ Setup Instructions

### 1. Create and activate environment
```bash
python -m venv env
env\Scripts\activate      # Windows
source env/bin/activate     # macOS/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the full automated pipeline
```bash
snakemake --cores 1 --latency-wait 15 -p
```

---

## 📊 Outputs

| Output | Description |
|--------|--------------|
| `data/interim/no_social/model_metrics.csv` | Model metrics without social features |
| `data/interim/full_social/model_metrics.csv` | Model metrics with social features |
| `data/interim/comparison/comparison_summary.csv` | R² / RMSE / MAE comparison table |
| `data/interim/comparison/r2_comparison.png` | Visual comparison of model performance |

---

## 🧩 Key Technologies

- **Python 3.13+**
- **Pandas**, **NumPy**, **Scikit-learn**, **XGBoost**
- **Snakemake** for workflow automation
- **Pytest** for testing
- **Matplotlib** for visualization
- **MLflow / DVC** (optional future integration)

---

## 🧪 Testing

Run all tests manually with:
```bash
pytest -v
```
Logs are stored in `logs/pytest_output.log`.

---

## 🧠 Author
**Erik R. (CityMind Project)**  
MIT License © 2025

---
