# app/main.py

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path

# --- Setup ---
app = FastAPI(
    title="Diabetes Prediction API",
    description="An API to predict diabetes using an XGBoost model."
)

# Define paths
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Load artifacts
try:
    model = joblib.load(ARTIFACTS_DIR / "diabetes_model.joblib")
    scaler = joblib.load(ARTIFACTS_DIR / "scaler.joblib")
    print("--- Model and scaler loaded successfully ---")
except FileNotFoundError:
    print("--- Error: Model or scaler not found. Run train.py first. ---")
    model = None
    scaler = None

# --- API Models ---

# This model defines the structure of the *input* data for the API
class PatientData(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int
    
    # Example data for the API documentation
    class Config:
        schema_extra = {
            "example": {
                "Pregnancies": 6,
                "Glucose": 148,
                "BloodPressure": 72,
                "SkinThickness": 35,
                "Insulin": 0,
                "BMI": 33.6,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 50
            }
        }

# This model defines the structure of the *output* data
class PredictionOut(BaseModel):
    prediction: int  # 0 for No Diabetes, 1 for Diabetes
    probability: float # The confidence score

# --- API Endpoints ---

@app.get("/", tags=["General"])
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the Diabetes Prediction API!"}

@app.post("/predict", tags=["Prediction"], response_model=PredictionOut)
def predict_diabetes(data: PatientData):
    """
    Make a diabetes prediction based on patient data.
    
    - **Pregnancies**: Number of times pregnant
    - **Glucose**: Plasma glucose concentration
    - **BloodPressure**: Diastolic blood pressure (mm Hg)
    - **SkinThickness**: Triceps skin fold thickness (mm)
    - **Insulin**: 2-Hour serum insulin (mu U/ml)
    - **BMI**: Body mass index
    - **DiabetesPedigreeFunction**: Diabetes pedigree function
    - **Age**: Age (years)
    """
    if model is None or scaler is None:
        return {"error": "Model not loaded. Please train the model first."}
        
    # 1. Convert input data to a numpy array in the correct order
    # This order MUST match the 'features' list in train.py
    input_data = np.array([[
        data.Pregnancies, data.Glucose, data.BloodPressure,
        data.SkinThickness, data.Insulin, data.BMI,
        data.DiabetesPedigreeFunction, data.Age
    ]])
    
    # 2. Scale the data
    scaled_data = scaler.transform(input_data)
    
    # 3. Make prediction
    pred = model.predict(scaled_data)
    proba = model.predict_proba(scaled_data)
    
    # Get the probability of the *predicted* class
    prediction_result = int(pred[0])
    probability_score = float(proba[0][prediction_result])
    
    return {
        "prediction": prediction_result,
        "probability": probability_score
    }