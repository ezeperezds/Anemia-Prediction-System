from enum import Enum
from pydantic import BaseModel, Field

class Gender(str, Enum):
    male = "Male" # se parseara a 0 para realizar la predicción
    female = "Female" # se parseara a 1 para realizar la predicción

class Patient(BaseModel):
    Gender: Gender
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