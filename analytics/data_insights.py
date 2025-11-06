"""
CityMind — Data Insights Module
--------------------------------
Análisis exploratorio real del dataset CDC PLACES 2024 (versión limpia).
Genera estadísticas y gráficos interactivos con Plotly.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = "data/processed/final_places.csv"

def load_data():
    """Carga el dataset limpio."""
    df = pd.read_csv(DATA_PATH)
    # Normalizamos columnas importantes
    df.columns = df.columns.str.lower()
    return df


def compute_summary(df):
    """Calcula métricas nacionales promedio."""
    return {
        "avg_mhlth": round(df["mhlth_crudeprev"].mean(), 2),
        "avg_depression": round(df["depression_crudeprev"].mean(), 2),
        "correlation": round(df["mhlth_crudeprev"].corr(df["depression_crudeprev"]), 3),
        "n_counties": df.shape[0],
        "last_year": int(df["year"].max()) if "year" in df.columns else 2024,
    }


def top_bottom_counties(df, col, n=5):
    """Devuelve los 5 condados con mayor y menor prevalencia en una métrica."""
    top = df.nlargest(n, col)[["name", "stateabbr", col]]
    bottom = df.nsmallest(n, col)[["name", "stateabbr", col]]
    return top, bottom


def choropleth_map(df, col):
    """Genera un mapa coroplético de EE.UU. (por condado)."""
    fig = px.choropleth(
        df,
        geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
        locations="locationname",  # o usa "fips" si está en el CSV
        color=col,
        color_continuous_scale="YlGnBu",
        scope="usa",
        labels={col: col.replace("_", " ").title()},
        hover_data=["name", "stateabbr"],
        title=f"{col.replace('_', ' ').title()} — U.S. Counties",
    )
    fig.update_layout(height=500, margin={"r":0, "t":50, "l":0, "b":0})
    return fig.to_html(full_html=False)


def correlation_heatmap(df):
    """Heatmap de correlaciones de factores clave."""
    selected = df[[
        "mhlth_crudeprev", "depression_crudeprev", "obesity_crudeprev",
        "sleep_crudeprev", "access2_crudeprev", "ghlth_crudeprev",
        "lpa_crudeprev", "phlth_crudeprev"
    ]]
    corr = selected.corr().round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlación entre factores socio-saludables",
    )
    fig.update_layout(height=600)
    return fig.to_html(full_html=False)


def generate_all_insights():
    """Función principal — ejecuta todo el análisis y devuelve resultados listos para Django."""
    df = load_data()
    summary = compute_summary(df)
    top_mhlth, bottom_mhlth = top_bottom_counties(df, "mhlth_crudeprev")
    top_dep, bottom_dep = top_bottom_counties(df, "depression_crudeprev")

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
