import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def show_metrics(model_name, y_true, y_pred):
    metrics = {
        'accuracy': round(accuracy_score(y_true, y_pred), 2),
        'precision': round(precision_score(y_true, y_pred), 2),
        'recall': round(recall_score(y_true, y_pred), 2),
        'f1-score': round(f1_score(y_true, y_pred), 2)
    }
    return f'{model_name} metrics: {metrics}'

def show_confusion_matrix(y_true, y_pred):
    matrix = confusion_matrix(y_true, y_pred)
    visualizer = ConfusionMatrixDisplay(matrix, display_labels=['Sin anemia', 'Con anemia'])
    return visualizer.plot()

def show_cv_metrics(model_scores):
    metrics = {
        "accuracy":
            model_scores["test_accuracy"].mean().round(4),

        "precision":
            model_scores["test_precision"].mean().round(4),

        "recall":
            model_scores["test_recall"].mean().round(4),

        "f1":
            model_scores["test_f1"].mean().round(4)
            }
    return metrics


def show_thresholds(y_proba_min, y_proba_max, y_proba, y_true):
    thresholds = np.arange(y_proba_min, y_proba_max, 0.01)
    rows = []
    for t in thresholds:
        y_pred = (y_proba >= t).astype(int)
        rows.append({
            'thresholds': t,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'predicted positives': y_pred.sum()
        })
    df_thresholds = pd.DataFrame(rows)
    return df_thresholds