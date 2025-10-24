# ======================================================
# CityMind - 04 Train Models (No Social)
# Entrena modelos (PCA, LassoCV, RandomForest, XGBoost)
# para depresión y distress SIN variables sociales
# ======================================================

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import time
import importlib.util, sys

# ======================================================
# 0. Integración con Monitoring (módulo 10)
# ======================================================
spec = importlib.util.spec_from_file_location(
    "monitoring",
    Path("scripts/common/10_monitoring_logging.py")
)
monitoring = importlib.util.module_from_spec(spec)
sys.modules["monitoring"] = monitoring
spec.loader.exec_module(monitoring)
PipelineStep = monitoring.PipelineStep
logger = monitoring.logger

step = PipelineStep("Train Models - No Social")

try:
    # ======================================================
    # 1. Configuración general
    # ======================================================
    DATA_DIR = Path("data/processed/no_social")
    OUT_DIR = Path("data/interim/no_social")
    MODELS_DIR = Path("models")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    DATASETS = {
        "depression_crudeprev": DATA_DIR / "model_data_depression_crudeprev.csv",
        "mhlth_crudeprev": DATA_DIR / "model_data_mhlth_crudeprev.csv"
    }

    # ======================================================
    # 2. Función para evaluar modelos
    # ======================================================
    def evaluate_model(name, y_true, y_pred):
        return {
            "model": name,
            "r2": round(r2_score(y_true, y_pred), 4),
            "rmse": round(mean_squared_error(y_true, y_pred, squared=False), 4),
            "mae": round(mean_absolute_error(y_true, y_pred), 4)
        }

    # ======================================================
    # 3. Integración con MLflow Tracking (módulo 11)
    # ======================================================
    try:
        spec = importlib.util.spec_from_file_location(
            "mlflow_tracker",
            Path("scripts/common/11_mlflow_tracking.py")
        )
        mlflow_tracker = importlib.util.module_from_spec(spec)
        sys.modules["mlflow_tracker"] = mlflow_tracker
        spec.loader.exec_module(mlflow_tracker)
        CityMindTracker = mlflow_tracker.CityMindTracker
        tracker = CityMindTracker()
    except Exception as e:
        tracker = None
        logger.warning(f"No se pudo importar MLflow Tracker: {e}")

    # ======================================================
    # 4. Entrenamiento
    # ======================================================
    results = []

    for target, path in DATASETS.items():
        print("\n==============================")
        print(f"Entrenando modelos (No Social) para: {target}")
        print("==============================")

        if not path.exists():
            logger.warning(f"Dataset no encontrado: {path}")
            continue

        df = pd.read_csv(path)
        X = df.drop(columns=[target])
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        pca = PCA(n_components=0.95, random_state=42)
        X_train_pca = pca.fit_transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)
        print(f"PCA → {pca.n_components_} componentes (95% varianza)")

        # LassoCV
        lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
        lasso.fit(X_train_scaled, y_train)
        y_pred_lasso = lasso.predict(X_test_scaled)
        metrics_lasso = evaluate_model("LassoCV", y_test, y_pred_lasso)
        metrics_lasso["target"] = target
        metrics_lasso["pca_components"] = pca.n_components_
        results.append(metrics_lasso)

        # Random Forest
        rf = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        metrics_rf = evaluate_model("RandomForest", y_test, y_pred_rf)
        metrics_rf["target"] = target
        metrics_rf["pca_components"] = pca.n_components_
        results.append(metrics_rf)

        # XGBoost
        xgb = XGBRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        xgb.fit(X_train, y_train)
        y_pred_xgb = xgb.predict(X_test)
        metrics_xgb = evaluate_model("XGBoost", y_test, y_pred_xgb)
        metrics_xgb["target"] = target
        metrics_xgb["pca_components"] = pca.n_components_
        results.append(metrics_xgb)

        # Guardar modelo XGBoost final
        if target == "depression_crudeprev":
            joblib.dump(xgb, MODELS_DIR / "xgboost_no_social_depression.joblib")
        elif target == "mhlth_crudeprev":
            joblib.dump(xgb, MODELS_DIR / "xgboost_no_social_mhlth.joblib")

    # ======================================================
    # 5. Guardar métricas
    # ======================================================
    df_results = pd.DataFrame(results)[["target", "model", "r2", "rmse", "mae", "pca_components"]]
    out_path = OUT_DIR / "model_metrics.csv"
    df_results.to_csv(out_path, index=False)
    logger.info(f"Métricas guardadas en {out_path}")

    # Fin exitoso del paso
    step.end(status="SUCCESS", message="Entrenamiento No Social completado correctamente.")

except Exception as e:
    # Si algo falla, registrar error
    step.end(status="FAILED", message=str(e))
    raise
