"""Baseline model klasik: TF-IDF + LogReg / SVM / Naive Bayes.

Jalankan: python src/baseline.py
Input : data/processed/train.csv, valid.csv, test.csv
"""
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from evaluate import evaluate_macro_f1, print_evaluation

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
LABELS = ["anger", "fear", "joy", "love", "sad", "neutral"]


def load_split(nama):
    return pd.read_csv(PROCESSED / f"{nama}.csv")


def buat_model(nama):
    if nama == "logreg":
        clf = LogisticRegression(max_iter=1000, random_state=42)
    elif nama == "svm":
        clf = LinearSVC(random_state=42)
    elif nama == "nb":
        clf = MultinomialNB()
    else:
        raise ValueError(nama)
    return Pipeline([
        ("tfidf", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
        ("clf", clf),
    ])


def main():
    train = load_split("train")
    valid = load_split("valid")
    test = load_split("test")

    hasil_semua = {}
    for nama in ["logreg", "svm", "nb"]:
        print(f"\n>>> Training {nama} ...")
        model = buat_model(nama)
        model.fit(train["text"], train["label"])

        # Validasi
        pred_valid = model.predict(valid["text"])
        res_valid = evaluate_macro_f1(valid["label"], pred_valid, LABELS)
        print(f"[{nama}] Macro F1 valid: {res_valid['macro_f1']:.4f}")

        # Test
        pred_test = model.predict(test["text"])
        res_test = evaluate_macro_f1(test["label"], pred_test, LABELS)
        print_evaluation(res_test, title=f"{nama} — TEST")

        hasil_semua[nama] = {
            "valid": res_valid["macro_f1"],
            "test": res_test["macro_f1"],
        }

    print("\n===== RINGKASAN =====")
    print(f"{'Model':<10} {'Valid':>8} {'Test':>8}")
    for nama, skor in hasil_semua.items():
        print(f"{nama:<10} {skor['valid']:>8.4f} {skor['test']:>8.4f}")


if __name__ == "__main__":
    main()