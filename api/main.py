from fastapi import FastAPI

description = """
This API exposes a trained machine learning pipeline capable of predicting
anemia from patient hematological measurements.

The inference pipeline automatically performs feature engineering,
preprocessing, feature selection, and classification before returning
the prediction.
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
        }
)

@app.get("/")
async def root():
    return {"message": "Hello World"}