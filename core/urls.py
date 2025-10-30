from rest_framework.routers import DefaultRouter
from .views import (
    PlaceRecordViewSet,
    ModelMetricsViewSet,
    ComparisonSummaryViewSet,
    PredictionViewSet,
)

router = DefaultRouter()
router.register(r'places', PlaceRecordViewSet)
router.register(r'metrics', ModelMetricsViewSet)
router.register(r'comparisons', ComparisonSummaryViewSet)
router.register(r'predictions', PredictionViewSet)

urlpatterns = router.urls
