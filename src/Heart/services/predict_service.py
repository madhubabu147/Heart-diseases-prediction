import os
import sys
import pandas as pd
import numpy as np
from src.Heart.logger import logging
from src.Heart.exception import customexception
from src.Heart.utils.utils import load_object
from src.Heart.pipeline.Prediction_pipeline import CustomData

class PredictService:
    def __init__(self):
        self.preprocessor_path = os.path.join("Artifacts", "Preprocessor.pkl")
        self.model_path = os.path.join("Artifacts", "Model.pkl")
        self.preprocessor = None
        self.model = None
        self._load_artifacts()

    def _load_artifacts(self):
        try:
            if not os.path.exists(self.preprocessor_path) or not os.path.exists(self.model_path):
                raise FileNotFoundError("Model artifacts not found. Please train the model first.")
            
            self.preprocessor = load_object(self.preprocessor_path)
            self.model = load_object(self.model_path)
        except Exception as e:
            raise customexception(e, sys)

    def predict(self, data: CustomData):
        try:
            df = data.get_data_as_dataframe()
            scaled_data = self.preprocessor.transform(df)
            pred = self.model.predict(scaled_data)
            
            # Get probability if supported
            probability = 0.0
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(scaled_data)
                probability = probs[0][1] * 100 # Probability of class 1 (Heart Disease)
            else:
                # Fallback for models without probability
                probability = 100.0 if pred[0] == 1 else 0.0

            return {
                "prediction": int(pred[0]),
                "probability": round(probability, 2),
                "label": "Heart Disease Detected" if pred[0] == 1 else "Normal"
            }
        except Exception as e:
            raise customexception(e, sys)

    def predict_batch(self, df: pd.DataFrame):
        try:
            # Ensure columns match expected input
            # This relies on the preprocessor handling the columns correctly
            # We assume the input DF has the correct column names as per CustomData
            
            scaled_data = self.preprocessor.transform(df)
            preds = self.model.predict(scaled_data)
            
            results = []
            probs = []
            
            if hasattr(self.model, "predict_proba"):
                proba_arr = self.model.predict_proba(scaled_data)
                probs = [round(p[1] * 100, 2) for p in proba_arr]
            else:
                probs = [100.0 if p == 1 else 0.0 for p in preds]

            df['Prediction'] = preds
            df['Probability_percent'] = probs
            df['Label'] = df['Prediction'].apply(lambda x: "Heart Disease" if x == 1 else "Normal")
            
            return df
        except Exception as e:
            raise customexception(e, sys)
