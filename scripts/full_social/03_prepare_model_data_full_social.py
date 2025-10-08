# ======================================================
# 🧠 CityMind - 03 Prepare Model Data (Full Social)
# Genera datasets de modelado a partir de las features seleccionadas por Lasso
# ======================================================

import pandas as pd
from pathlib import Path

# ======================================================
# 1️⃣ Configuración general
# ======================================================
DATA_PATH = Path("data/processed/full_social/places_imputed_full_clean.csv")
LASSO_DIR = Path("data/interim/full_social")
OUT_DIR = Path("data/processed/full_social")  # 👈 sin carpetas nuevas

OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = ["depression_crudeprev", "mhlth_crudeprev"]

print(f"📂 Cargando dataset base desde: {DATA_PATH.resolve()}")
df = pd.read_csv(DATA_PATH, low_memory=False)

# 💡 Eliminar posibles columnas duplicadas
df = df.loc[:, ~df.columns.duplicated()]
print(f"✅ Dataset base cargado: {df.shape}")

# ======================================================
# 2️⃣ Generar datasets según features seleccionadas
# ======================================================
for target in TARGETS:
    print(f"\n==============================")
    print(f"🎯 Preparando dataset para: {target}")
    print("==============================")

    # Cargar features seleccionadas por Lasso
    lasso_path = LASSO_DIR / f"features_lasso_{target.replace('_crudeprev', '')}.csv"
    if not lasso_path.exists():
        print(f"⚠️ No se encontró {lasso_path.name}, se omite.")
        continue

    lasso_features = pd.read_csv(lasso_path)["feature"].tolist()

    # Construir dataset final
    selected_cols = lasso_features + [target]
    model_df = df[selected_cols].dropna(subset=[target]).reset_index(drop=True)
    print(f"✅ Dataset para {target}: {model_df.shape[0]} filas, {model_df.shape[1]} columnas")

    # Guardar dataset directamente en full_social/
    output_path = OUT_DIR / f"model_data_{target}.csv"
    model_df.to_csv(output_path, index=False)
    print(f"💾 Guardado: {output_path.name}")

# ======================================================
# 3️⃣ Resumen general
# ======================================================
print("\n📊 Datasets de modelado generados correctamente en:")
print(f"   {OUT_DIR.resolve()}")
print("\n✅ Preparación completada con éxito.")
