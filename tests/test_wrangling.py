"""
tests/test_wrangling.py - Validaciones de limpieza de datos CityMind
---------------------------------------------------------------------
Verifica que los datasets limpios cumplan condiciones básicas:
  ✅ Existen los archivos procesados
  ✅ No hay valores nulos
  ✅ Columnas clave presentes
  ✅ Valores dentro de rangos válidos
  ✅ Sin valores negativos en indicadores de salud
"""

import os
import pytest
import pandas as pd


# ---------------------------------------------------------------
# 1️⃣ Test: existencia de archivos
# ---------------------------------------------------------------
def test_files_exist(data_paths):
    """Verifica que los archivos limpios existen en /data/processed"""
    for name, path in data_paths.items():
        assert path.exists(), f"❌ No existe el archivo esperado: {path}"


# ---------------------------------------------------------------
# 2️⃣ Test: no nulos en datasets limpios
# ---------------------------------------------------------------
def test_no_nulls_in_clean(no_social_df, full_social_df):
    """Comprueba que los datasets *_clean.csv no tengan valores nulos"""
    assert no_social_df.isna().sum().sum() == 0, "❌ Hay valores nulos en No Social"
    assert full_social_df.isna().sum().sum() == 0, "❌ Hay valores nulos en Full Social"


# ---------------------------------------------------------------
# 3️⃣ Test: rango de la variable de depresión
# ---------------------------------------------------------------
def test_depression_range(full_social_df):
    """La columna depression_crudeprev debe existir y estar en rango 0–100"""
    col = "depression_crudeprev"
    assert col in full_social_df.columns, f"❌ Falta columna '{col}'"
    assert full_social_df[col].between(0, 100).all(), "❌ Valores fuera de rango (0–100)"


# ---------------------------------------------------------------
# 4️⃣ Test: columnas clave en No Social
# ---------------------------------------------------------------
def test_columns_expected_no_social(no_social_df):
    """El dataset No Social Clean debe tener las columnas clave"""
    expected_cols = [
        "stateabbr",
        "statedesc",
        "countyname",
        "countyfips",
        "depression_crudeprev",
    ]
    for col in expected_cols:
        assert col in no_social_df.columns, f"❌ Falta columna '{col}' en No Social"


# ---------------------------------------------------------------
# 5️⃣ Test: valores no negativos en indicadores de salud
# ---------------------------------------------------------------
def test_positive_values_health(full_social_df):
    """Variables de salud deben ser no negativas"""
    cols_check = [
        "obesity_crudeprev",
        "diabetes_crudeprev",
        "lpa_crudeprev",  # physical inactivity (low physical activity)
    ]
    for col in cols_check:
        assert col in full_social_df.columns, f"❌ Falta columna '{col}'"
        assert (full_social_df[col] >= 0).all(), f"❌ Valores negativos detectados en {col}"
