from enum import Enum
from pydantic import BaseModel, Field

class GenderPatient(str, Enum):
    male = "Male" # se parseara a 0 para realizar la predicción
    female = "Female" # se parseara a 1 para realizar la predicción

class Patient(BaseModel):
    Gender: GenderPatient = Field(description='Gender of the patient.',
                                examples=['Male'])
    
    Hemoglobin:  float = Field(description='Hemoglobin concentration in grams per deciliter (g/dL).',
                            examples=[13.9],
                            gt=4,
                            lt=20)
    
    MCH: float = Field(description='Mean Corpuscular Hemoglobin (MCH) in picograms (pg).',
                            examples=[29.4],
                            gt=12,
                            lt=34)
    
    MCHC: float = Field(description='Mean Corpuscular Hemoglobin Concentration (MCHC) in grams per deciliter (g/dL).',
                            examples=[33.5],
                            gt=26,
                            lt=36)
    
    MCV: float = Field(description='Mean Corpuscular Volume (MCV) in femtoliters (fL).',
                            examples=[88.1],
                            gt=60,
                            lt=120)

class Diagnosis(str, Enum):
    anemic = "Anemic"
    not_anemic = "Not Anemic"

class PredictionResponse(BaseModel):
    prediction: int = Field(description='Predicted class returned by the model (0 = No Anemia, 1 = Anemia).',
                            examples=[1])
    diagnosis: Diagnosis = Field(description='Human-readable diagnosis corresponding to the predicted class.',
                            examples=['Anemic'])
    probability: float = Field(description='Estimated probability that the patient belongs to the positive class (Anemia).',
                            examples=[0.87])