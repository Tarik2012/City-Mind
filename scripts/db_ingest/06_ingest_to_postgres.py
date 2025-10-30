"""
CityMind - Script de Ingesta a PostgreSQL
-----------------------------------------
Carga los resultados del pipeline (wrangling, métricas, comparaciones y predicciones)
directamente a la base de datos gestionada por Django.

Se ejecuta como parte del pipeline Snakemake:
    python scripts/db_ingest/06_ingest_to_postgres.py
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

# ======================================================
#  CONFIGURACIÓN DJANGO
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citymind.settings")
django.setup()

from core.models import PlaceRecord, ModelMetrics, ComparisonSummary, Prediction


# ======================================================
#  CONFIGURACIÓN DE LOGGING
# ======================================================
LOG_PATH = "logs/db_ingest.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logging.info("===== INICIO DE INGESTA A POSTGRESQL =====")

print("🚀 Iniciando ingesta a PostgreSQL mediante Django ORM...")


# ======================================================
#  FUNCIONES DE INGESTA
# ======================================================

def clean_number(value):
    """Convierte cadenas numéricas con comas en enteros seguros"""
    try:
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return int(value.replace(",", "").strip())
        return int(value)
    except Exception:
        return None


def detect_dataset_type(path: str) -> str:
    """Detecta si el dataset es No Social o Full Social a partir de la ruta"""
    path_lower = path.lower()
    if "full_social" in path_lower:
        return "full_social"
    elif "no_social" in path_lower:
        return "no_social"
    else:
        return "no_social"  # fallback por defecto


def ingest_place_records(path="data/processed/final_places.csv"):
    """Carga los registros base de condados"""
    if not os.path.exists(path):
        logging.warning(f"No se encontró {path}, omitiendo PlaceRecord.")
        return
    df = pd.read_csv(path)
    logging.info(f"Iniciando carga de {len(df)} registros de PlaceRecord.")

    for _, row in df.iterrows():
        try:
            PlaceRecord.objects.update_or_create(
                fips=row["countyfips"],
                defaults={
                    "name": row.get("countyname", ""),
                    "state": row.get("statedesc", ""),
                    "population": clean_number(row.get("totalpopulation")),
                    "latitude": None,
                    "longitude": None,
                    "year": datetime.now().year,
                },
            )
        except Exception as e:
            logging.error(f"Error insertando PlaceRecord {row.get('countyfips')}: {e}")

    logging.info("Carga de PlaceRecord completada ✅")


def ingest_model_metrics():
    """Carga las métricas de modelos entrenados"""
    paths = [
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv",
    ]

    for p in paths:
        if not os.path.exists(p):
            logging.warning(f"No se encontró {p}, omitiendo ModelMetrics.")
            continue

        dataset_type = detect_dataset_type(p)
        df = pd.read_csv(p)
        df.columns = [c.strip().lower() for c in df.columns]
        logging.info(f"Iniciando carga de {len(df)} métricas desde {p} ({dataset_type}).")

        for _, row in df.iterrows():
            try:
                ModelMetrics.objects.create(
                    model_name=row.get("model") or row.get("model_name") or "unknown_model",
                    target=row.get("target", "unknown"),
                    dataset_type=dataset_type,  # 👈 nuevo campo
                    r2_score=row.get("r2") or row.get("r2_score") or 0,
                    mae=row.get("mae", 0),
                    rmse=row.get("rmse", 0),
                )
            except Exception as e:
                logging.error(f"Error insertando métrica desde {p}: {e}")

    logging.info("Carga de ModelMetrics completada ✅")


def ingest_comparison_summary(path="data/interim/comparison/comparison_summary.csv"):
    """Carga los resúmenes de comparación de modelos"""
    if not os.path.exists(path):
        logging.warning(f"No se encontró {path}, omitiendo ComparisonSummary.")
        return

    dataset_type = detect_dataset_type(path)
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    logging.info(f"Iniciando carga de {len(df)} resúmenes de comparación ({dataset_type}).")

    for _, row in df.iterrows():
        try:
            ComparisonSummary.objects.create(
                target=row.get("target", "unknown"),
                dataset_type=dataset_type,  # 👈 nuevo campo
                best_model=row.get("best_model", "unknown"),
                best_r2=row.get("best_r2") or row.get("r2") or 0,
                best_mae=row.get("best_mae") or row.get("mae") or 0,
                best_rmse=row.get("best_rmse") or row.get("rmse") or 0,
            )
        except Exception as e:
            logging.error(f"Error insertando resumen de comparación: {e}")

    logging.info("Carga de ComparisonSummary completada ✅")


def ingest_predictions(path="data/interim/predictions.csv"):
    """Carga predicciones generadas por los modelos"""
    if not os.path.exists(path):
        logging.warning(f"No se encontró {path}, omitiendo Predicciones.")
        return

    df = pd.read_csv(path)
    logging.info(f"Iniciando carga de {len(df)} predicciones.")
    for _, row in df.iterrows():
        try:
            place = PlaceRecord.objects.get(fips=row["fips"])
            Prediction.objects.create(
                place=place,
                model_used=row.get("model_used", ""),
                target=row.get("target", ""),
                predicted_value=row.get("predicted_value", None),
                input_vector=row.get("input_vector", "{}"),
            )
        except PlaceRecord.DoesNotExist:
            logging.error(f"No se encontró PlaceRecord con FIPS {row['fips']}, omitiendo predicción.")
        except Exception as e:
            logging.error(f"Error insertando predicción: {e}")

    logging.info("Carga de Predicciones completada ✅")


# ======================================================
#  PIPELINE PRINCIPAL
# ======================================================
if __name__ == "__main__":
    try:
        ingest_place_records()
        ingest_model_metrics()
        ingest_comparison_summary()
        ingest_predictions()
        logging.info("===== INGESTA FINALIZADA CON ÉXITO =====")
        print("✅ Ingesta completada correctamente. Ver logs/db_ingest.log para más detalles.")
    except Exception as e:
        logging.exception(f"Error durante la ingesta: {e}")
        print("❌ Error durante la ingesta. Revisa logs/db_ingest.log.")
