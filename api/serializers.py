from rest_framework import serializers
from core.models import Prediction, PlaceRecord, ModelMetrics, ComparisonSummary


# ======================================================
# 🔹 Serializer para PlaceRecord
# ======================================================
class PlaceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceRecord
        fields = ["id", "fips", "name", "state", "population", "latitude", "longitude", "year"]


# ======================================================
# 🔹 Serializer para ModelMetrics
# ======================================================
class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = ["id", "model_name", "target", "r2_score", "mae", "rmse", "timestamp"]


# ======================================================
# 🔹 Serializer para ComparisonSummary
# ======================================================
class ComparisonSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonSummary
        fields = ["id", "target", "best_model", "best_r2", "best_mae", "best_rmse", "comparison_date"]


# ======================================================
# 🔹 Serializer para Prediction
# ======================================================
class PredictionSerializer(serializers.ModelSerializer):
    """
    Serializador flexible:
    - Si la predicción está ligada a un PlaceRecord → lo incluye.
    - Si viene de una predicción directa (sin lugar) → lo omite sin error.
    """
    place = PlaceRecordSerializer(read_only=True)
    input_vector = serializers.JSONField()

    class Meta:
        model = Prediction
        fields = [
            "id",
            "place",
            "model_used",
            "target",
            "predicted_value",
            "input_vector",
            "prediction_date",
        ]
