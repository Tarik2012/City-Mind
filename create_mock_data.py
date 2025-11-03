"""
Mocks de datos para ejecutar pytest en CI sin datasets reales.
Compatible con las expectativas de los tests de CityMind.
"""

import os
import pandas as pd
from pathlib import Path

# Detectar entorno CI
if os.getenv("GITHUB_ACTIONS") == "true":
    print("🧪 Ejecutando en CI - creando datos de prueba mock...")

    base_dirs = [
        "data/processed/no_social",
        "data/processed/full_social",
        "data/interim/no_social",
        "data/interim/full_social",
        "data/interim/comparison",
    ]
    for d in base_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

    # Mock de No Social con columnas reales esperadas
    pd.DataFrame({
        "stateabbr": ["AL", "AL"],
        "statedesc": ["Alabama", "Alabama"],
        "countyname": ["Autauga", "Baldwin"],
        "countyfips": [1001, 1003],
        "depression_crudeprev": [15.2, 17.8],
        "obesity_crudeprev": [30.5, 29.8],
        "smoking_crudeprev": [20.0, 21.3]
    }).to_csv("data/processed/no_social/places_no_social_clean.csv", index=False)

    # Mock de Full Social con columnas reales esperadas
    pd.DataFrame({
        "county_fips": [1001, 1003],
        "depression_crudeprev": [14.8, 16.9],
        "mhlth_crudeprev": [11.7, 12.9],
        "obesity_crudeprev": [30.1, 29.9],
        "diabetes_crudeprev": [8.5, 9.0],
        "lpa_crudeprev": [22.0, 21.5],
        "income": [55000, 47000],
        "education": [85.3, 79.2]
    }).to_csv("data/processed/full_social/places_imputed_full_clean.csv", index=False)

    # Mock de métricas No Social
    pd.DataFrame({
        "model": ["XGBoost", "RandomForest"],
        "target": ["depression_crudeprev", "mhlth_crudeprev"],
        "r2": [0.85, 0.83],
        "rmse": [2.5, 2.8],
        "mae": [1.9, 2.0]
    }).to_csv("data/interim/no_social/model_metrics.csv", index=False)

    # Mock de métricas Full Social
    pd.DataFrame({
        "model": ["XGBoost", "LassoCV"],
        "target": ["depression_crudeprev", "mhlth_crudeprev"],
        "r2": [0.88, 0.81],
        "rmse": [2.3, 2.9],
        "mae": [1.7, 2.1]
    }).to_csv("data/interim/full_social/model_metrics.csv", index=False)

    # Mock de comparación con estructura completa esperada
    pd.DataFrame({
        "target": ["depression_crudeprev", "mhlth_crudeprev"] * 2,
        "model": ["XGBoost", "RandomForest", "XGBoost", "LassoCV"],
        "scenario": ["no_social", "no_social", "full_social", "full_social"],
        "r2": [0.85, 0.83, 0.88, 0.81],
        "rmse": [2.5, 2.8, 2.3, 2.9],
        "mae": [1.9, 2.0, 1.7, 2.1]
    }).to_csv("data/interim/comparison/comparison_summary.csv", index=False)

    print("✅ Datos mock creados correctamente.")
