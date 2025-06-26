from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# load model
model = joblib.load("best_model.pkl")

# mapping back the prediction to original label
target_order = [
    'Insufficient_Weight',
    'Normal_Weight',
    'Overweight_Level_I',
    'Overweight_Level_II',
    'Obesity_Type_I',
    'Obesity_Type_II',
    'Obesity_Type_III'
]

app = FastAPI()


class InputData(BaseModel):
    Gender: str
    Age: float
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: str   # Ordinal: "Jarang", "Sedang", "Sering"
    NCP: str    # Ordinal: "Kurang", "Cukup", "Berlebih"
    CAEC: str
    SMOKE: str
    CH2O: str   # Ordinal: "Kurang", "Cukup", "Banyak"
    SCC: str
    FAF: str    # Ordinal: "Tidak Aktif", "Kurang Aktif", "Cukup Aktif", "Sangat Aktif"
    TUE: str    # Ordinal: "Tidak Pernah", "Jarang", "Sering"
    CALC: str
    MTRANS: str

@app.get("/")
def home():
    return {"message": "Obesity prediction API is running."}

@app.post("/predict")
def predict(input_data: InputData):
    try:
        # convert input to DataFrame
        input_df = pd.DataFrame([input_data.dict()])

        # predict
        pred = model.predict(input_df)[0]  # returns int (0–6)
        pred_label = target_order[int(pred)]

        return {"prediction": pred_label}

    except Exception as e:
        return {"error": str(e)}