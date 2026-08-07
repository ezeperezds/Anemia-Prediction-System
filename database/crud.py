from database.tables import Prediction
from database.database import SessionLocal
from api.schemas import Patient, PredictionResponse, GenderPatient

import logging

logger = logging.getLogger(__name__)

# 
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

def get_prediction():
        pass

def get_predictions():
    pass

def delete_prediction():
    pass

def update_prediction():
    pass