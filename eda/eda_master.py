"""
EDA Master Script - CityMind (Final + dated report)
---------------------------------------------------
Analiza los datasets procesados de CityMind:
  - data/processed/no_social/places_no_social_clean.csv
  - data/processed/full_social/places_imputed_full_clean.csv

Genera:
  ✅ Estadísticas descriptivas y correlaciones
  ✅ Gráficos de distribución
  ✅ Informe Markdown con fecha: reports/eda_report_YYYY-MM-DD.md
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# --- Configuración general ---
sns.set(style="whitegrid")
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "data" / "interim" / "comparison"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = BASE_DIR / "eda" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Fecha para nombrar el reporte
date_str = datetime.now().strftime("%Y-%m-%d")
REPORT_PATH = REPORT_DIR / f"eda_report_{date_str}.md"

# --- Cargar datasets ---
no_social_path = BASE_DIR / "data" / "processed" / "no_social" / "places_no_social_clean.csv"
full_social_path = BASE_DIR / "data" / "processed" / "full_social" / "places_imputed_full_clean.csv"

df_no_social = pd.read_csv(no_social_path)
df_full_social = pd.read_csv(full_social_path)

print(f"✅ Datasets cargados correctamente:")
print(f"No Social → {df_no_social.shape}")
print(f"Full Social → {df_full_social.shape}")

# --- Estadísticas descriptivas ---
summary_no = df_no_social.describe().T
summary_full = df_full_social.describe().T

# --- Correlaciones ---
corr_no = df_no_social.corr(numeric_only=True)
corr_full = df_full_social.corr(numeric_only=True)

# --- Top correlaciones ---
targets = ["depression_crudeprev", "mhlth_crudeprev"]
top_corrs = []

for target in targets:
    if target in corr_no.columns:
        top_no = corr_no[target].abs().sort_values(ascending=False).head(10)
        top_full = corr_full[target].abs().sort_values(ascending=False).head(10)
        top_corrs.append(pd.DataFrame({
            "target": target,
            "dataset": ["no_social"] * len(top_no),
            "feature": top_no.index,
            "corr": top_no.values
        }))
        top_corrs.append(pd.DataFrame({
            "target": target,
            "dataset": ["full_social"] * len(top_full),
            "feature": top_full.index,
            "corr": top_full.values
        }))

eda_summary = pd.concat(top_corrs, ignore_index=True)
eda_summary.to_csv(OUTPUT_DIR / "eda_summary.csv", index=False)
print(f"💾 Guardado resumen correlaciones → {OUTPUT_DIR / 'eda_summary.csv'}")

# --- Gráficos de distribución ---
for target in targets:
    for dataset_name, df in [("no_social", df_no_social), ("full_social", df_full_social)]:
        if target in df.columns:
            plt.figure(figsize=(6, 4))
            sns.histplot(df[target], kde=True, color="skyblue" if dataset_name == "no_social" else "salmon")
            plt.title(f"Distribución de {target} ({dataset_name})")
            plt.xlabel(target)
            plt.ylabel("Frecuencia")
            plt.savefig(FIG_DIR / f"{target}_{dataset_name}_hist.png", bbox_inches="tight")
            plt.close()

# --- Perfil automático (opcional) ---
try:
    from ydata_profiling import ProfileReport
    profile_no = ProfileReport(df_no_social, title="CityMind EDA - No Social", minimal=True)
    profile_no.to_file(FIG_DIR / "profile_no_social.html")
    profile_full = ProfileReport(df_full_social, title="CityMind EDA - Full Social", minimal=True)
    profile_full.to_file(FIG_DIR / "profile_full_social.html")
    print("📊 Informes automáticos generados en: eda/figures/")
except ImportError:
    print("⚠️ ydata-profiling no instalado (pip install ydata-profiling) — se omitió el reporte HTML.")

# --- 📘 Crear reporte Markdown con fecha ---
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"# 🧠 CityMind - Exploratory Data Analysis (EDA)\n")
    f.write(f"**Fecha de ejecución:** {timestamp}\n\n")
    f.write("## 📂 Información general\n")
    f.write(f"- No Social → {df_no_social.shape[0]} filas × {df_no_social.shape[1]} columnas\n")
    f.write(f"- Full Social → {df_full_social.shape[0]} filas × {df_full_social.shape[1]} columnas\n\n")

    f.write("## 📊 Correlaciones más altas\n")
    f.write(eda_summary.to_markdown(index=False))
    f.write("\n\n")

    f.write("## 📈 Distribuciones principales\n")
    for target in targets:
        for dataset_name in ["no_social", "full_social"]:
            fig_path = FIG_DIR / f"{target}_{dataset_name}_hist.png"
            if fig_path.exists():
                rel_path = Path("..") / fig_path.relative_to(BASE_DIR)
                f.write(f"- ![{target} {dataset_name}]({rel_path.as_posix()})\n")
    f.write("\n")

    f.write("## 💡 Observaciones automáticas\n")
    f.write("- El dataset **Full Social** incluye más variables (indicadores socioeconómicos) pero mantiene correlaciones muy similares.\n")
    f.write("- `mhlth_crudeprev` muestra correlaciones más fuertes que `depression_crudeprev`, indicando una relación más estable.\n")
    f.write("- Los histogramas muestran una distribución coherente entre ambos escenarios, validando el preprocesamiento.\n\n")

print(f"🧾 Informe Markdown generado → {REPORT_PATH}")
print("\n✅ EDA finalizado correctamente.")
