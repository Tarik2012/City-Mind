"""
CityMind - Automated Data Insights Generator
--------------------------------------------
Genera análisis exploratorios (EDA) y gráficos HTML para los reportes automáticos del pipeline.
"""

import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_PATH = Path("data/processed/final_places.csv")
REPORT_PATH = Path("reports/data_insights.html")


def generate_html_report():
    df = pd.read_csv(DATA_PATH)
    print(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns")

    # --- Distribución de salud mental
    fig_mhlth = px.histogram(
        df,
        x="mhlth_crudeprev",
        nbins=40,
        title="Distribution of Poor Mental Health Prevalence (%)",
    )

    # --- Correlación depresión vs mala salud mental
    fig_dep = px.scatter(
        df,
        x="mhlth_crudeprev",
        y="depression_crudeprev",
        color="stateabbr" if "stateabbr" in df.columns else None,
        title="Depression vs Poor Mental Health (by County)",
        opacity=0.6,
    )

    # Guardar como HTML
    REPORT_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("<h1>CityMind Data Insights</h1>")
        f.write(fig_mhlth.to_html(full_html=False, include_plotlyjs="cdn"))
        f.write(fig_dep.to_html(full_html=False, include_plotlyjs=False))

    print(f"✅ Report generated at {REPORT_PATH.resolve()}")


if __name__ == "__main__":
    generate_html_report()
