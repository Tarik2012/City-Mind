# 🧠 CityMind -- Pipeline README (Resumen Esencial)

Pipeline automatizado con **Snakemake**\
**Flujo completo:** Wrangling → Training → Comparison → Testing →
Ingesta (PostgreSQL/Django)

------------------------------------------------------------------------

## ⚙️ Estructura base del proyecto

    CityMind/
    ├── Snakefile
    ├── data/
    │   ├── raw/places_county_2024.csv
    │   ├── processed/
    │   └── interim/
    ├── scripts/
    │   ├── common/01_wrangling_final.py
    │   ├── no_social/04_train_models.py
    │   ├── full_social/04_train_models_full_social.py
    │   ├── comparison/05_compare_results.py
    │   └── db_ingest/06_ingest_to_postgres.py
    └── logs/

------------------------------------------------------------------------

## 🚀 Objetivo final del workflow

El pipeline produce automáticamente los siguientes resultados finales:

-   `data/interim/no_social/model_metrics.csv`
-   `data/interim/full_social/model_metrics.csv`
-   `data/interim/comparison/comparison_summary.csv`
-   `tests/pytest_passed.txt`
-   `logs/db_ingest_done.txt`

------------------------------------------------------------------------

## 🔧 Comandos Snakemake más importantes

### ▶️ Ejecutar todo el pipeline

``` bash
snakemake -p --cores 1
```

### ♻️ Forzar la ejecución completa (rehacer todo)

``` bash
snakemake -p --cores 1 --forcerun all
```

### 🎯 Forzar solo una regla (por ejemplo, reentrenar modelos)

``` bash
snakemake -p --cores 1 --forcerun train_models
```

### 🔍 Ver comandos shell y más detalle

``` bash
snakemake -p --cores 1 --printshellcmds --verbose
```

### ⏳ Evitar errores por latencia (OneDrive/Windows)

``` bash
snakemake -p --cores 1 --latency-wait 15
```

### 🔓 Desbloquear el workflow si quedó bloqueado

``` bash
snakemake --unlock
```

### 🧪 Simular la ejecución sin correr nada

``` bash
snakemake -n -p
```

------------------------------------------------------------------------

## 🧹 Limpieza del pipeline

### Opción 1: Usar la regla `clean`

``` bash
snakemake -p --cores 1 clean
```

### Opción 2: Limpieza manual (PowerShell)

``` powershell
Remove-Item -Recurse -Force "data/interim" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "data/processed" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "logs" -ErrorAction SilentlyContinue
Remove-Item "tests/pytest_passed.txt" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
```

Y luego:

``` bash
snakemake -p --cores 1 --forcerun all
```

------------------------------------------------------------------------

## ✅ Ejemplo rápido completo

``` bash
snakemake -p --cores 1 --printshellcmds --verbose --latency-wait 20
```

------------------------------------------------------------------------

**Autor:** Equipo CityMind (2025)\
**Propósito:** Documentación rápida del pipeline de orquestación de
datos y modelos.
