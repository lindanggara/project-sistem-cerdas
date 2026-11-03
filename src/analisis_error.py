"""Analisis error: ambil contoh teks yang salah ditebak model terbaik.

Jalankan: python src/analisis_error.py
Input : data/processed/train.csv, data/processed/test.csv
"""
import sys
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseline import normalisasi_teks, KAMUS_GAUL

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"

def load_data(nama):
    df = pd.read_csv(PROCESSED / f"{nama}.csv")
    df["text"] = df["text"].map(normalisasi_teks)
    return df

def main():
    print("Memuat data...")
    train = load_data("train")
    test = load_data("test")

    print("Melatih model LogReg Tuned (terbaik)...")
    model = Pipeline([
        ("fitur", FeatureUnion([
            ("kata", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ("karakter", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000))
        ])),
        ("clf", LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced", C=1.0))
    ])
    model.fit(train["text"], train["label"])

    print("Memprediksi data uji...")
    test["prediksi"] = model.predict(test["text"])

    # Filter yang salah tebak
    salah = test[test["label"] != test["prediksi"]].copy()
    print(f"\nTotal salah tebak: {len(salah)} dari {len(test)} baris ({len(salah)/len(test)*100:.1f}%)\n")

    # 1. Tampilkan 10 pasangan kesalahan terbanyak
    print("=== 10 Pasangan Kesalahan Terbanyak ===")
    pasangan = salah.groupby(["label", "prediksi"]).size().sort_values(ascending=False).head(10)
    print(pasangan.to_string())

    # 2. Ambil 2 contoh teks untuk 5 pasangan teratas
    print("\n=== Contoh Teks Salah Tebak ===")
    for (asli, prediksi), jumlah in pasangan.head(5).items():
        print(f"\n[Asli: {asli.upper()} -> Ditebak: {prediksi.upper()}] ({jumlah} kasus)")
        contoh = salah[(salah["label"] == asli) & (salah["prediksi"] == prediksi)]["text"].head(2).tolist()
        for teks in contoh:
            print(f"  - {teks[:100]}...")

if __name__ == "__main__":
    main()