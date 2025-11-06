# 🧠 CityMind Project — AI-Powered Mental Health Insights

CityMind is a full data science + backend project that analyzes **mental health and depression prevalence** across US counties  
using the **CDC PLACES 2024 dataset**.  

It integrates a complete ML pipeline (Snakemake) with a **Django REST API** that delivers real-time predictions  
based on summarized socio-health indicators.

---

## 🌍 Overview

The system predicts two main health targets:

| Target | Description |
|--------|--------------|
| `mhlth_crudeprev` | Poor mental health prevalence |
| `depression_crudeprev` | Depression prevalence |

Each is trained in two parallel scenarios:
- 🧩 **No Social** → only health + demographic features  
- 🌐 **Full Social** → includes social, economic, and environmental features  

➡️ Result: **4 XGBoost models** (`no_social` + `full_social` × 2 targets)

---

## 🧱 Core Architecture

| Module | Description |
|--------|--------------|
| **Django Backend (`core`, `api`)** | ORM models, REST endpoints, and PostgreSQL integration |
| **ML Pipeline (Snakemake)** | Wrangling → Training → Comparison → Testing → Ingestion |
| **Scripts** | Modular scripts for wrangling, training, and result comparison |
| **Database Integration** | Automated data ingestion via Django ORM |

---

## 📂 Project Structure

```
CityMind/
│
├── core/                    # Django models, admin, and ORM logic
├── api/                     # Django REST API (PredictView, serializers, URLs)
│
├── scripts/
│   ├── common/              # Shared preprocessing scripts (wrangling, monitoring, feature expansion)
│   ├── no_social/           # Model training without social indicators
│   ├── full_social/         # Model training including social indicators
│   ├── comparison/          # Model comparison and visualization
│   ├── db_ingest/           # ORM-based ingestion into PostgreSQL
│
├── data/
│   ├── raw/                 # CDC PLACES input data
│   ├── processed/           # Clean data ready for ML
│   ├── interim/             # Model metrics and comparison summaries
│
├── models/                  # Trained models (.joblib)
├── logs/                    # Pipeline and API logs
├── tests/                   # Pytest validations
├── Snakefile                # Main Snakemake automation file
├── requirements.txt
├── manage.py
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Create environment
```bash
python -m venv env
env\Scripts\activate          # Windows
# or
source env/bin/activate       # macOS/Linux
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run migrations (PostgreSQL)
```bash
python manage.py migrate
```

### 4️⃣ Launch the backend
```bash
python manage.py runserver
```

Visit the API at:  
👉 **http://127.0.0.1:8000/api/predict/**

---

## 🔮 Prediction API (Example)

### POST `/api/predict/`
Send a JSON body with 8–9 summarized socio-health indicators:

```json
{
  "health_index": 0.25,
  "social_index": -0.15,
  "economy_index": 0.45,
  "environment_index": 0.35,
  "education_index": 0.10,
  "population": 125000,
  "unemployment": 0.06,
  "urbanization": 0.78,
  "safety_index": 0.5,
  "target": "depression_crudeprev",
  "use_social": true
}
```

### ✅ Response
```json
{
  "id": 1,
  "model_used": "models/xgboost_full_social_depression.joblib",
  "target": "depression_crudeprev",
  "predicted_value": 19.78,
  "input_vector": { ... },
  "prediction_date": "2025-10-30T19:04:47.99Z"
}
```

> 💡 Internally, `expand_features()` translates the summarized input into  
> 41–45 real features expected by each XGBoost model.

---

## 📊 ML Pipeline Execution

Run the **entire project workflow** via Snakemake:

```bash
snakemake -p --cores 1 --latency-wait 10
```

This executes:
1. 🧹 Data Wrangling  
2. 🧠 Model Training (No Social + Full Social)  
3. 📈 Results Comparison  
4. 🧪 Pytest Validation  
5. 🗃️ ORM Database Ingestion  

---

## 📦 Outputs

| File | Description |
|------|-------------|
| `data/interim/no_social/model_metrics.csv` | Model performance (no social) |
| `data/interim/full_social/model_metrics.csv` | Model performance (full social) |
| `data/interim/comparison/comparison_summary.csv` | Summary of R², MAE, RMSE |
| `data/interim/comparison/r2_comparison.png` | R² improvement visualization |
| `logs/db_ingest_done.txt` | Pipeline success marker |

---

## 🧩 Technologies Used

| Category | Stack |
|-----------|--------|
| **ML / Data** | XGBoost, Scikit-learn, Pandas, NumPy |
| **Backend** | Django 5 + Django REST Framework |
| **Orchestration** | Snakemake |
| **Database** | PostgreSQL (via Django ORM) |
| **Testing** | Pytest |
| **Visualization** | Matplotlib |

---

## 🧪 Testing

Run tests manually:
```bash
pytest -v
```
Logs: `logs/pytest_output.log`

---

## 🧠 Author
**Erik R. — CityMind Project (2025)**  
MIT License © 2025  
GitHub: [Tarik2012](https://github.com/Tarik2012)
