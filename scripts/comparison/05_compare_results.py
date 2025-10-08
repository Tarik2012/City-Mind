# ======================================================
# 📊 CityMind - 05 Compare Results
# Compara el rendimiento de modelos entre escenarios:
# "No Social" vs "Full Social" con ΔR²%
# ======================================================

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# ======================================================
# 1️⃣ Configuración general
# ======================================================
NO_SOCIAL_PATH = Path("data/interim/no_social/model_metrics.csv")
FULL_SOCIAL_PATH = Path("data/interim/full_social/model_metrics.csv")
OUT_DIR = Path("data/interim/comparison")
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"📂 Leyendo resultados desde:")
print(f"   • No Social → {NO_SOCIAL_PATH.resolve()}")
print(f"   • Full Social → {FULL_SOCIAL_PATH.resolve()}")

# ======================================================
# 2️⃣ Cargar datasets
# ======================================================
df_no = pd.read_csv(NO_SOCIAL_PATH)
df_full = pd.read_csv(FULL_SOCIAL_PATH)

required_cols = {"target", "model", "r2", "rmse", "mae"}
for name, df in {"No Social": df_no, "Full Social": df_full}.items():
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"❌ Faltan columnas {missing} en {name}")

print("✅ Métricas cargadas correctamente")

# ======================================================
# 3️⃣ Unir datasets
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

# Guardar CSV resumen
out_csv = OUT_DIR / "comparison_metrics.csv"
merged.to_csv(out_csv, index=False)
print(f"💾 Guardado resumen comparativo en: {out_csv.name}")

# ======================================================
# 4️⃣ Mostrar resumen numérico
# ======================================================
print("\n📊 Resumen de mejora por modelo:")
print(merged[["target", "model", "r2_no_social", "r2_full_social", "r2_diff", "r2_diff_pct"]])

avg_r2_gain = merged["r2_diff"].mean()
avg_r2_gain_pct = merged["r2_diff_pct"].mean()
print(f"\n🔹 Mejora media en R²: {avg_r2_gain:.4f} ({avg_r2_gain_pct:.2f}%)")

# ======================================================
# 5️⃣ Gráfico comparativo de R²
# ======================================================
plt.figure(figsize=(10, 6))

# Preparar posiciones
bar_width = 0.35
indices = np.arange(len(merged))
plt.bar(
    indices - bar_width/2,
    merged["r2_no_social"],
    width=bar_width,
    label="No Social",
    color="#FFC107"
)
plt.bar(
    indices + bar_width/2,
    merged["r2_full_social"],
    width=bar_width,
    label="Full Social",
    color="#4CAF50"
)

# Etiquetas ΔR²%
for i, diff in enumerate(merged["r2_diff_pct"]):
    plt.text(
        indices[i],
        max(merged["r2_no_social"][i], merged["r2_full_social"][i]) + 0.005,
        f"Δ{diff:+.2f}%",
        ha="center",
        va="bottom",
        fontsize=9,
        color="black",
        fontweight="bold"
    )

# Formato del gráfico
plt.xticks(indices, merged["target"] + " - " + merged["model"], rotation=45, ha="right")
plt.ylabel("R² Score")
plt.title("📈 Comparación de R²: No Social vs Full Social")
plt.legend()
plt.tight_layout()

# Guardar gráfico
out_plot = OUT_DIR / "r2_comparison.png"
plt.savefig(out_plot, dpi=300)
print(f"🖼️ Gráfico guardado en: {out_plot.name}")

# ======================================================
# 6️⃣ Conclusión
# ======================================================
print("\n✅ Comparación completada con éxito.")
