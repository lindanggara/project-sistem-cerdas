import joblib
import numpy as np


class Predictor:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, text: str):
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba([text])[0]
            idx = int(np.argmax(proba))
            label = self.model.classes_[idx]
            confidence = float(proba[idx])
        else:
            label = self.model.predict([text])[0]
            confidence = 1.0
        return str(label), confidence

    def predict_batch(self, texts):
        labels = self.model.predict(texts)
        if hasattr(self.model, "predict_proba"):
            probas = self.model.predict_proba(texts)
            confidences = probas.max(axis=1).tolist()
        else:
            confidences = [1.0] * len(texts)
        return [
            {"label": str(l), "confidence": float(c)}
            for l, c in zip(labels, confidences)
        ]
