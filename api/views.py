import joblib
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Prediction
from api.serializers import PredictionSerializer
from scripts.common.feature_expansion import expand_features  # traductor de features resumidas


class PredictView(APIView):
    """
    CityMind - PredictView
    -----------------------
    Genera una predicción a partir de 8–9 features simplificadas de la interfaz.
    Internamente expande esas features a las ~45 columnas que el modelo espera.
    """

    def post(self, request):
        try:
            # ======================================================
            # 1️⃣ Recibir el vector simplificado desde la interfaz
            # ======================================================
            proxy_data = request.data  # Diccionario con health_index, economy_index, etc.

            if not proxy_data:
                return Response(
                    {"error": "No se recibieron datos de entrada."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # ======================================================
            # 2️⃣ Expandir las features a las columnas originales
            # ======================================================
            expanded_row = expand_features(proxy_data)
            X = pd.DataFrame([expanded_row])

            # ======================================================
            # 3️⃣ Seleccionar modelo según 'target' y 'use_social'
            # ======================================================
            target = proxy_data.get("target", "mhlth_crudeprev")
            use_social = bool(proxy_data.get("use_social", True))

            if target not in ["mhlth_crudeprev", "depression_crudeprev"]:
                return Response(
                    {"error": "Target no válido. Usa 'mhlth_crudeprev' o 'depression_crudeprev'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            prefix = "xgboost_full_social" if use_social else "xgboost_no_social"
            # Separa correctamente el nombre del target (mhlth o depression)
            model_suffix = target.split("_")[0]
            model_path = f"models/{prefix}_{model_suffix}.joblib"

            # ======================================================
            # 4️⃣ Cargar modelo y generar predicción
            # ======================================================
            try:
                model = joblib.load(model_path)
            except FileNotFoundError:
                return Response(
                    {"error": f"No se encontró el modelo en: {model_path}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            y_pred = float(model.predict(X)[0])  # Valor escalar

            # ======================================================
            # 5️⃣ Guardar predicción en la base de datos
            # ======================================================
            prediction = Prediction.objects.create(
                model_used=model_path,
                target=target,
                predicted_value=y_pred,
                input_vector=proxy_data,
            )

            # ======================================================
            # 6️⃣ Devolver respuesta al cliente
            # ======================================================
            serializer = PredictionSerializer(prediction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Captura general de errores inesperados
            return Response(
                {"error": f"Error interno en la predicción: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
