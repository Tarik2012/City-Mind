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

# ======================================================
# 1️⃣ Configuración general
# ======================================================
DATA_DIR = Path("data/processed/no_social")
OUT_DIR = Path("data/interim/no_social")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "depression_crudeprev": DATA_DIR / "model_data_depression_crudeprev.csv",
    "mhlth_crudeprev": DATA_DIR / "model_data_mhlth_crudeprev.csv"
}

# ======================================================
# 2️⃣ Función para evaluar modelos
# ======================================================
def evaluate_model(name, y_true, y_pred):
    return {
        "model": name,
        "r2": round(r2_score(y_true, y_pred), 4),
        "rmse": round(mean_squared_error(y_true, y_pred, squared=False), 4),
        "mae": round(mean_absolute_error(y_true, y_pred), 4)
    }

# ======================================================
# 3️⃣ Integración con MLflow Tracking (módulo 11)
# ======================================================
try:
    import importlib.util, sys, pathlib
    spec = importlib.util.spec_from_file_location(
        "mlflow_tracker",
        pathlib.Path("scripts/common/11_mlflow_tracking.py")
    )
    mlflow_tracker = importlib.util.module_from_spec(spec)
    sys.modules["mlflow_tracker"] = mlflow_tracker
    spec.loader.exec_module(mlflow_tracker)
    CityMindTracker = mlflow_tracker.CityMindTracker
    tracker = CityMindTracker()
except Exception as e:
    tracker = None
    print(f"Advertencia: no se pudo importar MLflow Tracker ({e})")

# ======================================================
# 4️⃣ Entrenamiento
# ======================================================
results = []

for target, path in DATASETS.items():
    print(f"\n==============================")
    print(f"Entrenando modelos (No Social) para: {target}")
    print("==============================")

    if not path.exists():
        print(f"Dataset no encontrado: {path}")
        continue

    df = pd.read_csv(path)
    print("Dataset cargado:", df.shape)

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    pca = PCA(n_components=0.95, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    print(f"PCA → {pca.n_components_} componentes (95% varianza)")

    # ------------------ LassoCV ------------------
    lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
    lasso.fit(X_train_scaled, y_train)
    y_pred_lasso = lasso.predict(X_test_scaled)
    metrics_lasso = evaluate_model("LassoCV", y_test, y_pred_lasso)
    metrics_lasso["target"] = target
    metrics_lasso["pca_components"] = pca.n_components_
    results.append(metrics_lasso)
    print(f"LassoCV → R²={metrics_lasso['r2']:.3f} | RMSE={metrics_lasso['rmse']:.3f}")

    if tracker:
        tracker.log_metrics(
            model_name="LassoCV",
            scenario="no_social",
            metrics_dict=metrics_lasso,
            params={"target": target, "dataset_version": "2024"}
        )

    # ------------------ Random Forest ------------------
    rf = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    metrics_rf = evaluate_model("RandomForest", y_test, y_pred_rf)
    metrics_rf["target"] = target
    metrics_rf["pca_components"] = pca.n_components_
    results.append(metrics_rf)
    print(f"RandomForest → R²={metrics_rf['r2']:.3f} | RMSE={metrics_rf['rmse']:.3f}")

    if tracker:
        tracker.log_metrics(
            model_name="RandomForest",
            scenario="no_social",
            metrics_dict=metrics_rf,
            params={"target": target, "dataset_version": "2024"}
        )

    # ------------------ XGBoost ------------------
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
    print(f"XGBoost → R²={metrics_xgb['r2']:.3f} | RMSE={metrics_xgb['rmse']:.3f}")

    if tracker:
        tracker.log_metrics(
            model_name="XGBoost",
            scenario="no_social",
            metrics_dict=metrics_xgb,
            params={"target": target, "dataset_version": "2024"}
        )

# ======================================================
# 5️⃣ Guardar métricas
# ======================================================
df_results = pd.DataFrame(results)[["target", "model", "r2", "rmse", "mae", "pca_components"]]
out_path = OUT_DIR / "model_metrics.csv"
df_results.to_csv(out_path, index=False)

print("\nResultados guardados en:", out_path)
print(df_results)

print("\nEntrenamiento de modelos (No Social) completado con éxito.")
