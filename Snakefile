# ======================================================
# CityMind - Snakemake Pipeline (versión estable)
# Pipeline completo: Wrangling → Training → Comparison → Testing
# ======================================================

import os
import sys
import time
import csv
import importlib.util
from pathlib import Path

# ------------------------------------------------------
# Cargar dinámicamente el módulo 10_monitoring_logging.py
# ------------------------------------------------------
monitoring_path = Path("scripts/common/10_monitoring_logging.py")
spec = importlib.util.spec_from_file_location("monitoring", monitoring_path)
monitoring = importlib.util.module_from_spec(spec)
sys.modules["monitoring"] = monitoring
spec.loader.exec_module(monitoring)

PipelineStep = monitoring.PipelineStep
logger = monitoring.logger

# ------------------------------------------------------
# Función auxiliar: registrar resumen de ejecución
# ------------------------------------------------------
summary_path = Path("logs/pipeline_summary.csv")
summary_path.parent.mkdir(exist_ok=True)
if not summary_path.exists():
    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "status", "duration_seconds", "start_time", "end_time"])

def append_summary(step, status, duration, start, end):
    with open(summary_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([step, status, f"{duration:.2f}", start, end])

# ------------------------------------------------------
# 0️⃣ Regla principal
# ------------------------------------------------------
rule all:
    input:
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv",
        "data/interim/comparison/comparison_summary.csv",
        "tests/pytest_passed.txt"

# ------------------------------------------------------
# 1️⃣ Wrangling de datos
# ------------------------------------------------------
rule wrangling:
    input:
        "data/raw/places_county_2024.csv"
    output:
        "data/processed/no_social/places_no_social_clean.csv",
        "data/processed/full_social/places_imputed_full_clean.csv"
    run:
        start = time.time()
        with PipelineStep("wrangling"):
            os.system("python scripts/common/01_wrangling_final.py")
        end = time.time()
        append_summary("wrangling", "completed", end - start, start, end)

# ------------------------------------------------------
# 2️⃣ Entrenamiento de modelos
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
# 3️⃣ Comparación de resultados
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
# 4️⃣ Pruebas automáticas con pytest
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

            os.makedirs("logs", exist_ok=True)
            print("Running pytest...")

            result = subprocess.run(
                ["pytest", "-v", "--disable-warnings"],
                stdout=open("logs/pytest_output.log", "w"),
                stderr=subprocess.STDOUT
            )

            end = time.time()
            if result.returncode == 0:
                with open("tests/pytest_passed.txt", "w") as f:
                    f.write("ok")
                append_summary("pytest_validation", "passed", end - start, start, end)
                print("All tests passed.")
            else:
                append_summary("pytest_validation", "failed", end - start, start, end)
                print("Tests failed. Check logs/pytest_output.log")
                sys.exit(result.returncode)
