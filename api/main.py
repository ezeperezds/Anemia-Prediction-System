from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from api.predict import predict_patient
from api.schemas import PredictionResponse, Patient
from api.loader import load_pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the trained pipeline once when the application starts.
    # The same instance will be reused for every prediction request.
    app.state.pipeline = load_pipeline()
    yield


description = """
This API exposes a trained machine learning pipeline capable of predicting
anemia from patient hematological measurements.

The inference pipeline automatically performs feature engineering,
preprocessing, feature selection, and classification before returning
the prediction.

The API accepts patient hematological measurements as input and returns
the predicted class, a human-readable diagnosis, and the probability of
the positive class.
"""

app = FastAPI(
    title = 'Anemia Prediction API',
    description = description,
    summary = 'Machine Learning API for anemia prediction.',
    version = '1.0',
    contact = {
        'name': 'Ezequiel Alejandro Pérez',
        'email': 'ezep5993@gmail.com',
        'url': 'https://github.com/ezeperezds'
        },
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Anemia Prediction API is running."}

@app.post("/predict", 
        tags=["Prediction"],
        response_model=PredictionResponse, 
        summary="Predict anemia",
        description="Predicts whether a patient has anemia from hematological measurements.",
        response_description="Prediction result including the predicted class, diagnosis, and probability."
        )
def predict_endpoint(patient: Patient, request: Request):
    """
    Predict whether a patient has anemia using the trained pipeline.
    """
    return predict_patient(patient=patient, 
                        pipeline=request.app.state.pipeline)