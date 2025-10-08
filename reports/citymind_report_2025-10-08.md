# 🧠 CityMind – Informe de Modelos (2025-10-08)

**Proyecto:** CityMind  
**Autor:** Erik  
**Fecha:** 2025-10-08

---

## 📘 Resumen General

Este informe resume los resultados del análisis comparativo entre los modelos de predicción **con y sin variables sociales**.

El objetivo fue evaluar el impacto de las dimensiones sociales en la predicción de indicadores de salud mental (depresión y distress) a nivel de condado.

---

## 📊 Resumen Numérico

| Target | Modelo | R² (No Social) | R² (Full Social) | ΔR² | ΔR² (%) |
|---------|---------|----------------|------------------|------|--------|
| depression_crudeprev | LassoCV | 0.819 | 0.819 | +0.0000 | +0.00% |
| depression_crudeprev | RandomForest | 0.815 | 0.815 | +0.0000 | +0.00% |
| depression_crudeprev | XGBoost | 0.849 | 0.849 | +0.0000 | +0.00% |
| mhlth_crudeprev | LassoCV | 0.949 | 0.955 | +0.0065 | +0.69% |
| mhlth_crudeprev | RandomForest | 0.952 | 0.952 | +0.0004 | +0.04% |
| mhlth_crudeprev | XGBoost | 0.964 | 0.967 | +0.0035 | +0.36% |

**Promedio ΔR²:** 0.0017  
**Promedio ΔR² (%):** 0.18%  

---

## 🔍 Principales Conclusiones

- Las variables sociales **no aportan mejoras significativas** en la predicción de **depresión**.
- Sin embargo, muestran una **ligera mejora en la predicción de distress (mhlth_crudeprev)**,  
  con un incremento medio de R² del **0.18%**.
- El mejor modelo general fue **XGBoost** para el target **mhlth_crudeprev**,  
  con un R² de **0.967** bajo el escenario *Full Social*.
- Estos resultados indican que los factores sociales podrían tener un **efecto marginal**,  
  pero consistentemente positivo sobre el bienestar mental general.

---

## 📈 Comparación Visual de R²

![Comparación de R²](../data/interim/comparison/r2_comparison.png)

---

## 🧩 Próximos pasos

- Incluir más variables contextuales (educación, crimen, empleo) en los modelos.
- Probar técnicas de selección no lineal (SHAP, Boruta, Permutation Importance).
- Evaluar interacciones entre factores sociales y médicos.
- Integrar seguimiento temporal para evaluar evolución de la salud mental.

---

**CityMind** © 2025 – Proyecto Data Science  
*Generado automáticamente mediante pipeline reproducible.*
