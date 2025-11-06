# ======================================================
# CityMind - Snakemake Pipeline (versión PRO)
# Pipeline completo: Wrangling → Training → Comparison → Testing → Ingesta → Insights
# ======================================================

import os
import sys
import time
import csv
import importlib.util
from pathlib import Path
from datetime import datetime
import shutil

# ------------------------------------------------------
# 1. Cargar el módulo de logging dinámicamente
# ------------------------------------------------------
monitoring_path = Path("scripts/common/10_monitoring_logging.py")
spec = importlib.util.spec_from_file_location("monitoring", monitoring_path)
monitoring = importlib.util.module_from_spec(spec)
sys.modules["monitoring"] = monitoring
spec.loader.exec_module(monitoring)

PipelineStep = monitoring.PipelineStep
logger = monitoring.logger

# Carpeta actual de logs (viene del módulo)
LOG_DIR = monitoring.LOG_DIR
PIPELINE_SUMMARY = monitoring.summary_file

# ------------------------------------------------------
# 2. Función auxiliar: registrar resumen adicional
# ------------------------------------------------------
def append_summary(step, status, duration, start, end):
    with open(PIPELINE_SUMMARY, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([step, status, f"{duration:.2f}", start, end])

# ------------------------------------------------------
# 3. Regla principal (objetivos finales)
# ------------------------------------------------------
rule all:
    input:
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv",
        "data/interim/comparison/comparison_summary.csv",
        "tests/pytest_passed.txt",
        "logs/db_ingest_done.txt",
        "reports/data_insights.html"  # ✅ NUEVO: incluir análisis EDA final

# ------------------------------------------------------
# 4. Wrangling de datos (añadido export de final_places.csv)
# ------------------------------------------------------
rule wrangling:
    input:
        "data/raw/places_county_2024.csv"
    output:
        no_social="data/processed/no_social/places_no_social_clean.csv",
        full_social="data/processed/full_social/places_imputed_full_clean.csv",
        final="data/processed/final_places.csv"
    run:
        start = time.time()
        with PipelineStep("wrangling"):
            os.system("python scripts/common/01_wrangling_final.py")
        end = time.time()
        append_summary("wrangling", "completed", end - start, start, end)

# ------------------------------------------------------
# 5. Entrenamiento de modelos
# ------------------------------------------------------
rule train_models:
    input:
        no_social="data/processed/no_social/places_no_social_clean.csv",
        full_social="data/processed/full_social/places_imputed_full_clean.csv"
    output:
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv"
    run:
        start = time.time()
        with PipelineStep("train_models"):
            os.system("python scripts/no_social/04_train_models.py")
            os.system("python scripts/full_social/04_train_models_full_social.py")
        end = time.time()
        append_summary("train_models", "completed", end - start, start, end)

# ------------------------------------------------------
# 6. Comparación de resultados
# ------------------------------------------------------
rule compare_results:
    input:
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv"
    output:
        "data/interim/comparison/comparison_summary.csv"
    run:
        start = time.time()
        with PipelineStep("compare_results"):
            os.system("python scripts/comparison/05_compare_results.py")
        end = time.time()
        append_summary("compare_results", "completed", end - start, start, end)

# ------------------------------------------------------
# 7. Testing y validación
# ------------------------------------------------------
rule test:
    input:
        "data/interim/comparison/comparison_summary.csv"
    output:
        "tests/pytest_passed.txt"
    run:
        start = time.time()
        with PipelineStep("pytest_validation"):
            import subprocess

            pytest_log = LOG_DIR / "pytest_output.log"
            print(f"Running pytest (log → {pytest_log})...")

            result = subprocess.run(
                ["pytest", "-v", "--disable-warnings"],
                stdout=open(pytest_log, "w"),
                stderr=subprocess.STDOUT
            )

            end = time.time()
            if result.returncode == 0:
                with open("tests/pytest_passed.txt", "w") as f:
                    f.write("ok")
                append_summary("pytest_validation", "passed", end - start, start, end)
                print("\n✅ All tests passed successfully.")
            else:
                append_summary("pytest_validation", "failed", end - start, start, end)
                print("\n❌ Some tests failed. Check log at:", pytest_log)
                sys.exit(result.returncode)

# ------------------------------------------------------
# 8. Ingesta a PostgreSQL (Django ORM)
# ------------------------------------------------------
rule ingest_to_postgres:
    input:
        "tests/pytest_passed.txt",
        places="data/processed/final_places.csv",
        metrics_no_social="data/interim/no_social/model_metrics.csv",
        metrics_full_social="data/interim/full_social/model_metrics.csv",
        comparison="data/interim/comparison/comparison_summary.csv"
    output:
        "logs/db_ingest_done.txt"
    run:
        start = time.time()
        with PipelineStep("ingest_to_postgres"):
            print("🚀 Iniciando ingesta a PostgreSQL mediante Django ORM...")
            result = os.system("python scripts/db_ingest/06_ingest_to_postgres.py")

            if result == 0:
                with open("logs/db_ingest_done.txt", "w") as f:
                    f.write("done")
                print("✅ Ingesta a PostgreSQL completada correctamente.")
                status = "completed"
            else:
                print("❌ Error durante la ingesta a PostgreSQL.")
                status = "failed"

        end = time.time()
        append_summary("ingest_to_postgres", status, end - start, start, end)

# ------------------------------------------------------
# 9. Data Insights Report — EDA automatizado
# ------------------------------------------------------
rule data_insights:
    input:
        "data/processed/final_places.csv"
    output:
        "reports/data_insights.html"
    run:
        start = time.time()
        with PipelineStep("data_insights"):
            print("📊 Generando reporte de análisis exploratorio (EDA)...")
            os.system("python analytics/run_data_insights.py")
        end = time.time()
        append_summary("data_insights", "completed", end - start, start, end)

# ------------------------------------------------------
# 10. (Opcional) Limpieza
# ------------------------------------------------------
rule clean:
    shell:
        """
        echo Cleaning temporary data and logs...
        rmdir /s /q data\\interim 2>nul || true
        rmdir /s /q data\\processed 2>nul || true
        rmdir /s /q logs 2>nul || true
        mkdir logs
        echo Done.
        """
