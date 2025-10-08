"""
eda_model_validation.py
📊 Validación final de datasets para modelado (CityMind)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================
# 1. Cargar datasets finales
# ==============================
path_dep = "data/processed/model_data_depression_crudeprev.csv"
path_mhlth = "data/processed/model_data_mhlth_crudeprev.csv"

df_dep = pd.read_csv(path_dep)
df_mhlth = pd.read_csv(path_mhlth)

print(f"🧩 Depresión: {df_dep.shape}")
print(f"🧠 Distress: {df_mhlth.shape}")

# ==============================
# 2. Resumen general
# ==============================
for name, df in {"Depresión": df_dep, "Distress": df_mhlth}.items():
    print(f"\n{name} — Estadísticas generales:")
    display(df.describe(include="all"))
    print(f"Valores nulos totales: {df.isna().sum().sum()}")

# ==============================
# 3. Distribución del target
# ==============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df_dep["depression_crudeprev"], bins=30, kde=True, color="blue", ax=axes[0])
axes[0].set_title("Distribución Depresión")

sns.histplot(df_mhlth["mhlth_crudeprev"], bins=30, kde=True, color="green", ax=axes[1])
axes[1].set_title("Distribución Distress")

plt.tight_layout()
plt.show()

# ==============================
# 4. Correlación del target con features
# ==============================
for target, df in [("depression_crudeprev", df_dep), ("mhlth_crudeprev", df_mhlth)]:
    corr = df.corr(numeric_only=True)[target].sort_values(ascending=False)
    print(f"\nTop correlaciones ({target}):")
    print(corr.head(10))
    sns.barplot(x=corr.head(10).values, y=corr.head(10).index)
    plt.title(f"Top correlaciones con {target}")
    plt.show()

# ==============================
# 5. Nulos por columna
# ==============================
nulls = pd.DataFrame({
    "Depression": df_dep.isna().sum(),
    "Distress": df_mhlth.isna().sum()
}).sort_values(by=["Depression", "Distress"], ascending=False)

print("\n📋 Nulos por columna:")
display(nulls.head(15))

# ==============================
# 6. Guardar resumen
# ==============================
summary_path = "data/interim/model_validation_summary.csv"
summary = pd.DataFrame({
    "dataset": ["model_data_depression_crudeprev", "model_data_mhlth_crudeprev"],
    "rows": [df_dep.shape[0], df_mhlth.shape[0]],
    "columns": [df_dep.shape[1], df_mhlth.shape[1]],
    "nulls_total": [df_dep.isna().sum().sum(), df_mhlth.isna().sum().sum()]
})
summary.to_csv(summary_path, index=False)
print(f"\n✅ Resumen guardado en {summary_path}")
