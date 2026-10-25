"""Unduh dua dataset emosi lalu rapikan.

Jalankan dari folder proyek:  python src/download_data.py
Hasil (tidak di-commit ke Git, karena ada di .gitignore):
  DATASET UTAMA  - Emotion Dataset from Indonesian Public Opinion (6 emosi)
    data/raw/emosi_opini_publik/*.csv   berkas asli per emosi
    data/processed/emosi_gabungan.csv   semua baris (kolom: text, label)
    data/processed/emosi_bersih.csv     tanpa teks kembar dan tanpa teks berlabel ganda
  DATASET UJI LINTAS - EmoT dari IndoNLU (5 emosi, tanpa netral)
    data/raw/emot/*.csv                 berkas asli (train, valid, test)
    data/processed/emot_lintas.csv      kolom: text, label, split_asli
Sumber dan lisensi: lihat README (dataset utama CC-BY-NC-ND 4.0 menurut katalog NusaCrowd;
cek lisensi IndoNLU di repositorinya).
"""
import csv
import urllib.request
from pathlib import Path

import pandas as pd

BASE = ("https://raw.githubusercontent.com/Ricco48/"
        "Emotion-Dataset-from-Indonesian-Public-Opinion/main/"
        "Emotion%20Dataset%20from%20Indonesian%20Public%20Opinion")
EMOSI = ["Anger", "Fear", "Joy", "Love", "Sad", "Neutral"]

EMOT_BASE = ("https://raw.githubusercontent.com/indobenchmark/indonlu/"
             "master/dataset/emot_emotion-twitter")
EMOT_SPLITS = ["train", "valid", "test"]
# Samakan nama label EmoT dengan dataset utama.
PETA_LABEL_EMOT = {"anger": "anger", "fear": "fear", "happy": "joy", "love": "love", "sadness": "sad"}

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "emosi_opini_publik"
RAW_EMOT = ROOT / "data" / "raw" / "emot"
OUT = ROOT / "data" / "processed"


def unduh(nama):
    tujuan = RAW / f"{nama}Data.csv"
    if not tujuan.exists():
        print(f"Mengunduh {nama}Data.csv ...")
        urllib.request.urlretrieve(f"{BASE}/{nama}Data.csv", tujuan)
    return tujuan


def siapkan_emot():
    """EmoT: berkas berkoma dengan baris judul 'label,tweet'. Penanda [USERNAME] dan [URL]
    dibuang agar mirip dataset utama, yang sudah bersih dari mention dan tautan."""
    RAW_EMOT.mkdir(parents=True, exist_ok=True)
    frames = []
    for split in EMOT_SPLITS:
        tujuan = RAW_EMOT / f"{split}_preprocess.csv"
        if not tujuan.exists():
            print(f"Mengunduh EmoT {split} ...")
            urllib.request.urlretrieve(f"{EMOT_BASE}/{split}_preprocess.csv", tujuan)
        d = pd.read_csv(tujuan)
        d["split_asli"] = split
        frames.append(d)
    df = pd.concat(frames, ignore_index=True).rename(columns={"tweet": "text"})
    df["text"] = (df["text"].fillna("").astype(str)
                  .str.replace(r"\[(USERNAME|URL)\]", " ", regex=True)
                  .str.replace(r"\s+", " ", regex=True).str.strip())
    df["label"] = df["label"].str.strip().str.lower().map(PETA_LABEL_EMOT)
    df = df[(df["text"] != "") & df["label"].notna()].drop_duplicates("text")
    df[["text", "label", "split_asli"]].to_csv(OUT / "emot_lintas.csv", index=False, encoding="utf-8")
    print("\nEmoT (uji lintas):", len(df), "baris")
    print(df["label"].value_counts().to_string())


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    frames = []
    for nama in EMOSI:
        # Berkas dipisah tab, kolom: Tweet dan Label. quoting=NONE agar tanda kutip di teks tidak merusak baca.
        d = pd.read_csv(unduh(nama), sep="\t", quoting=csv.QUOTE_NONE, encoding="utf-8")
        frames.append(d.rename(columns={"Tweet": "text", "Label": "label"}))
    df = pd.concat(frames, ignore_index=True)
    df["text"] = df["text"].fillna("").astype(str).str.strip()
    df["label"] = df["label"].str.strip().str.lower()
    df = df[df["text"] != ""]
    df.to_csv(OUT / "emosi_gabungan.csv", index=False, encoding="utf-8")

    # Teks yang sama dengan label berbeda dibuang seluruhnya, sisanya dedup.
    jumlah_label = df.groupby("text")["label"].nunique()
    konflik = set(jumlah_label[jumlah_label > 1].index)
    bersih = df[~df["text"].isin(konflik)].drop_duplicates("text")
    bersih.to_csv(OUT / "emosi_bersih.csv", index=False, encoding="utf-8")

    print(f"\nTotal baris        : {len(df)}")
    print(f"Teks kembar        : {int(df.duplicated('text').sum())}")
    print(f"Teks label ganda   : {len(konflik)}")
    print(f"Baris setelah bersih: {len(bersih)}\n")
    print("Sebaran label (bersih):")
    print(bersih["label"].value_counts().to_string())

    siapkan_emot()


if __name__ == "__main__":
    main()
