"""
tests/test_compare_results.py - Validación de comparación entre escenarios CityMind
-----------------------------------------------------------------------------------
Comprueba que el archivo comparison_summary.csv existe, tiene estructura correcta
y que las métricas reflejan la superioridad del modelo XGBoost en ambos targets.
"""

import os
import pandas as pd
import pytest


# ---------------------------------------------------------------
# 1️⃣ FIXTURE LOCAL (rutas)
# ---------------------------------------------------------------
@pytest.fixture(scope="session")
def comparison_path():
    """Ruta del archivo de comparación"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", "interim", "comparison", "comparison_summary.csv")


# ---------------------------------------------------------------
# 2️⃣ Test: existencia del archivo de comparación
# ---------------------------------------------------------------
def test_comparison_file_exists(comparison_path):
    """Verifica que el archivo comparison_summary.csv exista"""
    assert os.path.exists(comparison_path), f"❌ No existe el archivo de comparación: {comparison_path}"


# ---------------------------------------------------------------
# 3️⃣ Test: estructura del archivo
# ---------------------------------------------------------------
def test_comparison_structure(comparison_path):
    """Comprueba que la tabla tiene las columnas esperadas"""
    df = pd.read_csv(comparison_path)
    expected_cols = {"target", "model", "scenario", "r2", "rmse", "mae"}
    missing = expected_cols - set(df.columns)
    assert not missing, f"❌ Faltan columnas {missing} en comparison_summary.csv"
    assert len(df) > 0, "❌ El archivo de comparación está vacío"


# ---------------------------------------------------------------
# 4️⃣ Test: presencia de targets esperados
# ---------------------------------------------------------------
def test_targets_present(comparison_path):
    """Verifica que ambos targets principales están incluidos"""
    df = pd.read_csv(comparison_path)
    expected_targets = {"depression_crudeprev", "mhlth_crudeprev"}
    found = set(df["target"].unique())
    missing = expected_targets - found
    assert not missing, f"❌ Faltan targets en el archivo de comparación: {missing}"


# ---------------------------------------------------------------
# 5️⃣ Test: coherencia de métricas
# ---------------------------------------------------------------
def test_metrics_consistency(comparison_path):
    """Las métricas deben tener valores coherentes"""
    df = pd.read_csv(comparison_path)
    assert df["r2"].between(0, 1).all(), "❌ R² fuera de rango (0-1)"
    assert (df["rmse"] > 0).all(), "❌ RMSE no positivo"
    assert (df["mae"] > 0).all(), "❌ MAE no positivo"


# ---------------------------------------------------------------
# 6️⃣ Test: XGBoost mejor modelo (comparación por target)
# ---------------------------------------------------------------
def test_xgboost_best_model(comparison_path):
    """XGBoost debe tener el mejor R² en ambos targets"""
    df = pd.read_csv(comparison_path)

    for target in df["target"].unique():
        subset = df[df["target"] == target]
        best_model = subset.loc[subset["r2"].idxmax(), "model"]
        assert best_model == "XGBoost", f"❌ {target}: el mejor modelo no es XGBoost (es {best_model})"
