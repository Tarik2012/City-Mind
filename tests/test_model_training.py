"""
tests/test_model_training.py - Validaciones de resultados de entrenamiento CityMind
------------------------------------------------------------------------------------
Comprueba que los archivos de métricas existen, contienen columnas esperadas
y que las métricas tienen valores coherentes.
"""

import os
import pandas as pd
import pytest


# ---------------------------------------------------------------
# 1️⃣ FIXTURES LOCALES (opcional si aún no las tienes en conftest)
# ---------------------------------------------------------------
@pytest.fixture(scope="session")
def model_metrics_paths():
    """Rutas esperadas para los resultados de modelos."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    interim_dir = os.path.join(base_dir, "data", "interim")
    return {
        "no_social": os.path.join(interim_dir, "no_social", "model_metrics.csv"),
        "full_social": os.path.join(interim_dir, "full_social", "model_metrics.csv"),
    }


# ---------------------------------------------------------------
# 2️⃣ Test: existencia de archivos de métricas
# ---------------------------------------------------------------
def test_metrics_files_exist(model_metrics_paths):
    """Verifica que los archivos de métricas existen en /data/interim"""
    for name, path in model_metrics_paths.items():
        assert os.path.exists(path), f"❌ No existe el archivo de métricas para {name}: {path}"


# ---------------------------------------------------------------
# 3️⃣ Test: columnas esperadas en las métricas
# ---------------------------------------------------------------
def test_metrics_columns(model_metrics_paths):
    """Comprueba que los CSVs de métricas contienen las columnas esperadas"""
    expected_cols = {"model", "target", "r2", "rmse", "mae"}
    for name, path in model_metrics_paths.items():
        df = pd.read_csv(path)
        missing = expected_cols - set(df.columns)
        assert not missing, f"❌ Faltan columnas {missing} en {path}"


# ---------------------------------------------------------------
# 4️⃣ Test: rango de valores de métricas
# ---------------------------------------------------------------
def test_metrics_value_ranges(model_metrics_paths):
    """Verifica que las métricas tienen valores coherentes"""
    for name, path in model_metrics_paths.items():
        df = pd.read_csv(path)

        # R² debe estar entre 0 y 1
        assert df["r2"].between(0, 1).all(), f"❌ R² fuera de rango en {name}"

        # RMSE y MAE deben ser positivos
        assert (df["rmse"] > 0).all(), f"❌ RMSE no positivo en {name}"
        assert (df["mae"] > 0).all(), f"❌ MAE no positivo en {name}"


# ---------------------------------------------------------------
# 5️⃣ Test: modelos esperados registrados
# ---------------------------------------------------------------
def test_expected_models(model_metrics_paths):
    """Verifica que los modelos esperados están en los resultados"""
    expected_models = {"XGBoost", "LassoCV", "RandomForest"}
    for name, path in model_metrics_paths.items():
        df = pd.read_csv(path)
        models = set(df["model"].unique())
        assert expected_models & models, f"❌ No se encontraron los modelos esperados en {name}"
