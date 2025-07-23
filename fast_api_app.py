from fastapi import FastAPI, Form
from pydantic import BaseModel
import pandas as pd
import pickle

# Load model, encoders, and scaler
with open('best_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)
with open('encoder.pkl', 'rb') as encoders_file:
    encoders = pickle.load(encoders_file)
with open('scaler.pkl', 'rb') as scaler_file:
    scaler_data = pickle.load(scaler_file)

# Initialize FastAPI app
app = FastAPI()

def make_prediction(input_data):
    input_df = pd.DataFrame([input_data])

    for col, encoder in encoders.items():
        input_df[col] = encoder.transform(input_df[col])

    numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    input_df[numerical_cols] = scaler_data.transform(input_df[numerical_cols])

    prediction = loaded_model.predict(input_df)[0]
    probability = loaded_model.predict_proba(input_df)[0, 1]
    return "Churn" if prediction == 1 else "No Churn", probability

class PredictionRequest(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.post("/predict")
async def predict(data: PredictionRequest):
    input_data = data.dict()
    prediction, probability = make_prediction(input_data)
    return {"prediction": prediction, "probability": probability}