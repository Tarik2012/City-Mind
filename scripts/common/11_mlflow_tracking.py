# ======================================================
# CityMind - 11 MLflow Tracking (solo XGBoost)
# ======================================================

import mlflow
import mlflow.sklearn
from pathlib import Path

class CityMindTracker:
    """Registra métricas en MLflow solo para el modelo XGBoost."""

    def __init__(self, experiment_name="CityMind_Models"):
        project_root = Path(__file__).resolve().parents[2]
        tracking_dir = project_root / "mlruns"
        tracking_uri = f"file:///{tracking_dir.as_posix()}"
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        print(f"MLflow tracking activo en: {tracking_uri}")

    def log_metrics(self, model_name, scenario, metrics_dict, params=None):
        """Solo registra XGBoost en MLflow, ignora otros modelos."""
        if "xgboost" not in model_name.lower():
            return  # se salta LassoCV y RandomForest

        target = None
        if params and "target" in params:
            target = params["target"]

        run_name = f"{model_name}_{scenario}_{target}" if target else f"{model_name}_{scenario}"

        with mlflow.start_run(run_name=run_name):
            mlflow.set_tag("stage", "training")
            mlflow.set_tag("scenario", scenario)
            mlflow.set_tag("model", model_name)
            if target:
                mlflow.set_tag("target", target)

            mlflow.log_param("scenario", scenario)
            mlflow.log_param("model_name", model_name)
            if params:
                for k, v in params.items():
                    mlflow.log_param(k, v)

            for metric, value in metrics_dict.items():
                if isinstance(value, (int, float)):
                    mlflow.log_metric(metric, float(value))

        print(f"Run registrado en MLflow (XGBoost): {run_name}")
