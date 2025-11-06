from django.shortcuts import render
from django.db.models import Avg
from core.models import PlaceRecord, ModelMetrics, Prediction
from django.utils import timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from pathlib import Path


# ======================================================
#  HOME VIEW — resumen general del sistema CityMind
# ======================================================
def home(request):
    # Total de condados analizados
    total_places = PlaceRecord.objects.count()

    # Cuatro modelos XGBoost (por target y dataset)
    latest_metrics = []
    targets = ["mhlth_crudeprev", "depression_crudeprev"]
    datasets = ["no_social", "full_social"]

    for target in targets:
        for dataset in datasets:
            metric = (
                ModelMetrics.objects.filter(
                    model_name__icontains="xgboost",
                    target=target,
                    dataset_type=dataset,
                )
                .order_by("-timestamp")
                .first()
            )
            if metric:
                latest_metrics.append(metric)

    # Última predicción o actualización del sistema
    last_pred = Prediction.objects.order_by("-prediction_date").first()
    last_update = last_pred.prediction_date if last_pred else timezone.now()

    # Total de predicciones almacenadas
    total_predictions = Prediction.objects.count()

    # Diferencia de rendimiento promedio (social vs no social)
    social_r2 = ModelMetrics.objects.filter(
        dataset_type="full_social", model_name__icontains="xgboost"
    ).aggregate(avg=Avg("r2_score"))["avg"]

    no_social_r2 = ModelMetrics.objects.filter(
        dataset_type="no_social", model_name__icontains="xgboost"
    ).aggregate(avg=Avg("r2_score"))["avg"]

    social_gain = (
        ((social_r2 - no_social_r2) / no_social_r2 * 100)
        if social_r2 and no_social_r2
        else 0
    )

    # 👇 Valor absoluto para evitar filtro |abs en template
    social_gain_abs = abs(social_gain)

    context = {
        "total_places": total_places,
        "latest_metrics": latest_metrics,
        "total_predictions": total_predictions,
        "last_update": last_update,
        "social_gain": social_gain,
        "social_gain_abs": social_gain_abs,
    }

    return render(request, "dashboard/home.html", context)


# ======================================================
#  DASHBOARD VIEW — análisis y visualizaciones con Plotly
# ======================================================
from analytics.data_insights import generate_all_insights


def dashboard_view(request):
    try:
        insights = generate_all_insights()
        print("✅ INSIGHTS LOADED:", insights["summary"])  # ← Log de control
        no_data = False
    except Exception as e:
        print("❌ ERROR LOADING INSIGHTS:", e)
        insights = {}
        no_data = True

    context = {"insights": insights, "no_data": no_data}
    return render(request, "dashboard/dashboard.html", context)




# ======================================================
#  PREDICT VIEW — formulario de predicción
# ======================================================
def predict_view(request):
    return render(request, "dashboard/predict.html")


# ======================================================
#  ABOUT VIEW — información del proyecto
# ======================================================
def about_view(request):
    return render(request, "dashboard/about.html")
