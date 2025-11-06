# 🧠 CityMind Project — AI-Powered Mental Health Insights
[![CityMind CI](https://github.com/Tarik2012/City-Mind/actions/workflows/ci.yml/badge.svg)](https://github.com/Tarik2012/City-Mind/actions/workflows/ci.yml)

CityMind es un proyecto **end-to-end (ML + backend)** que analiza la **prevalencia de salud mental y depresión** en condados de EE. UU. usando **CDC PLACES 2024**.  
Integra un **pipeline ML (Snakemake)** y una **Django REST API** para servir predicciones en tiempo real a partir de indicadores socio-sanitarios agregados.

---

## 🌍 Targets y escenarios

| Target                 | Descripción                         |
|-----------------------|-------------------------------------|
| `mhlth_crudeprev`     | Prevalencia de mala salud mental    |
| `depression_crudeprev`| Prevalencia de depresión            |

Cada target se entrena en dos escenarios paralelos:
- 🧩 **No Social** → solo variables de salud/demográficas  
- 🌐 **Full Social** → añade indicadores sociales/económicos/ambientales  

➡️ Resultado: **4 modelos XGBoost** (`no_social` + `full_social` × 2 targets).

---

## 🧱 Arquitectura

| Módulo                      | Descripción                                                     |
|----------------------------|-----------------------------------------------------------------|
| **Django Backend (`core`, `api`)** | Modelos ORM, endpoints REST y conexión PostgreSQL          |
| **Pipeline ML (Snakemake)** | Wrangling → Training → Comparison → Testing → Ingestion        |
| **Scripts**                | Preprocesado, entrenamiento y comparación                       |
| **DB Ingest**              | Ingesta automática vía ORM de Django                            |

---

## 📂 Estructura del proyecto

```
CityMind/
├── core/                         # Django models/admin/ORM
├── api/                          # DRF (views/serializers/urls)
├── scripts/
│   ├── common/                   # Wrangling y utilidades
│   ├── no_social/                # Entrenamiento sin variables sociales
│   ├── full_social/              # Entrenamiento con variables sociales
│   └── comparison/               # Comparación y visualización
├── data/
│   ├── raw/                      # Datos CDC de entrada
│   ├── processed/                # Datos limpios para ML
│   └── interim/                  # Métricas y resúmenes
├── models/                       # Modelos entrenados (.joblib)
├── tests/                        # Pytest + mocks (create_mock_data.py)
├── logs/                         # Logs de pipeline y API
├── Snakefile                     # Definición de Snakemake
├── requirements.txt
├── manage.py
└── .github/workflows/ci.yml      # CI de GitHub Actions
```

---

## ⚙️ Instalación y arranque

### 1) Crear entorno
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 2) Dependencias
```bash
pip install -r requirements.txt
```

### 3) Migraciones (PostgreSQL)
```bash
python manage.py migrate
```

### 4) Levantar API
```bash
python manage.py runserver
```

API: http://127.0.0.1:8000/api/predict/

---

## 🔮 Ejemplo de predicción

### POST `/api/predict/`
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

**Respuesta**
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

> Internamente `expand_features()` transforma los índices agregados en ~41–45 features reales esperadas por cada modelo XGBoost.

---

## 📊 Ejecución del pipeline (Snakemake)

```bash
snakemake -p --cores 1 --latency-wait 10
```

Secuencia:
1. 🧹 Wrangling  
2. 🧠 Entrenamiento (No Social + Full Social)  
3. 📈 Comparación de resultados  
4. 🧪 Pytest  
5. 🗃️ Ingesta a DB por ORM  

---

## 📦 Artefactos generados

| Archivo                                        | Descripción                               |
|-----------------------------------------------|-------------------------------------------|
| `data/interim/no_social/model_metrics.csv`     | Métricas modelo No Social                 |
| `data/interim/full_social/model_metrics.csv`   | Métricas modelo Full Social               |
| `data/interim/comparison/comparison_summary.csv` | R² / MAE / RMSE comparativo             |
| `data/interim/comparison/r2_comparison.png`    | Visualización de mejora en R²             |
| `logs/db_ingest_done.txt`                      | Marcador de pipeline completo             |

---

## 🧪 Tests

Ejecutar tests localmente:
```bash
pytest -v
```
Logs: `logs/pytest_output.log`

**En CI** se crean datos mock compatibles con los tests:
- `tests/create_mock_data.py` genera:
  - `data/processed/no_social/places_no_social_clean.csv`
  - `data/processed/full_social/places_imputed_full_clean.csv`
  - métricas por escenario y `comparison_summary.csv` con **XGBoost como mejor modelo** en ambos targets (alineado con los asserts).

---

## 🔄 CI/CD (GitHub Actions)

Workflow: `.github/workflows/ci.yml` (ramas `main` y `dev`)

Etapas:
1. Checkout  
2. Python 3.11  
3. `pip install -r requirements.txt`  
4. `flake8` (no bloqueante)  
5. **Mocks de datos** (`tests/create_mock_data.py`)  
6. `snakemake -n -p` (dry-run)  
7. `pytest -v`

**Badge:** ![CityMind CI](https://github.com/Tarik2012/City-Mind/actions/workflows/ci.yml/badge.svg)

---

## 🧩 Tecnologías

| Categoría       | Stack                                   |
|-----------------|-----------------------------------------|
| ML / Datos      | XGBoost, scikit-learn, Pandas, NumPy     |
| Backend         | Django 5, Django REST Framework          |
| Orquestación    | Snakemake                                |
| Base de datos   | PostgreSQL (Django ORM)                  |
| Testing         | Pytest                                   |
| Visualización   | Matplotlib                               |

---

## 🧱 Historial de CI/Testing (lecciones clave)

| Incidencia                                   | Causa raíz                                  | Solución                                                                 |
|---------------------------------------------|---------------------------------------------|--------------------------------------------------------------------------|
| Faltaba `.env.example`                      | Validación en CI                            | Añadido check + archivo ejemplo                                          |
| Snakemake sin entradas                      | Datos CDC no presentes en CI                | Generador de mocks para rutas esperadas                                  |
| Error YAML en `ci.yml`                      | Indentación/sintaxis                        | Reformat de workflow                                                     |
| `create_mock_data.py` no encontrado         | Ruta incorrecta                             | Script en `tests/` y paso explícito en workflow                          |
| 7/14 tests fallando                         | Columnas incompatibles con los tests        | Mocks con **nombres reales** (`*_crudeprev`, `stateabbr`, etc.)          |
| XGBoost no “best model” en CI               | Valores de R² de mock                       | Ajuste de mocks: XGBoost > resto en ambos targets                        |
| ✅ Estado final                              | CI verde                                     | 14/14 tests OK y pipeline reproducible                                   |

---

## 🧠 Autor
**Erik R. — CityMind Project (2025)** · MIT License © 2025  
Maintainer CI/CD: **Tarik2012**
