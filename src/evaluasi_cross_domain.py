"""Evaluasi lintas domain (EmoT) untuk model klasik.

Jalankan: python src/evaluasi_cross_domain.py
Input : data/processed/train.csv, data/processed/emot_lintas.csv
"""
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import classification_report, f1_score

# 1. TAMBAHKAN DEFINISI ROOT DI SINI
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Label untuk data lintas domain (tanpa neutral)
LABEL_LINTAS = ["anger", "fear", "joy", "love", "sad"]

# Kamus normalisasi (sama seperti baseline)
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

def load_data(nama):
    # 2. PASTIKAN PATH MENGGUNAKAN ROOT
    df = pd.read_csv(ROOT / "data" / "processed" / f"{nama}.csv")
    df["text"] = df["text"].map(normalisasi_teks)
    return df

def main():
    print("Memuat data...")
    train = load_data("train")
    emot_test = load_data("emot_lintas")

    print("\n>>> Melatih model LogReg Tuned (terbaik) dengan fitur gabungan...")
    # Menggunakan arsitektur yang sama dengan tuning terbaik
    model = Pipeline([
        ("fitur", FeatureUnion([
            ("kata", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ("karakter", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000))
        ])),
        ("clf", LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced", C=1.0))
    ])
    model.fit(train["text"], train["label"])

    print("\n>>> Mengevaluasi pada dataset EmoT (lintas domain)...")
    pred_emot = model.predict(emot_test["text"])

    # Evaluasi Khusus EmoT (hanya 5 kelas, tanpa neutral)
    macro_f1_emot = f1_score(emot_test["label"], pred_emot, average="macro", labels=LABEL_LINTAS)
    
    print(f"Macro F1 (EmoT): {macro_f1_emot:.4f}")
    print("\nLaporan per kelas (EmoT):")
    print(classification_report(emot_test["label"], pred_emot, labels=LABEL_LINTAS, digits=4, zero_division=0))

if __name__ == "__main__":
    main()