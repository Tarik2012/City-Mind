from rest_framework import serializers
from core.models import PlaceRecord, ModelMetrics, ComparisonSummary, Prediction


# ======================================================
#  SERIALIZERS
# ======================================================

class PlaceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceRecord
        fields = '__all__'


class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = '__all__'


class ComparisonSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonSummary
        fields = '__all__'


class PredictionSerializer(serializers.ModelSerializer):
    place = PlaceRecordSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = '__all__'
