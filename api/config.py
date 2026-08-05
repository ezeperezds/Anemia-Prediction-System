from pathlib import Path

# Resolve the project root directory regardless of where the application is executed.
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "catboost_pipeline.pkl"

# API Configuration

API_TITLE = "Anemia Prediction API"

API_DESCRIPTION = """
This API exposes a trained machine learning pipeline capable of predicting
anemia from patient hematological measurements.

The inference pipeline automatically performs feature engineering,
preprocessing, feature selection, and classification before returning
the prediction.

The API accepts patient hematological measurements as input and returns
the predicted class, a human-readable diagnosis, and the probability of
the positive class.
"""

API_VERSION = "1.0"

API_SUMMARY = "Machine Learning API for anemia prediction."

API_CONTACT = {
    "name" : "Ezequiel Alejandro Pérez",
    "email": "ezep5993@gmail.com",
    "url": "https://github.com/ezeperezds"
}