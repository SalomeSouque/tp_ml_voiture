#from backend.models.model_db import AccidentPrediction
from sqlmodel import Session
from fastapi import APIRouter, Depends

from engine import get_db
from services.prediction_service import save_prediction
from models.accident import Accident



import pandas as pd
import time
import os
import joblib



router = APIRouter(tags=["predict"])
#prefix="/predict", 
MODEL_PATH = "model_prediction/model_accidents_.pkl"
model = joblib.load(MODEL_PATH)


@router.post("/predict",)
# Fonction qui va prédire : 
def predict(accident: Accident, db: Session = Depends(get_db)):  # Prend en paramètre les détail de l'accident ordonné grace à ma class Accident 
    start = time.perf_counter()
    try :
        data = pd.DataFrame([accident.dict()])   # Convertion en df
        
        categorical_cols = ['catr', 'surf'] 
        for col in categorical_cols:
            data[col] = data[col].astype(int)


        prediction = model.predict(data)[0]      
        prediction_proba = model.predict_proba(data)[0]
        
        
        result = {
            "prediction": int(prediction),
            "probability": {
                "blessure_legere": float(prediction_proba[0]),
                "accident_grave": float(prediction_proba[1])
            }
        }

        # result en format dict pr ma db
        result_dict = {
            "prediction": int(prediction),
            "proba_blessure_legere": float(prediction_proba[0]),
            "proba_blessure_grave": float(prediction_proba[1])
        }

        success = True
        error_message = False

    except Exception as e :
        result = {
            "prediction": None,
            "probability": None,
        }

        result_dict = {
                "prediction": None,
                "proba_blessure_legere": None,
                "proba_blessure_grave": None,
            }
        
        success = False
        error_message = str(e)


    
    finally :
        end = time.perf_counter()
        execution_time = end - start # Durée de la fonction 


        metadonnee_dict = {
            "success" : success,
            "error_message" : error_message,
            "execution_time" : execution_time

        }

        
        save_prediction(accident, result_dict, metadonnee_dict)

    return result
