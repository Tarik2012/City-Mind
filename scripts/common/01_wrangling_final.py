# ======================================================
#  CityMind - 01 Wrangling Final (Wide format, estructurado)
# Limpieza, imputación y generación de datasets base desde CDC PLACES 2024
# ======================================================

import pandas as pd
from pathlib import Path

# ======================================================
# 1️⃣ Configuración general
# ======================================================
RAW_PATH = Path("data/raw/places_county_2024.csv")
BASE_DIR = Path("data/processed")
OUT_NO_SOCIAL = BASE_DIR / "no_social"
OUT_FULL_SOCIAL = BASE_DIR / "full_social"

for folder in [BASE_DIR, OUT_NO_SOCIAL, OUT_FULL_SOCIAL]:
    folder.mkdir(parents=True, exist_ok=True)

if not RAW_PATH.exists():
    raise FileNotFoundError(f"❌ No se encontró el archivo: {RAW_PATH.resolve()}")
else:
    print(f"📂 Cargando datos desde: {RAW_PATH.resolve()}")

# ======================================================
# 2️⃣ Cargar dataset crudo
# ======================================================
df = pd.read_csv(RAW_PATH, low_memory=False)
print("📊 Datos cargados:", df.shape)

# Normalizamos nombres de columnas (mejor práctica)
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

if "countyfips" in df.columns:
    df["countyfips"] = df["countyfips"].astype(str).str.zfill(5)

# ======================================================
# 3️⃣ Seleccionar columnas relevantes (solo crude prevalence)
# ======================================================
cols_meta = [
    "stateabbr", "statedesc", "countyname", "countyfips",
    "totalpopulation", "totalpop18plus"
]
cols_crude = [c for c in df.columns if c.endswith("crudeprev")]
df_clean = df[cols_meta + cols_crude]
print(f"✅ Seleccionadas columnas: {len(df_clean.columns)}")

# ======================================================
# 4️⃣ Imputación social (mediana estatal)
# ======================================================
cols_social = [
    "foodinsecu_crudeprev", "foodstamp_crudeprev", "housinsecu_crudeprev",
    "emotionspt_crudeprev", "isolation_crudeprev",
    "lacktrpt_crudeprev", "shututility_crudeprev"
]

df_imputed = df_clean.copy()
for col in cols_social:
    if col in df_imputed.columns:
        df_imputed[col] = df_imputed.groupby("stateabbr")[col].transform(lambda x: x.fillna(x.median()))

# ======================================================
# 5️⃣ Eliminar sociales
# ======================================================
df_no_social = df_clean.drop(columns=cols_social, errors="ignore")

# ======================================================
# 6️⃣ Eliminar nulos médicos críticos
# ======================================================
cols_med = ["highchol_crudeprev", "cholscreen_crudeprev", "bphigh_crudeprev", "bpmed_crudeprev"]
df_no_social_clean = df_no_social.dropna(subset=cols_med)
df_imputed_clean = df_imputed.dropna(subset=cols_med)

# ======================================================
# 7️⃣ Imputación completa (media nacional)
# ======================================================
df_imputed_full = df_imputed_clean.copy()
for col in cols_crude:
    if col not in cols_meta and df_imputed_full[col].isna().sum() > 0:
        df_imputed_full[col] = df_imputed_full[col].fillna(df_imputed_full[col].mean())

# ======================================================
# 8️⃣ Guardar datasets generales
# ======================================================
outputs = {
    OUT_NO_SOCIAL / "places_no_social_clean.csv": df_no_social_clean,
    OUT_FULL_SOCIAL / "places_imputed_clean.csv": df_imputed_clean,
    OUT_FULL_SOCIAL / "places_imputed_full_clean.csv": df_imputed_full
}

for path, data in outputs.items():
    data.to_csv(path, index=False)
    print(f"💾 Guardado: {path.name} ({data.shape})")

# ======================================================
# 9️⃣ Generar datasets específicos para cada target
# ======================================================
TARGETS = ["depression_crudeprev", "mhlth_crudeprev"]

for target in TARGETS:
    if target not in df_no_social_clean.columns:
        print(f"⚠️ Target {target} no encontrado, se omite.")
        continue

    df_no_social_clean[[target] + [c for c in df_no_social_clean.columns if c != target]].to_csv(
        OUT_NO_SOCIAL / f"model_data_{target}.csv", index=False
    )

    df_imputed_full[[target] + [c for c in df_imputed_full.columns if c != target]].to_csv(
        OUT_FULL_SOCIAL / f"model_data_{target}.csv", index=False
    )

print("📁 Archivos por target creados correctamente.")

# ======================================================
# 🔟 Guardar resumen
# ======================================================
summary = pd.DataFrame([
    {"dataset": path.name, "rows": d.shape[0], "cols": d.shape[1], "nulls": d.isna().sum().sum()}
    for path, d in outputs.items()
])
summary_path = BASE_DIR / "wrangling_summary.csv"
summary.to_csv(summary_path, index=False)
print(f"\n🧾 Resumen guardado en {summary_path}")
print(summary)

# ======================================================
# 🚀 Export final para ingesta
# ======================================================
FINAL_PATH = BASE_DIR / "final_places.csv"
df_imputed_full.to_csv(FINAL_PATH, index=False)
print(f"\n🚀 Dataset final exportado para ingesta → {FINAL_PATH.name} ({df_imputed_full.shape})")
print("\n🎯 Wrangling completado con éxito.")
