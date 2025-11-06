"""
CityMind - Automated EDA Report Generator
-----------------------------------------
Ejecuta el módulo de análisis 'data_insights' y guarda un informe HTML
completo con todas las visualizaciones y métricas del dataset limpio.
"""

from analytics.data_insights import generate_all_insights
import os

OUTPUT_PATH = "reports/data_insights.html"

def main():
    print("🔍 Generando informe de análisis exploratorio (EDA)...")
    insights = generate_all_insights()

    # Construir un informe HTML simple
    html_content = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>CityMind Data Insights Report</title>
    </head>
    <body style="font-family: Arial; margin: 40px;">
        <h1 style="color:#16a34a;">🧠 CityMind — Data Insights Report</h1>
        <p><b>Total counties:</b> {insights['summary']['n_counties']}</p>
        <p><b>Average poor mental health:</b> {insights['summary']['avg_mhlth']}%</p>
        <p><b>Average depression:</b> {insights['summary']['avg_depression']}%</p>
        <p><b>Correlation (mental health ↔ depression):</b> {insights['summary']['correlation']}</p>

        <h2>🌎 Poor Mental Health Map</h2>
        {insights['map_mhlth']}

        <h2>🌎 Depression Map</h2>
        {insights['map_dep']}

        <h2>📈 Correlation Heatmap</h2>
        {insights['heatmap']}

        <h2>🏆 Top 5 Counties (Mental Health)</h2>
        <ul>
        {''.join([f"<li>{x['name']} ({x['stateabbr']}) — {x['mhlth_crudeprev']:.2f}%</li>" for x in insights['top_mhlth']])}
        </ul>

        <h2>⚠️ Bottom 5 Counties (Mental Health)</h2>
        <ul>
        {''.join([f"<li>{x['name']} ({x['stateabbr']}) — {x['mhlth_crudeprev']:.2f}%</li>" for x in insights['bottom_mhlth']])}
        </ul>

        <h2>🏆 Top 5 Counties (Depression)</h2>
        <ul>
        {''.join([f"<li>{x['name']} ({x['stateabbr']}) — {x['depression_crudeprev']:.2f}%</li>" for x in insights['top_dep']])}
        </ul>

        <h2>⚠️ Bottom 5 Counties (Depression)</h2>
        <ul>
        {''.join([f"<li>{x['name']} ({x['stateabbr']}) — {x['depression_crudeprev']:.2f}%</li>" for x in insights['bottom_dep']])}
        </ul>

        <p style="margin-top:40px;color:gray;">Generated automatically by CityMind analytics pipeline.</p>
    </body>
    </html>
    """

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Reporte generado: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
