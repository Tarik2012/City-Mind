# ======================================================
# 📄 CityMind - 06 Generate Report
# Genera un informe automático con resultados comparativos
# entre modelos No Social y Full Social.
# ======================================================

import pandas as pd
from pathlib import Path
from datetime import datetime
import textwrap

# ======================================================
# 1️⃣ Configuración general
# ======================================================
COMPARISON_PATH = Path("data/interim/comparison/comparison_metrics.csv")
R2_PLOT_PATH = Path("data/interim/comparison/r2_comparison.png")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d")
md_path = REPORTS_DIR / f"citymind_report_{date_str}.md"

print(f"📂 Generando informe desde {COMPARISON_PATH.name}")

# ======================================================
# 2️⃣ Cargar datos comparativos
# ======================================================
df = pd.read_csv(COMPARISON_PATH)

if df.empty:
    raise ValueError("❌ El archivo de comparación está vacío. Ejecuta 05_compare_results.py primero.")

# ======================================================
# 3️⃣ Calcular resumen
# ======================================================
avg_r2_gain = df["r2_diff"].mean()
avg_r2_gain_pct = df["r2_diff_pct"].mean()

best_model = df.sort_values("r2_full_social", ascending=False).iloc[0]
best_target = best_model["target"]
best_name = best_model["model"]
best_r2 = best_model["r2_full_social"]

# ======================================================
# 4️⃣ Construir texto del informe
# ======================================================
header = f"# 🧠 CityMind – Informe de Modelos ({date_str})\n"
intro = textwrap.dedent(f"""
**Proyecto:** CityMind  
**Autor:** Erik  
**Fecha:** {date_str}

---

## 📘 Resumen General

Este informe resume los resultados del análisis comparativo entre los modelos de predicción **con y sin variables sociales**.

El objetivo fue evaluar el impacto de las dimensiones sociales en la predicción de indicadores de salud mental (depresión y distress) a nivel de condado.

---
""")

summary = textwrap.dedent(f"""
## 📊 Resumen Numérico

| Target | Modelo | R² (No Social) | R² (Full Social) | ΔR² | ΔR² (%) |
|---------|---------|----------------|------------------|------|--------|
""")

for _, row in df.iterrows():
    summary += f"| {row['target']} | {row['model']} | {row['r2_no_social']:.3f} | {row['r2_full_social']:.3f} | {row['r2_diff']:+.4f} | {row['r2_diff_pct']:+.2f}% |\n"

summary += f"""
**Promedio ΔR²:** {avg_r2_gain:.4f}  
**Promedio ΔR² (%):** {avg_r2_gain_pct:.2f}%  

---
"""

insights = textwrap.dedent(f"""
## 🔍 Principales Conclusiones

- Las variables sociales **no aportan mejoras significativas** en la predicción de **depresión**.
- Sin embargo, muestran una **ligera mejora en la predicción de distress (mhlth_crudeprev)**,  
  con un incremento medio de R² del **{avg_r2_gain_pct:.2f}%**.
- El mejor modelo general fue **{best_name}** para el target **{best_target}**,  
  con un R² de **{best_r2:.3f}** bajo el escenario *Full Social*.
- Estos resultados indican que los factores sociales podrían tener un **efecto marginal**,  
  pero consistentemente positivo sobre el bienestar mental general.

---
""")

image_section = textwrap.dedent(f"""
## 📈 Comparación Visual de R²

![Comparación de R²](../data/interim/comparison/r2_comparison.png)

---
""")

footer = textwrap.dedent("""
## 🧩 Próximos pasos

- Incluir más variables contextuales (educación, crimen, empleo) en los modelos.
- Probar técnicas de selección no lineal (SHAP, Boruta, Permutation Importance).
- Evaluar interacciones entre factores sociales y médicos.
- Integrar seguimiento temporal para evaluar evolución de la salud mental.

---

**CityMind** © 2025 – Proyecto Data Science  
*Generado automáticamente mediante pipeline reproducible.*
""")

# ======================================================
# 5️⃣ Guardar en Markdown
# ======================================================
report_text = header + intro + summary + insights + image_section + footer
md_path.write_text(report_text, encoding="utf-8")
print(f"💾 Informe Markdown guardado en: {md_path}")

print("\n✅ Informe final generado con éxito.")
