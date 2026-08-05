from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from api.predict import predict_patient
from api.schemas import PredictionResponse, Patient
from api.loader import load_pipeline

from api.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_SUMMARY, API_CONTACT

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the trained pipeline once when the application starts.
    # The same instance will be reused for every prediction request.
    app.state.pipeline = load_pipeline()
    yield

app = FastAPI(
    title = API_TITLE,
    description = API_DESCRIPTION,
    summary = API_SUMMARY,
    version = API_VERSION,
    contact = API_CONTACT,
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