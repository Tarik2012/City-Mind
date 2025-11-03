"""
Mocks de datos para ejecutar pytest en CI sin datasets reales.
Solo se activa en entornos GitHub Actions.
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

    # Mock de datos limpios
    pd.DataFrame({
        "county_fips": [1001, 1003],
        "depression": [15.2, 17.8],
        "poor_mental_health": [12.1, 13.4],
        "obesity": [30.5, 29.8],
        "smoking": [20.0, 21.3]
    }).to_csv("data/processed/no_social/places_no_social_clean.csv", index=False)

    pd.DataFrame({
        "county_fips": [1001, 1003],
        "depression": [14.8, 16.9],
        "poor_mental_health": [11.7, 12.9],
        "income": [55000, 47000],
        "education": [85.3, 79.2]
    }).to_csv("data/processed/full_social/places_imputed_full_clean.csv", index=False)

    # Mock de métricas y comparación
    pd.DataFrame({
        "model": ["XGBoost", "RandomForest"],
        "target": ["depression", "mental_health"],
        "r2": [0.85, 0.83],
        "rmse": [2.5, 2.8],
        "mae": [1.9, 2.0]
    }).to_csv("data/interim/no_social/model_metrics.csv", index=False)

    pd.DataFrame({
        "model": ["XGBoost", "LassoCV"],
        "target": ["depression", "mental_health"],
        "r2": [0.88, 0.81],
        "rmse": [2.3, 2.9],
        "mae": [1.7, 2.1]
    }).to_csv("data/interim/full_social/model_metrics.csv", index=False)

    pd.DataFrame({
        "scenario": ["no_social", "full_social"],
        "best_model": ["XGBoost", "XGBoost"],
        "r2_avg": [0.84, 0.86]
    }).to_csv("data/interim/comparison/comparison_summary.csv", index=False)
