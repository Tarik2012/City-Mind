"""
CityMind — Data Insights Module (for Django Dashboard)
------------------------------------------------------
Genera métricas y gráficos interactivos directamente desde el dataset procesado.
Adaptado a la estructura del pipeline CityMind (usa countyname, stateabbr, countyfips).
"""

import pandas as pd
import plotly.express as px
from pathlib import Path
from django.conf import settings


# Ruta absoluta al dataset generado por Snakemake
DATA_PATH = Path(settings.BASE_DIR) / "data" / "processed" / "final_places.csv"


# =========================================================
# 🧩 Carga y preprocesamiento
# =========================================================
def load_data():
    """Carga el dataset limpio del pipeline."""
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.lower()
    return df


# =========================================================
# 📊 Cálculos principales
# =========================================================
def compute_summary(df):
    """Calcula métricas nacionales promedio."""
    return {
        "avg_mhlth": round(df["mhlth_crudeprev"].mean(), 2),
        "avg_depression": round(df["depression_crudeprev"].mean(), 2),
        "correlation": round(df["mhlth_crudeprev"].corr(df["depression_crudeprev"]), 3),
        "n_counties": df.shape[0],
        "last_year": 2024,
    }


def top_bottom_counties(df, col, n=5):
    """Top & Bottom condados según la métrica, usando countyname y stateabbr."""
    top = df.nlargest(n, col)[["countyname", "stateabbr", col]]
    bottom = df.nsmallest(n, col)[["countyname", "stateabbr", col]]
    return top, bottom


# =========================================================
# 🗺️ Visualizaciones interactivas
# =========================================================
def choropleth_map(df, col):
    """Mapa coroplético de EE.UU. a nivel de condado."""
    if "countyfips" not in df.columns:
        raise ValueError("El dataset no contiene 'countyfips', necesario para el mapa.")

    fig = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations="countyfips",
        color=col,
        color_continuous_scale="YlGnBu",
        scope="usa",
        labels={col: col.replace("_", " ").title()},
        hover_data=["countyname", "stateabbr"],
        title=f"{col.replace('_', ' ').title()} — U.S. Counties",
    )
    fig.update_layout(height=500, margin={"r": 0, "t": 50, "l": 0, "b": 0})
    return fig.to_html(full_html=False)


def correlation_heatmap(df):
    """Heatmap de correlaciones de factores clave."""
    selected = df[
        [
            "mhlth_crudeprev",
            "depression_crudeprev",
            "obesity_crudeprev",
            "sleep_crudeprev",
            "access2_crudeprev",
            "ghlth_crudeprev",
            "lpa_crudeprev",
            "phlth_crudeprev",
        ]
    ]
    corr = selected.corr().round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlación entre factores socio-saludables",
    )
    fig.update_layout(height=600)
    return fig.to_html(full_html=False)


# =========================================================
# 🧠 Función principal
# =========================================================
def generate_all_insights():
    """
    Ejecuta el análisis completo y devuelve resultados listos para el dashboard.
    Retorna un diccionario con:
      - summary: métricas resumen
      - map_mhlth / map_dep: mapas Plotly
      - heatmap: correlación de factores
      - top/bottom: listas de condados extremos
    """
    df = load_data()
    summary = compute_summary(df)

    # Top & Bottom condados
    top_mhlth, bottom_mhlth = top_bottom_counties(df, "mhlth_crudeprev")
    top_dep, bottom_dep = top_bottom_counties(df, "depression_crudeprev")

    # Mapas y heatmap
    map_mhlth = choropleth_map(df, "mhlth_crudeprev")
    map_dep = choropleth_map(df, "depression_crudeprev")
    heatmap = correlation_heatmap(df)

    return {
        "summary": summary,
        "map_mhlth": map_mhlth,
        "map_dep": map_dep,
        "heatmap": heatmap,
        "top_mhlth": top_mhlth.to_dict(orient="records"),
        "bottom_mhlth": bottom_mhlth.to_dict(orient="records"),
        "top_dep": top_dep.to_dict(orient="records"),
        "bottom_dep": bottom_dep.to_dict(orient="records"),
    }
