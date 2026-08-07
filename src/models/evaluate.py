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
            f'{round(model_scores["test_accuracy"].mean(), 4)} ± {round(model_scores['test_accuracy'].std(), 4)}',

        "precision":
            f'{round(model_scores["test_precision"].mean(), 4)} ± {round(model_scores['test_precision'].std(), 4)}',

        "recall":
            f'{round(model_scores["test_recall"].mean(), 4)} ± {round(model_scores['test_recall'].std(), 4)}',

        "f1":
            f'{round(model_scores["test_f1"].mean(), 4)} ± {round(model_scores['test_f1'].std(), 4)}'
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
            'f1-score': f1_score(y_true, y_pred),
            'predicted positives': y_pred.sum()
        })
    df_thresholds = pd.DataFrame(rows)
    return df_thresholds