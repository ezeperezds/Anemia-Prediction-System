import pandas as pd
from sklearn.pipeline import Pipeline
from api.schemas import Patient, PredictionResponse, Diagnosis, GenderPatient

def predict_patient(pipeline: Pipeline, patient: Patient) -> PredictionResponse:
    
    # Convert the validated Pydantic model into a dictionary.
    patient = patient.model_dump()
    
    # Convert the categorical gender representation into the numerical encoding
    # expected by the trained model.
    patient['Gender'] = (1 if patient['Gender'] == GenderPatient.female else 0)
    
    # Create a single-row DataFrame matching the format expected by the pipeline.
    patient_df = pd.DataFrame([patient])
    
    # Run inference using the complete machine learning pipeline.
    pred = int(pipeline.predict(patient_df)[0])
    # Obtain the probability of the positive class (Anemic).
    pred_proba = float(pipeline.predict_proba(patient_df)[0][1])
    
    probability = round(pred_proba*100, 4)
    
    # Make the diagnosis.
    diagnosis = (Diagnosis.anemic if pred == 1 else Diagnosis.not_anemic)
    
    return PredictionResponse(
        prediction = pred,
        diagnosis = diagnosis,
        probability = probability
    )