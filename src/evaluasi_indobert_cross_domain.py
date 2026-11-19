
"""
TEXTSCOPE - EVALUASI LINTAS DOMAIN INDOBERT
Menguji model IndoBERT pada dataset EmoT IndoNLU.

Input:
- models/indobert
- data/processed/emot_lintas.csv

Output:
- models/indobert/cross_domain_emot/
"""

from pathlib import Path
import sys
import time

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Mengimpor evaluator standar kelompok
from evaluate import evaluate_macro_f1, print_evaluation, LABEL_LINTAS


# =====================================================
# 1. KONFIGURASI
# =====================================================

ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = ROOT / "models" / "indobert"
DATA_PATH = ROOT / "data" / "processed" / "emot_lintas.csv"

OUTPUT_DIR = MODEL_DIR / "cross_domain_emot"

MAX_LENGTH = 128
BATCH_SIZE = 16

DEVICE = torch.device("cpu")

torch.set_num_threads(4)


# =====================================================
# 2. MEMUAT DATASET
# =====================================================

def load_data():
    print("\n[1] MEMUAT DATASET EMOT")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {"text", "label"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            "Dataset harus memiliki kolom text dan label."
        )

    df = df.dropna(subset=["text", "label"]).copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip().str.lower()

    df = df[df["text"] != ""].reset_index(drop=True)

    label_invalid = set(df["label"].unique()) - set(LABEL_LINTAS)

    if label_invalid:
        raise ValueError(
            f"Ditemukan label tidak dikenal: {label_invalid}"
        )

    print(f"Jumlah data : {len(df)}")
    print("\nDistribusi label:")
    print(df["label"].value_counts())

    return df


# =====================================================
# 3. MEMUAT MODEL INDOBERT
# =====================================================

def load_model():
    print("\n[2] MEMUAT MODEL INDOBERT")

    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"Folder model tidak ditemukan: {MODEL_DIR}"
        )

    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_DIR)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(MODEL_DIR)
    )

    model.to(DEVICE)
    model.eval()

    # Membaca pemetaan label dari konfigurasi model
    id2label = {
        int(k): str(v).lower()
        for k, v in model.config.id2label.items()
    }

    print(f"Model     : {MODEL_DIR}")
    print(f"Device    : {DEVICE}")
    print(f"Label map : {id2label}")

    if set(id2label.values()) != set(
        ["anger", "fear", "joy", "love", "sad", "neutral"]
    ):
        raise ValueError(
            "Pemetaan label model tidak sesuai LABEL_UTAMA."
        )

    return tokenizer, model, id2label


# =====================================================
# 4. PREDIKSI DATA EMOT
# =====================================================

def predict_emot(df, tokenizer, model, id2label):
    print("\n[3] MELAKUKAN PREDIKSI EMOT")

    predictions = []

    start_time = time.time()

    texts = df["text"].tolist()

    with torch.inference_mode():

        for start in range(0, len(texts), BATCH_SIZE):

            batch_texts = texts[start:start + BATCH_SIZE]

            encoded = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt"
            )

            encoded = {
                key: value.to(DEVICE)
                for key, value in encoded.items()
            }

            outputs = model(**encoded)

            predicted_ids = torch.argmax(
                outputs.logits,
                dim=1
            ).cpu().tolist()

            batch_predictions = [
                id2label[idx]
                for idx in predicted_ids
            ]

            predictions.extend(batch_predictions)

            selesai = min(start + BATCH_SIZE, len(texts))

            print(
                f"\rProgress: {selesai}/{len(texts)} data",
                end="",
                flush=True
            )

    elapsed = time.time() - start_time

    print(f"\nWaktu prediksi: {elapsed:.2f} detik")

    return predictions, elapsed


# =====================================================
# 5. EVALUASI MENGGUNAKAN EVALUATOR KELOMPOK
# =====================================================

def evaluate_emot(df, predictions):
    print("\n[4] EVALUASI LINTAS DOMAIN")

    y_true = df["label"].tolist()
    y_pred = predictions

    # Wajib menggunakan evaluator standar kelompok.
    # Prediksi neutral tetap dihitung sebagai kesalahan.
    result = evaluate_macro_f1(
        y_true,
        y_pred,
        label_names=LABEL_LINTAS
    )

    print_evaluation(
        result,
        title="INDOBERT - CROSS DOMAIN EMOT"
    )

    jumlah_neutral = sum(
        pred == "neutral" for pred in y_pred
    )

    print(
        f"\nPrediksi neutral: {jumlah_neutral} "
        f"({jumlah_neutral / len(y_pred) * 100:.2f}%)"
    )

    return result


# =====================================================
# 6. MENYIMPAN HASIL
# =====================================================

def save_results(df, predictions, result, elapsed):
    print("\n[5] MENYIMPAN HASIL")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Menyimpan seluruh prediksi
    df_pred = df.copy()
    df_pred["prediksi"] = predictions

    pred_path = OUTPUT_DIR / "prediksi_emot.csv"
    df_pred.to_csv(pred_path, index=False)

    # Menyimpan ringkasan metrik
    summary = pd.DataFrame([{
        "model": "IndoBERT",
        "dataset": "EmoT IndoNLU",
        "jumlah_data": len(df),
        "macro_f1": result["macro_f1"],
        "accuracy": result["accuracy"],
        "waktu_prediksi_detik": elapsed,
        "prediksi_neutral": predictions.count("neutral")
    }])

    summary_path = OUTPUT_DIR / "hasil_evaluasi_emot.csv"
    summary.to_csv(summary_path, index=False)

    # Menyimpan laporan per kelas
    report = pd.DataFrame(result["report_dict"]).T

    report_path = OUTPUT_DIR / "laporan_per_kelas_emot.csv"
    report.to_csv(report_path)

    # Menyimpan confusion matrix
    cm = pd.DataFrame(
        result["confusion_matrix"],
        index=LABEL_LINTAS,
        columns=LABEL_LINTAS
    )

    cm_path = OUTPUT_DIR / "confusion_matrix_emot.csv"
    cm.to_csv(cm_path)

    print("\nFile berhasil disimpan:")
    print(pred_path)
    print(summary_path)
    print(report_path)
    print(cm_path)


# =====================================================
# 7. MAIN PROGRAM
# =====================================================

def main():
    print("=" * 60)
    print("TEXTSCOPE - INDOBERT CROSS DOMAIN EVALUATION")
    print("=" * 60)

    df = load_data()

    tokenizer, model, id2label = load_model()

    predictions, elapsed = predict_emot(
        df,
        tokenizer,
        model,
        id2label
    )

    result = evaluate_emot(
        df,
        predictions
    )

    save_results(
        df,
        predictions,
        result,
        elapsed
    )

    print("\n" + "=" * 60)
    print("EVALUASI LINTAS DOMAIN SELESAI!")
    print("=" * 60)


if __name__ == "__main__":
    main()
