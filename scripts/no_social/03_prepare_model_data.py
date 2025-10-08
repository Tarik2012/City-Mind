# ======================================================
# 🧩 CityMind - 03 Prepare Model Data (No Social)
# Combina datasets limpios con features seleccionadas (Lasso)
# para crear los datasets de modelado finales.
# ======================================================

import pandas as pd
from pathlib import Path

# ======================================================
# 1️⃣ Configuración general
# ======================================================
PROCESSED_DIR = Path("data/processed/no_social")
INTERIM_DIR = Path("data/interim/no_social")
OUT_DIR = PROCESSED_DIR  # guardamos en el mismo sitio (como full_social)
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "depression_crudeprev": "features_lasso_depression.csv",
    "mhlth_crudeprev": "features_lasso_mhlth.csv"
}

BASE_DATA = PROCESSED_DIR / "places_no_social_clean.csv"

print(f"📂 Cargando dataset base: {BASE_DATA.resolve()}")
df_base = pd.read_csv(BASE_DATA, low_memory=False)
print("✅ Dataset cargado:", df_base.shape)

# 💡 Eliminar posibles columnas duplicadas
df_base = df_base.loc[:, ~df_base.columns.duplicated()]

# ======================================================
# 2️⃣ Función auxiliar
# ======================================================
def prepare_dataset(df, target_col, features_file):
    print(f"\n==============================")
    print(f"🎯 Preparando dataset para: {target_col}")
    print("==============================")

    # Leer features seleccionadas
    feat_path = INTERIM_DIR / features_file
    if not feat_path.exists():
        raise FileNotFoundError(f"❌ No se encontró {feat_path}")

    df_feat = pd.read_csv(feat_path)
    if "feature" not in df_feat.columns:
        raise KeyError(f"❌ No se encontró columna 'feature' en {features_file}")

    features = df_feat["feature"].tolist()
    print(f"📊 Total features seleccionadas: {len(features)}")

    # Verificar que existan en el dataset base
    features_valid = [f for f in features if f in df.columns]
    if len(features_valid) == 0:
        raise ValueError(f"❌ Ninguna feature de {features_file} está en el dataset base.")
    print(f"✅ Features válidas en el dataset: {len(features_valid)}")

    # Construir dataset final
    df_model = df[features_valid + [target_col]]

    # Guardar dataset final
    out_path = OUT_DIR / f"model_data_{target_col}.csv"
    df_model.to_csv(out_path, index=False)
    print(f"💾 Guardado: {out_path.name} ({df_model.shape})")

    return {"target": target_col, "rows": df_model.shape[0], "cols": df_model.shape[1]}

# ======================================================
# 3️⃣ Ejecutar para cada target
# ======================================================
summary = []
for target, feat_file in TARGETS.items():
    info = prepare_dataset(df_base, target, feat_file)
    summary.append(info)

# ======================================================
# 4️⃣ Guardar resumen
# ======================================================
summary_df = pd.DataFrame(summary)
summary_path = OUT_DIR / "model_data_summary.csv"
summary_df.to_csv(summary_path, index=False)

print("\n📊 Resumen de datasets generados:")
print(summary_df)
print(f"\n💾 Guardado resumen en: {summary_path.name}")

print("\n✅ Generación de datasets de modelado (No Social) completada con éxito.")
