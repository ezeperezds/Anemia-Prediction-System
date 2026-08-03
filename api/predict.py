import pandas as pd
from sklearn.pipeline import Pipeline
from api.schemas import Patient, PredictionResponse, Diagnosis, GenderPatient

def predict_patient(pipeline: Pipeline, patient: Patient) -> PredictionResponse:
    
    # el objeto patient pasa a ser un diccionario
    patient = patient.model_dump()
    
    # se parsea los valores de gender a 1 o 0 según sea el caso
    patient['Gender'] = 1 if patient['Gender'] == GenderPatient.female else 0
    
    # creamos un df a partir del dict del paciente
    patient_df = pd.DataFrame([patient])
    
    # obtenemos la prediccion y las probabilidades
    pred = pipeline.predict(patient_df)[0]
    pred_proba = pipeline.predict_proba(patient_df)
    
    # guardamos la probabilidad
    probability = pred_proba[0][1]
    
    # creamos el diagnostico
    diagnosis = (Diagnosis.anemic if pred[0] == 1 else Diagnosis.not_anemic)
    
    return PredictionResponse(
        prediction = pred,
        diagnosis = diagnosis,
        probability = round(probability, 4)
    )