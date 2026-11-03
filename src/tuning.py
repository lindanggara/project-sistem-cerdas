"""Tuning model klasik: TF-IDF (Word + Char) + GridSearchCV.

Jalankan: python src/tuning.py
Input : data/processed/train.csv, valid.csv, test.csv
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV

# Tambahkan path ke src agar bisa import evaluate
sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate import evaluate_macro_f1, print_evaluation, LABEL_UTAMA

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

# --- 1. KAMUS NORMALISASI KATA GAUL (Sama seperti baseline) ---
KAMUS_GAUL = {
    "gak": "tidak", "ga": "tidak", "nggak": "tidak", "engga": "tidak",
    "bgt": "banget", "bgtt": "banget", "bngt": "banget",
    "sm": "sama", "sma": "sama", "dgn": "dengan",
    "yg": "yang", "utk": "untuk", "krn": "karena",
    "sdh": "sudah", "udh": "sudah", "blm": "belum",
    "bkn": "bukan", "tp": "tapi", "tpi": "tapi",
    "aja": "saja", "aj": "saja", "doang": "saja",
    "ak": "aku", "aq": "aku", "gw": "aku", "gue": "aku",
    "km": "kamu", "kmu": "kamu", "lu": "kamu", "lo": "kamu",
}

def normalisasi_teks(teks):
    teks = str(teks).lower()
    kata = teks.split()
    kata_normal = [KAMUS_GAUL.get(k, k) for k in kata]
    return " ".join(kata_normal)

def load_split(nama):
    df = pd.read_csv(PROCESSED / f"{nama}.csv")
    df["text"] = df["text"].map(normalisasi_teks)
    return df

def main():
    print("Memuat data...")
    train = load_split("train")
    valid = load_split("valid")
    test = load_split("test")

    # --- 2. FEATURE ENGINEERING: GABUNG TF-IDF KATA & KARAKTER ---
    # Fitur kata (n-gram 1-2) menangkap konteks kalimat.
    # Fitur karakter (n-gram 3-5) menangkap typo/singkatan (cocok untuk Twitter).
    fitur_gabungan = FeatureUnion([
        ("kata", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
        ("karakter", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000))
    ])

    # --- 3. PIPELINE & GRID SEARCH UNTUK LOGISTIC REGRESSION ---
    pipeline_logreg = Pipeline([
        ("fitur", fitur_gabungan),
        ("clf", LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced"))
    ])

    # Coba beberapa nilai C (semakin kecil C, semakin kuat regularisasinya)
    param_grid_logreg = {
        "clf__C": [0.1, 1.0, 10.0]
    }

    print("\n>>> Melakukan GridSearchCV untuk LogReg (mencari C terbaik)...")
    grid_logreg = GridSearchCV(pipeline_logreg, param_grid_logreg, cv=3, scoring="f1_macro", n_jobs=-1)
    grid_logreg.fit(train["text"], train["label"])

    print(f"Parameter terbaik LogReg: {grid_logreg.best_params_}")
    best_logreg = grid_logreg.best_estimator_

    # Evaluasi di Validasi
    pred_valid_lr = best_logreg.predict(valid["text"])
    res_valid_lr = evaluate_macro_f1(valid["label"], pred_valid_lr, LABEL_UTAMA)
    print(f"[LogReg Tuned] Macro F1 valid: {res_valid_lr['macro_f1']:.4f}")

    # Evaluasi di Test
    pred_test_lr = best_logreg.predict(test["text"])
    res_test_lr = evaluate_macro_f1(test["label"], pred_test_lr, LABEL_UTAMA)
    print_evaluation(res_test_lr, title="LogReg Tuned — TEST")

    # --- 4. PIPELINE & GRID SEARCH UNTUK SVM ---
    pipeline_svm = Pipeline([
        ("fitur", FeatureUnion([
            ("kata", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ("karakter", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000))
        ])),
        ("clf", LinearSVC(random_state=42, class_weight="balanced"))
    ])

    param_grid_svm = {
        "clf__C": [0.1, 1.0, 10.0]
    }

    print("\n>>> Melakukan GridSearchCV untuk SVM (mencari C terbaik)...")
    grid_svm = GridSearchCV(pipeline_svm, param_grid_svm, cv=3, scoring="f1_macro", n_jobs=-1)
    grid_svm.fit(train["text"], train["label"])

    print(f"Parameter terbaik SVM: {grid_svm.best_params_}")
    best_svm = grid_svm.best_estimator_

    # Evaluasi di Validasi
    pred_valid_svm = best_svm.predict(valid["text"])
    res_valid_svm = evaluate_macro_f1(valid["label"], pred_valid_svm, LABEL_UTAMA)
    print(f"[SVM Tuned] Macro F1 valid: {res_valid_svm['macro_f1']:.4f}")

    # Evaluasi di Test
    pred_test_svm = best_svm.predict(test["text"])
    res_test_svm = evaluate_macro_f1(test["label"], pred_test_svm, LABEL_UTAMA)
    print_evaluation(res_test_svm, title="SVM Tuned — TEST")

    # --- 5. RINGKASAN ---
    print("\n===== RINGKASAN TUNING =====")
    print(f"{'Model':<15} {'Valid':>8} {'Test':>8}")
    print(f"{'LogReg Tuned':<15} {res_valid_lr['macro_f1']:>8.4f} {res_test_lr['macro_f1']:>8.4f}")
    print(f"{'SVM Tuned':<15} {res_valid_svm['macro_f1']:>8.4f} {res_test_svm['macro_f1']:>8.4f}")

if __name__ == "__main__":
    main()