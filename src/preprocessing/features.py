import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureSelector(BaseEstimator, TransformerMixin):

    def __init__(self, features_to_drop, column_names):
        self.features_to_drop = features_to_drop
        self.column_names = column_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # X will be a numpy array from the preprocessor
        X_df = pd.DataFrame(X, columns=self.column_names)
        return X_df.drop(columns=self.features_to_drop, errors="ignore").values