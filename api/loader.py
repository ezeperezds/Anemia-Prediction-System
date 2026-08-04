from joblib import load
from pathlib import Path
from sklearn.pipeline import Pipeline
from src.preprocessing.features import FeatureEngineering, FeatureSelector

def load_pipeline() -> Pipeline:
    """
    Load the serialized machine learning pipeline from disk.
    """
    # Resolve the project root directory regardless of where the application is executed.
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    MODEL_PATH = BASE_DIR / "models" / "catboost_pipeline.pkl"
    
    # Verify that the serialized pipeline exists before loading it.
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )
    pipeline = load(MODEL_PATH)
    
    return pipeline