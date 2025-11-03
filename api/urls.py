from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import (
    PlaceRecordViewSet,
    ModelMetricsViewSet,
    ComparisonSummaryViewSet,
    PredictionViewSet,
)
from .views import PredictView

# 1️⃣ Router DRF (para CRUDs y endpoints "latest")
router = DefaultRouter()
router.register(r'places', PlaceRecordViewSet)
router.register(r'metrics', ModelMetricsViewSet)
router.register(r'comparisons', ComparisonSummaryViewSet)
router.register(r'predictions', PredictionViewSet)

# 2️⃣ Endpoint personalizado de predicción
urlpatterns = [
    path("predict/", PredictView.as_view(), name="predict"),
]

# 3️⃣ Combinar ambos grupos de rutas
urlpatterns += router.urls
