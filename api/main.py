from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager

from api.predict import predict_patient
from api.schemas import PredictionResponse, Patient, PredictionRecord
from api.loader import load_pipeline
from api.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_SUMMARY, API_CONTACT

from database.database import create_database
from database import tables
from database.crud import save_prediction, get_prediction, get_predictions

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database
    create_database()
    
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
    response = predict_patient(patient=patient, 
                        pipeline=request.app.state.pipeline)
    
    save_prediction(patient=patient, response=response)
    
    return response

@app.get('/predictions/{id}',
        tags=['Queries'],
        response_model=PredictionRecord,
        summary="Get prediction by ID",
        description="Retrieves a stored prediction by its unique identifier.",
        response_description="Prediction retrieved successfully."
        )
def read_prediction(id: int):
    """
    Retrieve a stored prediction by its unique identifier.
    """
    prediction = get_prediction(id)
    
    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found."
        )
    
    return PredictionRecord.model_validate(prediction)

@app.get('/predictions',
        tags=["Queries"],
        response_model=list[PredictionRecord],
        summary="Get all predictions.",
        description="Retrieves all predictions stored in the database.",
        response_description="List of stored predictions.")
def read_predictions() -> list[PredictionRecord]:
    """
    Retrieve all stored predictions from the database.
    """
    predictions = get_predictions()
    
    return [PredictionRecord.model_validate(prediction) 
            for prediction in predictions]

@app.get('/predictions/count')
def count_predictions():
    pass