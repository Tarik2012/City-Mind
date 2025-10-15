"""
conftest.py - Configuración de pytest para CityMind
---------------------------------------------------
Define fixtures reutilizables para todos los tests:
  - Rutas base del proyecto
  - Carga de datasets limpios (No Social / Full Social)
  - Directorios de trabajo (data, reports)
"""

import os
import pytest
import pandas as pd
from pathlib import Path

# =====================================================
# 🔧 FIXTURES GLOBALES
# =====================================================

@pytest.fixture(scope="session")
def base_dir():
    """
    Devuelve la ruta base del proyecto CityMind.
    (Ejemplo: C:/Users/.../CityMind)
    """
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def data_paths(base_dir):
    """
    Devuelve las rutas principales de los datasets procesados.
    """
    data_dir = base_dir / "data" / "processed"
    return {
        "no_social": data_dir / "no_social" / "places_no_social_clean.csv",
        "full_social": data_dir / "full_social" / "places_imputed_full_clean.csv"
    }


@pytest.fixture(scope="session")
def no_social_df(data_paths):
    """
    Carga el dataset limpio 'No Social'.
    """
    path = data_paths["no_social"]
    assert path.exists(), f"❌ No existe el dataset: {path}"
    df = pd.read_csv(path)
    return df


@pytest.fixture(scope="session")
def full_social_df(data_paths):
    """
    Carga el dataset limpio 'Full Social'.
    """
    path = data_paths["full_social"]
    assert path.exists(), f"❌ No existe el dataset: {path}"
    df = pd.read_csv(path)
    return df


@pytest.fixture(scope="session")
def report_dir(base_dir):
    """
    Devuelve la ruta del directorio de reportes (/reports)
    y lo crea si no existe.
    """
    report_path = base_dir / "reports"
    report_path.mkdir(parents=True, exist_ok=True)
    return report_path


@pytest.fixture(scope="session")
def interim_dir(base_dir):
    """
    Devuelve la ruta del directorio de resultados intermedios (/data/interim)
    """
    interim_path = base_dir / "data" / "interim"
    interim_path.mkdir(parents=True, exist_ok=True)
    return interim_path


# =====================================================
# 🔬 FIXTURES OPCIONALES (para futuras pruebas)
# =====================================================

@pytest.fixture
def sample_no_social(no_social_df):
    """
    Devuelve una muestra pequeña del dataset No Social para tests rápidos.
    """
    return no_social_df.sample(n=100, random_state=42)


@pytest.fixture
def sample_full_social(full_social_df):
    """
    Devuelve una muestra pequeña del dataset Full Social para tests rápidos.
    """
    return full_social_df.sample(n=100, random_state=42)
