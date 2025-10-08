# ======================================================
# 🔍 CityMind - 02 Feature Selection (Full Social)
# Selección de variables relevantes para Depresión y Distress
# desde el dataset con variables sociales imputadas
# ======================================================

import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from pathlib import Path
import json

# ======================================================
# 1️⃣ Configuración general
# ======================================================
DATA_PATH = Path("data/processed/full_social/places_imputed_full_clean.csv")
OUT_DIR = Path("data/interim/full_social")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = ["depression_crudeprev", "mhlth_crudeprev"]

print(f"📂 Leyendo dataset limpio desde: {DATA_PATH.resolve()}")
df = pd.read_csv(DATA_PATH, low_memory=False)

# 💡 Eliminar posibles columnas duplicadas (por seguridad)
if df.columns.duplicated().any():
    dup_cols = df.columns[df.columns.duplicated()].tolist()
    print(f"⚠️ Columnas duplicadas eliminadas: {dup_cols}")
    df = df.loc[:, ~df.columns.duplicated()]

print(f"✅ Dataset cargado: {df.shape}")

# ======================================================
# 2️⃣ Selección de columnas numéricas
# ======================================================
df_num = df.select_dtypes(include=[np.number])
print(f"📊 Variables numéricas: {df_num.shape[1]}")

# ======================================================
# 3️⃣ Funciones auxiliares
# ======================================================
def select_by_correlation(df, target, threshold=0.3):
    """Selecciona variables correlacionadas con el target."""
    corr = df.corr(numeric_only=True)[target].dropna().sort_values(key=abs, ascending=False)
    selected = corr[abs(corr) > threshold].index.tolist()
    return selected, corr.to_dict()

def select_by_lasso(df, target):
    """Selecciona variables mediante LassoCV con limpieza de NaN y target 1D asegurado."""
    # 1️⃣ Eliminar filas con NaN en el target
    df = df.dropna(subset=[target]).copy().reset_index(drop=True)

    # 2️⃣ Separar X, y
    X = df.drop(columns=[target])
    
    # Asegurar que y sea un vector 1D, no un DataFrame
    y = df[target]
    if isinstance(y, pd.DataFrame):
        y = y.iloc[:, 0]

    # 3️⃣ Imputar nulos en X
    X = X.fillna(X.mean())

    # 4️⃣ Verificar tamaños iguales
    assert len(X) == len(y), f"Tamaños no coinciden: X={len(X)}, y={len(y)}"

    # 5️⃣ Entrenar modelo LassoCV
    model = LassoCV(cv=5, random_state=42, max_iter=10000)
    model.fit(X, y)

    coef = pd.Series(model.coef_, index=X.columns)
    selected = coef[coef != 0].index.tolist()
    return selected, coef

# ======================================================
# 4️⃣ Bucle para cada target
# ======================================================
summary_records = []

for target in TARGETS:
    print("\n==============================")
    print(f"🎯 Target: {target}")
    print("==============================")

    # --- Correlación ---
    corr_features, corr_dict = select_by_correlation(df_num, target, threshold=0.3)
    corr_path = OUT_DIR / f"features_corr_{target}.json"
    with open(corr_path, "w") as f:
        json.dump(corr_dict, f, indent=2)
    print(f"💾 Guardadas correlaciones en {corr_path.name} ({len(corr_features)} features)")

    # --- Lasso ---
    cols_for_lasso = [c for c in corr_features if c in df.columns] + [target]
    if len(cols_for_lasso) <= 1:
        print(f"⚠️ No hay suficientes columnas correlacionadas para ejecutar Lasso en {target}.")
        continue

    try:
        lasso_features, lasso_coef = select_by_lasso(df[cols_for_lasso], target)
    except Exception as e:
        print(f"❌ Error en Lasso para {target}: {e}")
        continue

    lasso_path = OUT_DIR / f"features_lasso_{target.replace('_crudeprev', '')}.csv"
    pd.DataFrame({"feature": lasso_features, "coef": lasso_coef[lasso_features]}).to_csv(lasso_path, index=False)
    print(f"💾 Guardadas features Lasso en {lasso_path.name} ({len(lasso_features)} features)")

    # --- Resumen individual ---
    summary_records.append({
        "target": target,
        "corr_features": len(corr_features),
        "lasso_features": len(lasso_features),
        "corr_file": corr_path.name,
        "lasso_file": lasso_path.name
    })

# ======================================================
# 5️⃣ Guardar resumen general
# ======================================================
summary_df = pd.DataFrame(summary_records)
summary_path = OUT_DIR / "feature_selection_summary.csv"
summary_df.to_csv(summary_path, index=False)

print(f"\n📊 Resumen general guardado en {summary_path}")
print(summary_df)
print("\n✅ Selección de variables (Full Social) completada con éxito.")
