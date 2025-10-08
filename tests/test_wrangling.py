import os
import pandas as pd

# ---------------------------
# Configuración de rutas
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sube desde /tests a la raíz
DATA_DIR = os.path.join(BASE_DIR, "data")

# Archivos que deberíamos haber generado en wrangling_final.ipynb
FILES_EXPECTED = [
    "places_no_social_clean.csv",
    "places_imputed_clean.csv",
    "places_imputed_full_clean.csv",
]


# ---------------------------
# Tests
# ---------------------------

def test_files_exist():
    """Verifica que los archivos generados existen en /data"""
    for fname in FILES_EXPECTED:
        fpath = os.path.join(DATA_DIR, fname)
        assert os.path.exists(fpath), f"El archivo {fname} no existe en {DATA_DIR}"


def test_no_nulls_in_clean():
    """Comprueba que los datasets *_clean.csv no tengan nulos"""
    for fname in ["places_no_social_clean.csv", "places_imputed_full_clean.csv"]:
        fpath = os.path.join(DATA_DIR, fname)
        df = pd.read_csv(fpath)
        assert df.isna().sum().sum() == 0, f"Hay nulos en {fname}"


def test_depression_range():
    """La columna depression debe existir y estar en rango 0-100"""
    fpath = os.path.join(DATA_DIR, "places_imputed_full_clean.csv")
    df = pd.read_csv(fpath)
    assert "depression" in df.columns, "No existe columna 'depression'"
    assert df["depression"].between(0, 100).all(), "Valores de depression fuera de rango"


def test_columns_expected_no_social():
    """El dataset No Social Clean debe tener las columnas clave"""
    fpath = os.path.join(DATA_DIR, "places_no_social_clean.csv")
    df = pd.read_csv(fpath)
    expected_cols = ["stateabbr", "statedesc", "locationname", "locationid", "depression"]
    for col in expected_cols:
        assert col in df.columns, f"Falta columna {col} en places_no_social_clean.csv"


def test_positive_values_health():
    """Algunas variables de salud deben ser no negativas"""
    fpath = os.path.join(DATA_DIR, "places_imputed_full_clean.csv")
    df = pd.read_csv(fpath)
    cols_check = ["obesity", "physical_inactivity", "diabetes"]
    for col in cols_check:
        assert (df[col] >= 0).all(), f"Valores negativos encontrados en {col}"
