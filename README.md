# 🧠 CityMind – Mental Health & Social Factors Modeling

CityMind es un proyecto de *Data Science* orientado a analizar y predecir indicadores de salud mental a nivel local, usando datos abiertos del CDC (PLACES, USA) y variables socioeconómicas.  
Integra un pipeline completo con **Python**, **Snakemake**, **Pytest**, **Logging**, y **DVC/MLflow-ready**.

---

## 📂 Estructura del proyecto

```
CityMind/
│
├── data/
│   ├── raw/                     # Datos originales (CDC PLACES, etc.)
│   ├── interim/                 # Resultados intermedios y métricas parciales
│   │   ├── no_social/           # Escenario sin variables sociales
│   │   ├── full_social/         # Escenario con variables sociales
│   │   └── comparison/          # Comparación entre escenarios
│   ├── processed/               # Datasets finales para modelado/API
│   └── old/                     # Versiones antiguas archivadas
│
├── eda/
│   └── eda_master.py            # Análisis exploratorio (EDA)
│
├── scripts/
│   ├── common/
│   │   └── 01_wrangling_final.py
│   ├── no_social/
│   │   ├── 02_feature_selection.py
│   │   ├── 03_prepare_model_data.py
│   │   └── 04_train_models.py
│   ├── full_social/
│   │   ├── 02_feature_selection_full_social.py
│   │   ├── 03_prepare_model_data_full_social.py
│   │   └── 04_train_models_full_social.py
│   ├── comparison/
│   │   └── 05_compare_results.py
│   └── report/
│       └── 06_generate_report.py
│
├── tests/
│   ├── test_wrangling.py
│   ├── test_model_training.py
│   ├── test_compare_results.py
│   └── .pytest_passed
│
├── reports/
│   └── citymind_report_YYYY-MM-DD.md
│
├── Snakefile                   # Orquestación de pipeline con Snakemake
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Pipeline general

| Etapa | Script | Entrada | Salida | Descripción |
|-------|--------|----------|---------|--------------|
| 🧹 Wrangling | `01_wrangling_final.py` | Datos brutos | Datasets limpios | Limpieza, imputación, normalización |
| ⚙️ Feature Selection | `02_feature_selection*.py` | Clean datasets | Summary CSV | Selección de variables (Lasso, correlación, PCA) |
| 🧮 Model Data | `03_prepare_model_data*.py` | Features | Model data CSV | Construcción datasets de modelado |
| 🤖 Training | `04_train_models*.py` | Model data | model_metrics.csv | Entrenamiento de LassoCV, RF, XGBoost |
| 📊 Comparison | `05_compare_results.py` | Métricas | comparison_summary.csv | Comparación No Social vs Full Social |
| 🧾 Reporte | `06_generate_report.py` | Summary | MD/PDF report | Genera reporte final técnico |

---

## 🧪 Testing

Se usa **Pytest** para asegurar calidad de cada paso:

| Test | Archivo | Objetivo |
|------|----------|----------|
| ✅ Limpieza | `test_wrangling.py` | Verifica datasets limpios y completos |
| ✅ Modelado | `test_model_training.py` | Revisa métricas y valores coherentes |
| ✅ Comparación | `test_compare_results.py` | Asegura consistencia y ranking correcto |

Ejecutar todos los tests:

```bash
pytest -v
```

Salida esperada:

```
5 passed in 0.14s
```

---

## 🧰 Automatización (Snakemake)

Pipeline automatizado con **Snakemake**:

```python
rule all:
    input:
        "data/interim/no_social/places_no_social_clean.csv",
        "data/interim/full_social/places_imputed_full_clean.csv",
        "tests/.pytest_passed"

rule wrangling:
    input:
        "data/raw/places_county_2024.csv"
    output:
        "data/interim/no_social/places_no_social_clean.csv",
        "data/interim/full_social/places_imputed_full_clean.csv"
    shell:
        "python scripts/common/01_wrangling_final.py"

rule test:
    input:
        "data/interim/no_social/places_no_social_clean.csv",
        "data/interim/full_social/places_imputed_full_clean.csv"
    output:
        "tests/.pytest_passed"
    shell:
        "pytest -v && echo 'ok' > {output}"
```

Ejecutar pipeline completo:

```bash
snakemake -j1
```

---

## 📈 Resultados principales

| Target | Modelo | R² | RMSE | MAE | PCA |
|---------|---------|----|------|-----|-----|
| depression_crudeprev | XGBoost | 0.849 | 1.319 | 1.004 | 5 |
| mhlth_crudeprev | XGBoost | 0.967 | 0.423 | 0.326 | 10 |

### 🏁 Conclusión:
- El modelo **XGBoost** ofrece el mejor rendimiento en ambos targets.  
- Las variables sociales solo mejoran marginalmente la predicción de *salud mental general*.  
- Para la API se recomienda el escenario **No Social**, por simplicidad y reproducibilidad.

---

## 🧩 Tecnologías utilizadas

| Categoría | Tecnologías |
|------------|-------------|
| Lenguaje | Python 3.13 |
| Workflow | Snakemake, DVC (planificado), MLflow (planificado) |
| ML | Scikit-learn, XGBoost |
| EDA | Pandas, Matplotlib, ydata-profiling |
| Tests | Pytest |
| Logging | `logging` de Python |
| Web (futuro) | Django API |
| CI/CD | GitHub Actions (planificado) |

---

## 🧾 Autor

**CityMind Project** — *Data Science for Urban Mental Health*  
Desarrollado por **Erik Rocha**  
📍 Proyecto académico y profesional — 2025  
Repositorio: [GitHub - CityMind](https://github.com/tu_usuario/CityMind)

---

> “Measure what matters. Model what improves.”  
> — *CityMind Team, 2025*
