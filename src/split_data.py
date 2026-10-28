"""Split dataset emosi bersih menjadi train/valid/test secara stratified.

Jalankan: python src/split_data.py
Input : data/processed/emosi_bersih.csv  (kolom: text, label)
Output: data/processed/train.csv
        data/processed/valid.csv
        data/processed/test.csv
"""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RANDOM_STATE = 42          # JANGAN diubah — biar split reproducible
TEST_SIZE = 0.15
VALID_SIZE = 0.15          # dari total, jadi valid = 0.15, test = 0.15


def main():
    df = pd.read_csv(PROCESSED / "emosi_bersih.csv")
    print(f"Total baris bersih: {len(df)}")
    print("Sebaran label:")
    print(df["label"].value_counts().to_string())

    # Split 1: train vs (valid+test)
    train, temp = train_test_split(
        df,
        test_size=(TEST_SIZE + VALID_SIZE),
        stratify=df["label"],
        random_state=RANDOM_STATE,
    )
    # Split 2: valid vs test
    valid, test = train_test_split(
        temp,
        test_size=TEST_SIZE / (TEST_SIZE + VALID_SIZE),
        stratify=temp["label"],
        random_state=RANDOM_STATE,
    )

    # Cek no leakage
    set_train = set(train["text"])
    set_valid = set(valid["text"])
    set_test = set(test["text"])
    assert set_train.isdisjoint(set_valid), "LEAKAGE: train & valid ada teks sama!"
    assert set_train.isdisjoint(set_test),  "LEAKAGE: train & test ada teks sama!"
    assert set_valid.isdisjoint(set_test),  "LEAKAGE: valid & test ada teks sama!"
    print("\n✅ Tidak ada leakage antar split")

    # Simpan
    train.to_csv(PROCESSED / "train.csv", index=False, encoding="utf-8")
    valid.to_csv(PROCESSED / "valid.csv", index=False, encoding="utf-8")
    test.to_csv(PROCESSED / "test.csv", index=False, encoding="utf-8")

    print(f"\ntrain: {len(train)} baris")
    print(f"valid: {len(valid)} baris")
    print(f"test : {len(test)} baris")
    print("\nSebaran label per split:")
    for nama, d in [("train", train), ("valid", valid), ("test", test)]:
        print(f"\n[{nama}]")
        print(d["label"].value_counts().to_string())


if __name__ == "__main__":
    main()