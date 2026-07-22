import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureSelector(BaseEstimator, TransformerMixin):

    def __init__(self, features_to_drop, column_names):
        self.features_to_drop = features_to_drop
        self.column_names = column_names

    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):
        # X will be a numpy array from the preprocessor
        X_df = pd.DataFrame(X, columns=self.column_names)
        return X_df.drop(columns=self.features_to_drop, errors="ignore").values

class FeatureEngineering(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X):

        X = X.copy()
            
        # Hemoglobina baja según genero
    
        anemia_hb = []
        for index, row in X.iterrows():
            if row['Hemoglobin'] < 13 and row['Gender'] == 0:
                anemia_hb.append(1)
            elif row['Hemoglobin'] < 12 and row['Gender'] == 1:
                anemia_hb.append(1)
            else:
                anemia_hb.append(0)
    
        X['Low_Hb'] = anemia_hb
    
        # Clasificación del MCV
    
        mcv_categoria = []
    
        for index, row in X.iterrows():
            if (row['MCV'] < 80):
                mcv_categoria.append('Micro')
        
            elif ((row['MCV'] >= 80) & (row['MCV']<=100)):
                mcv_categoria.append('Normal')
            else:
                mcv_categoria.append('Macro')
        
    
        X['MCV_Cat'] = mcv_categoria
    
        # Relación entre Hemoglobina y MCV
    
        X['HB_MCV_ratio'] = (X['Hemoglobin'] / X['MCV']).round(2)
    
        # Clasificación del MCHC
    
        mchc_cat = []
    
        for index, row in X.iterrows():
            if (row['MCHC']) < 32:
                mchc_cat.append('Bajo')
            elif ((row['MCHC'] >= 32) & (row['MCHC'] <= 36)):
                mchc_cat.append('Normal')
            else:
                mchc_cat.append('Alto')
    
        X['MCHC_Cat'] = mchc_cat
    
        # Clasificación del MCH
    
        mch_cat = []

        for index, row in X.iterrows():
            if (row['MCH']) < 27:
                mch_cat.append('Bajo')
            elif ((row['MCH'] >= 27) & (row['MCH'] <= 33)):
                mch_cat.append('Normal')
            else:
                mch_cat.append('Alto')
    
        X['MCH_Cat'] = mch_cat
    
        # Indicador de microcitosis
    
        X['Microcitosis'] = np.where(X['MCV'] < 80, 1, 0)
    
        # Indicador de hipocromía
    
        X['Hipocromía'] = np.where(X['MCHC'] < 32, 1, 0)
    
        # Score hematológico simple
    
        X['Score'] = X['Low_Hb'] + (
        (X['MCHC_Cat'] == 'Bajo').astype(int) +
        (X['MCH_Cat'] == 'Bajo').astype(int) +
        (X['MCV_Cat'] == 'Micro').astype(int)
        )
        return X