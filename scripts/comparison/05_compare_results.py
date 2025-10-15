# ======================================================
# 📊 CityMind - 05 Compare Results
# Compara el rendimiento de modelos entre escenarios:
# "No Social" vs "Full Social" con ΔR²%
# ======================================================

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import logging
import sys

# ======================================================
# 1️⃣ Configuración general + Logging
# ======================================================
OUT_DIR = Path("data/interim/comparison")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuración del logger
log_path = OUT_DIR / "comparison.log"
logger = logging.getLogger("comparison_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("🚀 Iniciando comparación de resultados CityMind")

NO_SOCIAL_PATH = Path("data/interim/no_social/model_metrics.csv")
FULL_SOCIAL_PATH = Path("data/interim/full_social/model_metrics.csv")

logger.info(f"📂 Leyendo resultados desde:")
logger.info(f"   • No Social → {NO_SOCIAL_PATH.resolve()}")
logger.info(f"   • Full Social → {FULL_SOCIAL_PATH.resolve()}")

# ======================================================
# 2️⃣ Cargar datasets
# ======================================================
df_no = pd.read_csv(NO_SOCIAL_PATH)
df_full = pd.read_csv(FULL_SOCIAL_PATH)

required_cols = {"target", "model", "r2", "rmse", "mae"}
for name, df in {"No Social": df_no, "Full Social": df_full}.items():
    missing = required_cols - set(df.columns)
    if missing:
        logger.error(f"❌ Faltan columnas {missing} en {name}")
        raise ValueError(f"❌ Faltan columnas {missing} en {name}")

logger.info("✅ Métricas cargadas correctamente")

# ======================================================
# 3️⃣ Unir datasets (formato ancho)
# ======================================================
merged = pd.merge(
    df_no,
    df_full,
    on=["target", "model"],
    suffixes=("_no_social", "_full_social")
)

# Calcular diferencias
merged["r2_diff"] = merged["r2_full_social"] - merged["r2_no_social"]
merged["r2_diff_pct"] = (merged["r2_diff"] / merged["r2_no_social"]) * 100
merged["rmse_diff"] = merged["rmse_full_social"] - merged["rmse_no_social"]
merged["mae_diff"] = merged["mae_full_social"] - merged["mae_no_social"]

# ======================================================
# 4️⃣ Guardar CSVs (ancho y largo)
# ======================================================

# 📁 1. Formato ancho (para análisis interno)
out_wide = OUT_DIR / "comparison_summary_wide.csv"
merged.to_csv(out_wide, index=False)

# 📁 2. Formato largo (para pytest y visualizaciones simples)
df_long_no = df_no.assign(scenario="No Social")
df_long_full = df_full.assign(scenario="Full Social")
df_long = pd.concat([df_long_no, df_long_full], ignore_index=True)
out_csv = OUT_DIR / "comparison_summary.csv"
df_long.to_csv(out_csv, index=False)

logger.info(f"💾 Guardado resumen comparativo:")
logger.info(f"   • Formato largo  → {out_csv.name}")
logger.info(f"   • Formato ancho  → {out_wide.name}")

# ======================================================
# 5️⃣ Mostrar resumen numérico
# ======================================================
logger.info("📊 Resumen de mejora por modelo:")
summary_table = merged[["target", "model", "r2_no_social", "r2_full_social", "r2_diff", "r2_diff_pct"]]
logger.info("\n" + summary_table.to_string(index=False))

avg_r2_gain = merged["r2_diff"].mean()
avg_r2_gain_pct = merged["r2_diff_pct"].mean()
logger.info(f"\n🔹 Mejora media en R²: {avg_r2_gain:.4f} ({avg_r2_gain_pct:.2f}%)")

# ======================================================
# 6️⃣ Gráfico comparativo de R²
# ======================================================
plt.figure(figsize=(10, 6))
bar_width = 0.35
indices = np.arange(len(merged))

plt.bar(indices - bar_width/2, merged["r2_no_social"], width=bar_width, label="No Social", color="#FFC107")
plt.bar(indices + bar_width/2, merged["r2_full_social"], width=bar_width, label="Full Social", color="#4CAF50")

for i, diff in enumerate(merged["r2_diff_pct"]):
    plt.text(indices[i], max(merged["r2_no_social"][i], merged["r2_full_social"][i]) + 0.005,
             f"Δ{diff:+.2f}%", ha="center", va="bottom", fontsize=9, color="black", fontweight="bold")

plt.xticks(indices, merged["target"] + " - " + merged["model"], rotation=45, ha="right")
plt.ylabel("R² Score")
plt.title("📈 Comparación de R²: No Social vs Full Social")
plt.legend()
plt.tight_layout()

out_plot = OUT_DIR / "r2_comparison.png"
plt.savefig(out_plot, dpi=300)
logger.info(f"🖼️ Gráfico guardado en: {out_plot.name}")

# ======================================================
# 7️⃣ Conclusión
# ======================================================
logger.info("✅ Comparación completada con éxito.")
