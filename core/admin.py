from django.contrib import admin
from .models import PlaceRecord, ModelMetrics, ComparisonSummary, Prediction


# ======================================================
# CONFIGURACIÓN DEL ADMIN
# ======================================================

@admin.register(PlaceRecord)
class PlaceRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "population", "year")
    search_fields = ("name", "state", "fips")
    list_filter = ("state", "year")
    ordering = ("state", "name")


@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = (
        "model_name",
        "target",
        "dataset_type",   # 👈 nuevo campo visible
        "r2_score",
        "mae",
        "rmse",
        "timestamp",
    )
    search_fields = ("model_name", "target")
    list_filter = ("target", "dataset_type")  # 👈 permite filtrar por tipo de dataset
    ordering = ("-timestamp",)


@admin.register(ComparisonSummary)
class ComparisonSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "target",
        "dataset_type",   # 👈 nuevo campo visible
        "best_model",
        "best_r2",
        "best_mae",
        "best_rmse",
        "comparison_date",
    )
    list_filter = ("target", "dataset_type")  # 👈 permite filtrar por tipo de dataset
    ordering = ("-comparison_date",)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("place", "model_used", "target", "predicted_value", "prediction_date")
    search_fields = ("place__name", "model_used", "target")
    list_filter = ("model_used", "target")
    ordering = ("-prediction_date",)
