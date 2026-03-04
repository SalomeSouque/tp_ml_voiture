import time
from typing import Any

import joblib
import pandas as pd
from engine import get_db
from fastapi import APIRouter, Depends
from models.accident import Accident
from prometheus_client import Counter, Histogram
from services.prediction_service import save_prediction
from sqlmodel import Session

router = APIRouter(tags=["predict"])
# prefix="/predict",
MODEL_PATH = "model_prediction/model_accidents_.pkl"
model = joblib.load(MODEL_PATH)

# Déclaration des métriques :
#
# Counter = un compteur qui ne fait qu'augmenter
# (pour compter des événements : prédictions, erreurs)
#
# Histogram = enregistre des valeurs et les range dans des "buckets"
# (pour des durées ou des distributions)
# ─────────────────────────────────────────────────────────────

predictions_total = Counter(
    "predictions_total", "Nombre total de prédictions demandées"
)

predictions_success_total = Counter(
    "predictions_success_total", "Nombre de prédictions réussies"
)

predictions_error_total = Counter(
    "predictions_error_total", "Nombre de prédictions en échec"
)

# Les buckets = les "cases" de l'histogramme en secondes
prediction_duration_seconds = Histogram(
    "prediction_duration_seconds",
    "Durée des prédictions en secondes",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

# Distribution des probabilités de "blessure grave" prédites
prediction_proba_histogram = Histogram(
    "prediction_proba_histogram",
    "Distribution des probabilités de blessure grave",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)


@router.post(
    "/predict",
)
# Fonction qui va prédire :
def predict(
    accident: Accident,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    # Prend en paramètre les détail de l'accident ordonné grace à ma class Accident
    start = time.perf_counter()
    # Types explicites pour mypy
    result: dict[str, Any]
    result_dict: dict[str, float | int | None]
    success: bool | None
    error_message: str | bool | None

    # on compte chaque appel à /predict :
    predictions_total.inc()

    try:
        data = pd.DataFrame([accident.model_dump()])
        # Convertion en df

        categorical_cols = ["catr", "surf"]
        for col in categorical_cols:
            data[col] = data[col].astype(int)

        prediction = model.predict(data)[0]
        prediction_proba = model.predict_proba(data)[0]

        result = {
            "prediction": int(prediction),
            "probability": {
                "blessure_legere": float(prediction_proba[0]),
                "accident_grave": float(prediction_proba[1]),
            },
        }

        # result en format dict pr ma db
        result_dict = {
            "prediction": int(prediction),
            "proba_blessure_legere": float(prediction_proba[0]),
            "proba_blessure_grave": float(prediction_proba[1]),
        }

        # succès = incrémente + observe la proba
        predictions_success_total.inc()
        prediction_proba_histogram.observe(float(prediction_proba[1]))

        success = True
        error_message = False

    except Exception as e:
        result = {
            "prediction": None,
            "probability": None,
        }

        result_dict = {
            "prediction": None,
            "proba_blessure_legere": None,
            "proba_blessure_grave": None,
        }

        # erreur = incrémente le counter d'erreurs
        predictions_error_total.inc()

        success = False
        error_message = str(e)

    finally:
        end = time.perf_counter()
        execution_time = end - start
        # Durée de la fonction

        # Branche sur l'histograme
        prediction_duration_seconds.observe(execution_time)

        metadonnee_dict = {
            "success": success,
            "error_message": error_message,
            "execution_time": execution_time,
        }

        save_prediction(accident, result_dict, metadonnee_dict)

    return result
