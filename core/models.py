from django.db import models


# ======================================================
#  MODELO BASE (herencia común)
# ======================================================
class BaseModel(models.Model):
    """Campos comunes para todas las tablas"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ======================================================
#  PLACE RECORD
# ======================================================
class PlaceRecord(BaseModel):
    """Información geográfica y demográfica del condado"""
    fips = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    population = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    year = models.IntegerField(default=2024)

    class Meta:
        db_table = "place_record"
        verbose_name = "Place Record"
        verbose_name_plural = "Place Records"

    def __str__(self):
        return f"{self.name}, {self.state}"


# ======================================================
#  MODEL METRICS
# ======================================================
class ModelMetrics(BaseModel):
    """Métricas de evaluación de cada modelo entrenado"""
    DATASET_CHOICES = [
        ("no_social", "No Social"),
        ("full_social", "Full Social"),
    ]

    model_name = models.CharField(max_length=100)
    target = models.CharField(max_length=50)  # 'depression_crudeprev' o 'mhlth_crudeprev'
    dataset_type = models.CharField(max_length=20, choices=DATASET_CHOICES, default="no_social")  # 👈 nuevo campo
    r2_score = models.FloatField(null=True, blank=True)
    mae = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "model_metrics"
        verbose_name = "Model Metrics"
        verbose_name_plural = "Model Metrics"

    def __str__(self):
        return f"{self.model_name} ({self.target}, {self.dataset_type})"


# ======================================================
#  COMPARISON SUMMARY
# ======================================================
class ComparisonSummary(BaseModel):
    """Resumen de comparación entre modelos (por target)"""
    DATASET_CHOICES = [
        ("no_social", "No Social"),
        ("full_social", "Full Social"),
    ]

    target = models.CharField(max_length=50)
    dataset_type = models.CharField(max_length=20, choices=DATASET_CHOICES, default="no_social")  # 👈 nuevo campo
    best_model = models.CharField(max_length=100)
    best_r2 = models.FloatField(null=True, blank=True)
    best_mae = models.FloatField(null=True, blank=True)
    best_rmse = models.FloatField(null=True, blank=True)
    comparison_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comparison_summary"
        verbose_name = "Comparison Summary"
        verbose_name_plural = "Comparison Summaries"

    def __str__(self):
        return f"Best: {self.best_model} ({self.target}, {self.dataset_type})"


# ======================================================
#  PREDICTION
# ======================================================
class Prediction(BaseModel):
    """Predicciones generadas por los modelos"""
    place = models.ForeignKey(
        PlaceRecord,
        on_delete=models.CASCADE,
        related_name="predictions",
        null=True,
        blank=True  # 👈 esto permite crear predicciones sin lugar específico
    )
    model_used = models.CharField(max_length=100)
    target = models.CharField(max_length=50)
    predicted_value = models.FloatField()
    input_vector = models.JSONField()  # guarda features de entrada (8–10 simplificados)
    prediction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "prediction"
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

    def __str__(self):
        if self.place:
            return f"{self.place.name} - {self.model_used} ({self.target})"
        return f"Predicción sin lugar - {self.model_used} ({self.target})"

