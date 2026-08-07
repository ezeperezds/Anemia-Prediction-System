from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class GenderPatient(str, Enum):
    """Supported patient genders."""
    male = "Male"
    female = "Female"

class Patient(BaseModel):
    Gender: GenderPatient = Field(description='Gender of the patient.',
                                examples=['Male'])
    
    Hemoglobin:  float = Field(description='Hemoglobin concentration in grams per deciliter (g/dL).',
                            examples=[13.9],
                            ge=4,
                            le=20)
    
    MCH: float = Field(description='Mean Corpuscular Hemoglobin (MCH) in picograms (pg).',
                            examples=[29.4],
                            ge=12,
                            le=34)
    
    MCHC: float = Field(description='Mean Corpuscular Hemoglobin Concentration (MCHC) in grams per deciliter (g/dL).',
                            examples=[33.5],
                            ge=26,
                            le=36)
    
    MCV: float = Field(description='Mean Corpuscular Volume (MCV) in femtoliters (fL).',
                            examples=[88.1],
                            ge=60,
                            le=120)

class Diagnosis(str, Enum):
    anemic = "Anemic"
    not_anemic = "Not Anemic"

class PredictionResponse(BaseModel):
    prediction: int = Field(description='Predicted class returned by the model (0 = No Anemia, 1 = Anemia).',
                            examples=[1])
    diagnosis: Diagnosis = Field(description='Human-readable diagnosis corresponding to the predicted class.',
                            examples=['Anemic'])
    probability: float = Field(description='Estimated probability (percentage) that the patient belongs to the positive class (Anemia).',
                            examples=[87.69])

class PredictionRecord(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="Unique identifier of the stored prediction.",
                    examples=[15]
                    )
    
    gender: int = Field(description="Encoded gender used by the model (0 = Male, 1 = Female).",
                        examples=[1]
                        )
    
    hemoglobin: float = Field(description="Hemoglobin concentration in grams per deciliter (g/dL).",
                            examples=[13.8]
                            )
    
    mch: float = Field(description="Mean Corpuscular Hemoglobin (MCH) in picograms (pg).",
                    examples=[29.4]
                    )
    
    mchc: float = Field(description="Mean Corpuscular Hemoglobin Concentration (MCHC) in grams per deciliter (g/dL).",
                        examples=[33.5]
                        )
    
    mcv: float = Field(description="Mean Corpuscular Volume (MCV) in femtoliters (fL).",
                    examples=[88.1]
                    )
    prediction: int = Field(description="Predicted class returned by the model (0 = No Anemia, 1 = Anemia).",
                            examples=[1]
                            )
    
    diagnosis: Diagnosis = Field(description="Human-readable diagnosis corresponding to the predicted class.",
                                examples=["Anemic"]
                                )
    probability: float = Field(description="Estimated probability of the positive class expressed as a percentage.",
                            examples=[97.84]
                            )
    
    created_at: datetime = Field(description="UTC date and time when the prediction was stored.",
                                examples=["2026-08-07T14:35:22Z"]
                                )