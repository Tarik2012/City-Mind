"""
CityMind - Feature Expansion (versión final, ajustada a XGBoost)
-----------------------------------------------------------------
Genera vectores con las columnas exactas para cada tipo de modelo:
- Depression / MHLTH
- Full Social / No Social
"""

import pandas as pd
import numpy as np


# ============================================================
# 🔹 Columnas del modelo Full Social (41 columnas)
# ============================================================
FEATURE_NAMES_FULL = [
    'totalpopulation', 'totalpop18plus', 'access2_crudeprev', 'arthritis_crudeprev',
    'binge_crudeprev', 'bphigh_crudeprev', 'bpmed_crudeprev', 'cancer_crudeprev',
    'casthma_crudeprev', 'chd_crudeprev', 'checkup_crudeprev', 'cholscreen_crudeprev',
    'colon_screen_crudeprev', 'copd_crudeprev', 'csmoking_crudeprev', 'dental_crudeprev',
    'depression_crudeprev',  # 👈 añadido (necesario para MHLTH full social)
    'diabetes_crudeprev', 'ghlth_crudeprev', 'highchol_crudeprev', 'lpa_crudeprev',
    'mammouse_crudeprev', 'mhlth_crudeprev', 'obesity_crudeprev', 'phlth_crudeprev',
    'sleep_crudeprev', 'stroke_crudeprev', 'teethlost_crudeprev', 'hearing_crudeprev',
    'vision_crudeprev', 'cognition_crudeprev', 'mobility_crudeprev', 'selfcare_crudeprev',
    'indeplive_crudeprev', 'disability_crudeprev', 'isolation_crudeprev',
    'foodstamp_crudeprev', 'foodinsecu_crudeprev', 'housinsecu_crudeprev',
    'shututility_crudeprev', 'lacktrpt_crudeprev', 'emotionspt_crudeprev'
]


# ============================================================
# 🔹 Columnas de modelos No Social
# ============================================================
FEATURE_NAMES_NO_SOCIAL_DEPRESSION = [
    'totalpopulation', 'totalpop18plus', 'access2_crudeprev', 'arthritis_crudeprev',
    'binge_crudeprev', 'bphigh_crudeprev', 'bpmed_crudeprev', 'cancer_crudeprev',
    'casthma_crudeprev', 'chd_crudeprev', 'checkup_crudeprev', 'cholscreen_crudeprev',
    'colon_screen_crudeprev', 'copd_crudeprev', 'csmoking_crudeprev', 'dental_crudeprev',
    'diabetes_crudeprev', 'ghlth_crudeprev', 'highchol_crudeprev', 'lpa_crudeprev',
    'mammouse_crudeprev', 'mhlth_crudeprev', 'obesity_crudeprev', 'phlth_crudeprev',
    'sleep_crudeprev', 'stroke_crudeprev', 'teethlost_crudeprev', 'hearing_crudeprev',
    'vision_crudeprev', 'cognition_crudeprev', 'mobility_crudeprev', 'selfcare_crudeprev',
    'indeplive_crudeprev', 'disability_crudeprev'
]

FEATURE_NAMES_NO_SOCIAL_MHLTH = [
    'totalpopulation', 'totalpop18plus', 'access2_crudeprev', 'arthritis_crudeprev',
    'binge_crudeprev', 'bphigh_crudeprev', 'bpmed_crudeprev', 'cancer_crudeprev',
    'casthma_crudeprev', 'chd_crudeprev', 'checkup_crudeprev', 'cholscreen_crudeprev',
    'colon_screen_crudeprev', 'copd_crudeprev', 'csmoking_crudeprev', 'dental_crudeprev',
    'depression_crudeprev', 'diabetes_crudeprev', 'ghlth_crudeprev', 'highchol_crudeprev',
    'lpa_crudeprev', 'mammouse_crudeprev', 'obesity_crudeprev', 'phlth_crudeprev',
    'sleep_crudeprev', 'stroke_crudeprev', 'teethlost_crudeprev', 'hearing_crudeprev',
    'vision_crudeprev', 'cognition_crudeprev', 'mobility_crudeprev', 'selfcare_crudeprev',
    'indeplive_crudeprev', 'disability_crudeprev'
]


# ============================================================
# 🔹 Expansor principal
# ============================================================
def expand_features(proxy_vector):
    """
    Expande un vector resumido (8–9 índices) en las features esperadas
    por el modelo correspondiente (según target y tipo).
    """

    # 1️⃣ Detectar tipo de modelo y target
    use_social = proxy_vector.get("use_social", True)
    target = proxy_vector.get("target", "mhlth_crudeprev")

    # Seleccionar lista base de columnas según tipo
    if use_social:
        feature_names = FEATURE_NAMES_FULL.copy()
    else:
        if target == "depression_crudeprev":
            feature_names = FEATURE_NAMES_NO_SOCIAL_DEPRESSION.copy()
        else:
            feature_names = FEATURE_NAMES_NO_SOCIAL_MHLTH.copy()

    # 🔹 Quitar el target de las features si aparece (para evitar el error)
    if target in feature_names:
        feature_names.remove(target)

    # 2️⃣ Crear base inicial vacía
    base = {col: 0.0 for col in feature_names}

    # 3️⃣ Extraer índices de entrada
    health = proxy_vector.get("health_index", 0.3)
    economy = proxy_vector.get("economy_index", 0.5)
    environment = proxy_vector.get("environment_index", 0.4)
    education = proxy_vector.get("education_index", 0.4)
    social = proxy_vector.get("social_index", 0.2)
    population = proxy_vector.get("population", 100000)
    urbanization = proxy_vector.get("urbanization", 0.7)

    # 4️⃣ Asignaciones proporcionales
    base["totalpopulation"] = population
    if "totalpop18plus" in base:
        base["totalpop18plus"] = population * 0.8

    for col in ["mhlth_crudeprev", "phlth_crudeprev", "ghlth_crudeprev",
                "sleep_crudeprev", "obesity_crudeprev", "diabetes_crudeprev"]:
        if col in base:
            base[col] = 10 + 10 * health

    for col in ["checkup_crudeprev", "cholscreen_crudeprev", "colon_screen_crudeprev"]:
        if col in base:
            base[col] = 50 + education * 30

    for col in ["csmoking_crudeprev", "binge_crudeprev", "copd_crudeprev"]:
        if col in base:
            base[col] = (1 - environment) * 20

    for col in ["isolation_crudeprev", "disability_crudeprev", "emotionspt_crudeprev"]:
        if col in base:
            base[col] = (1 - social) * 30

    for col in ["foodinsecu_crudeprev", "housinsecu_crudeprev",
                "lacktrpt_crudeprev", "shututility_crudeprev"]:
        if col in base:
            base[col] = (1 - economy) * 20

    # 5️⃣ Devolver Serie ordenada según las features reales del modelo
    return pd.Series(base)[feature_names]
