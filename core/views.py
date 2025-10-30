from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import PlaceRecord, ModelMetrics, ComparisonSummary, Prediction
from .serializers import (
    PlaceRecordSerializer,
    ModelMetricsSerializer,
    ComparisonSummarySerializer,
    PredictionSerializer,
)


# ======================================================
#  VIEWSETS PRINCIPALES
# ======================================================

class PlaceRecordViewSet(viewsets.ModelViewSet):
    queryset = PlaceRecord.objects.all().order_by("name")
    serializer_class = PlaceRecordSerializer


class ModelMetricsViewSet(viewsets.ModelViewSet):
    queryset = ModelMetrics.objects.all().order_by("-timestamp")
    serializer_class = ModelMetricsSerializer

    @action(detail=False, methods=["get"])
    def latest(self, request):
        """Devuelve las métricas más recientes"""
        latest_metrics = ModelMetrics.objects.order_by("-timestamp")[:5]
        serializer = self.get_serializer(latest_metrics, many=True)
        return Response(serializer.data)


class ComparisonSummaryViewSet(viewsets.ModelViewSet):
    queryset = ComparisonSummary.objects.all().order_by("-comparison_date")
    serializer_class = ComparisonSummarySerializer

    @action(detail=False, methods=["get"])
    def latest(self, request):
        """Devuelve la última comparación registrada"""
        latest_comparison = ComparisonSummary.objects.order_by("-comparison_date").first()
        serializer = self.get_serializer(latest_comparison)
        return Response(serializer.data)


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all().order_by("-prediction_date")
    serializer_class = PredictionSerializer

    @action(detail=False, methods=["get"])
    def latest(self, request):
        """Devuelve las últimas predicciones generadas"""
        latest_preds = Prediction.objects.order_by("-prediction_date")[:10]
        serializer = self.get_serializer(latest_preds, many=True)
        return Response(serializer.data)
