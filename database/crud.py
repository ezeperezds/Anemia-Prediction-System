from database.tables import Prediction
from database.database import SessionLocal
from api.schemas import Patient, PredictionResponse, GenderPatient, PredictionRecord
from sqlalchemy import select

import logging

logger = logging.getLogger(__name__)


# Store a prediction and its associated patient data in the database.

def save_prediction(patient: Patient, response: PredictionResponse):
    
    session = SessionLocal()
    
    prediction = Prediction(
        gender = 1 if patient.Gender == GenderPatient.female else 0,
        hemoglobin = patient.Hemoglobin,
        mch = patient.MCH,
        mchc = patient.MCHC,
        mcv = patient.MCV,
        prediction = response.prediction,
        diagnosis = response.diagnosis,
        probability = response.probability
    )
    
    try:
        session.add(prediction)
        session.commit()
        session.refresh(prediction)
        
        logger.info("Prediction saved successfully.")
        
        return prediction
    except Exception:
        logger.exception("Unexpected error while saving the prediction.")
        session.rollback()
        raise
    finally:
        session.close()

# Retrieve a stored prediction by its unique identifier.
def get_prediction(id: int) -> PredictionRecord | None:
    
    session = SessionLocal()
    
    try:
        prediction = session.get(Prediction, id)
        
        if prediction is None:
            return None
        
        return prediction
    finally:
        session.close()

# Retrieve all stored predictions from the database.
def get_predictions() -> list[Prediction]:
    
    session = SessionLocal()
    
    try:
        stmt = (select(Prediction).order_by(Prediction.id))
        
        predictions = (session.execute(stmt).scalars().all())
        return predictions
        
    finally:
        session.close()