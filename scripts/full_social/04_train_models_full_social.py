# ======================================================
# 🤖 CityMind - 04 Train Models (Full Social)
# Entrena modelos (PCA, LassoCV, RandomForest, XGBoost)
# para predecir depresión y distress con variables sociales
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
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# ======================================================
# 1️⃣ Configuración general
# ======================================================
DATA_DIR = Path("data/processed/full_social")
OUT_DIR = Path("data/interim/full_social")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = ["depression_crudeprev", "mhlth_crudeprev"]

print(f"📂 Buscando datasets de modelado en: {DATA_DIR.resolve()}")

# ======================================================
# 2️⃣ Función auxiliar: evaluación
# ======================================================
def evaluate_model(y_true, y_pred):
    """Calcula métricas de rendimiento."""
    return {
        "r2": round(r2_score(y_true, y_pred), 4),
        "rmse": round(mean_squared_error(y_true, y_pred, squared=False), 4),
        "mae": round(mean_absolute_error(y_true, y_pred), 4)
    }

# ======================================================
# 3️⃣ Entrenamiento por target
# ======================================================
results = []

for target in TARGETS:
    print(f"\n==============================")
    print(f" Entrenando modelos (Full Social) para: {target}")
    print("==============================")

    # Cargar dataset
    data_path = DATA_DIR / f"model_data_{target}.csv"
    if not data_path.exists():
        print(f"⚠️ No se encontró {data_path.name}, se omite.")
        continue

    df = pd.read_csv(data_path)
    df = df.dropna(subset=[target])
    X = df.drop(columns=[target])
    y = df[target]

    # --- Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Escalado
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # --- 1️ PCA (95% de varianza explicada)
    pca = PCA(n_components=0.95, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    print(f" PCA → {pca.n_components_} componentes (95% varianza)")

    # ==================================================
    # 🔹 Modelo 1: LassoCV
    # ==================================================
    lasso = LassoCV(cv=5, random_state=42, max_iter=10000)
    lasso.fit(X_train_scaled, y_train)
    preds_lasso = lasso.predict(X_test_scaled)
    metrics_lasso = evaluate_model(y_test, preds_lasso)
    metrics_lasso["pca_components"] = pca.n_components_
    results.append({
        "target": target,
        "model": "LassoCV",
        **metrics_lasso
    })
    print(f" LassoCV → R²={metrics_lasso['r2']:.3f} | RMSE={metrics_lasso['rmse']:.3f}")

    # ==================================================
    # 🔹 Modelo 2: Random Forest
    # ==================================================
    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    preds_rf = rf.predict(X_test)
    metrics_rf = evaluate_model(y_test, preds_rf)
    metrics_rf["pca_components"] = pca.n_components_
    results.append({
        "target": target,
        "model": "RandomForest",
        **metrics_rf
    })
    print(f" RandomForest → R²={metrics_rf['r2']:.3f} | RMSE={metrics_rf['rmse']:.3f}")

    # Guardar importancias
    importances = pd.DataFrame({
        "feature": X.columns,
        "importance": rf.feature_importances_
    }).sort_values(by="importance", ascending=False)
    imp_path = OUT_DIR / f"rf_importances_{target}.csv"
    importances.to_csv(imp_path, index=False)
    print(f" Importancias RF guardadas en: {imp_path.name}")

    # ==================================================
    # 🔹 Modelo 3: XGBoost
    # ==================================================
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
    preds_xgb = xgb.predict(X_test)
    metrics_xgb = evaluate_model(y_test, preds_xgb)
    metrics_xgb["pca_components"] = pca.n_components_
    results.append({
        "target": target,
        "model": "XGBoost",
        **metrics_xgb
    })
    print(f" XGBoost → R²={metrics_xgb['r2']:.3f} | RMSE={metrics_xgb['rmse']:.3f}")

    print(f" Modelos completados para {target}")

# ======================================================
# 4️⃣ Guardar métricas generales
# ======================================================
metrics_df = pd.DataFrame(results)
metrics_path = OUT_DIR / "model_metrics.csv"
metrics_df.to_csv(metrics_path, index=False)

print(f"\n Resultados guardados en: {metrics_path.name}")
print(metrics_df)

print("\n Entrenamiento de modelos (Full Social) completado con éxito.")
