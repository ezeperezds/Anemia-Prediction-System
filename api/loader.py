from joblib import load
from sklearn.pipeline import Pipeline
from src.preprocessing.features import FeatureEngineering, FeatureSelector

from api.config import MODEL_PATH

import logging

logger = logging.getLogger(__name__)

def load_pipeline() -> Pipeline:
    """
    Load the serialized machine learning pipeline from disk.
    """
    
    # Verify that the serialized pipeline exists before loading it.
    if not MODEL_PATH.exists():
        logger.critical(
            "Model file not found: %s", MODEL_PATH
            )
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )
    
    logger.info("Loading prediction pipeline...")
    
    try:
        pipeline = load(MODEL_PATH)
        logger.info("Prediction pipeline loaded successfully")
    except Exception:
        logger.critical("Failed to load the prediction pipeline.", exc_info=True)
        raise
    
    return pipeline