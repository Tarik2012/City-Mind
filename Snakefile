# ======================================================
# 🧠 CityMind - Snakemake Pipeline (versión estable)
# Pipeline completo: Wrangling → Training → Comparison → Testing
# ======================================================

import os

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
    shell:
        """
        python scripts/common/01_wrangling_final.py
        """

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
    shell:
        """
        python scripts/no_social/04_train_models.py
        python scripts/full_social/04_train_models_full_social.py
        """

# ------------------------------------------------------
# 3️⃣ Comparación de resultados
# ------------------------------------------------------
rule compare_results:
    input:
        "data/interim/no_social/model_metrics.csv",
        "data/interim/full_social/model_metrics.csv"
    output:
        "data/interim/comparison/comparison_summary.csv"
    shell:
        """
        python scripts/comparison/05_compare_results.py
        """

# ------------------------------------------------------
# 4️⃣ Pruebas automáticas con pytest
# ------------------------------------------------------
rule test:
    input:
        "data/interim/comparison/comparison_summary.csv"
    output:
        "tests/pytest_passed.txt"
    run:
        import subprocess, sys, os

        os.makedirs("logs", exist_ok=True)
        print("Running pytest...")

        # Ejecutar pytest y guardar salida
        result = subprocess.run(
            ["pytest", "-v", "--disable-warnings"],
            stdout=open("logs/pytest_output.log", "w"),
            stderr=subprocess.STDOUT
        )

        # Si pasa todo, crea el archivo marcador
        if result.returncode == 0:
            with open("tests/pytest_passed.txt", "w") as f:
                f.write("ok")
            print("✅ All tests passed.")
        else:
            print("❌ Tests failed. Check logs/pytest_output.log")
            sys.exit(result.returncode)
