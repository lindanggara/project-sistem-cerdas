
import os
import time
import pandas as pd
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ============================================================
# TEXTSCOPE - ANALISIS CONFIDENCE INDOBERT PADA DATASET EMOT
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "emot_lintas.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "indobert"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR, "models", "indobert", "cross_domain_emot"
)

MAX_LENGTH = 128
BATCH_SIZE = 16

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("TEXTSCOPE - ANALISIS CONFIDENCE INDOBERT")
print("=" * 60)

# 1. Memuat dataset
print("\n[1] MEMUAT DATASET EMOT")

df = pd.read_csv(DATA_PATH)
print("Jumlah data:", len(df))

# 2. Memuat model dan tokenizer
print("\n[2] MEMUAT MODEL INDOBERT")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(device)
model.eval()

id2label = {
    int(k): v for k, v in model.config.id2label.items()
}

print("Device:", device)
print("Label map:", id2label)

# 3. Prediksi probabilitas
print("\n[3] MENGHITUNG PROBABILITAS")

all_probabilities = []

start_time = time.time()

texts = df["text"].fillna("").astype(str).tolist()

with torch.inference_mode():
    for start in range(0, len(texts), BATCH_SIZE):

        batch_texts = texts[start:start + BATCH_SIZE]

        inputs = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits, dim=1
        )

        all_probabilities.extend(
            probabilities.cpu().numpy()
        )

        selesai = min(start + BATCH_SIZE, len(texts))
        print(
            f"\rProgress: {selesai}/{len(texts)}",
            end=""
        )

print("\nWaktu:", round(time.time() - start_time, 2), "detik")

# 4. Menyimpan confidence setiap kelas
prob_array = np.array(all_probabilities)

for class_id, label in id2label.items():
    df[f"prob_{label}"] = prob_array[:, class_id]

# Confidence tertinggi dan prediksi berdasarkan probabilitas
df["confidence"] = prob_array.max(axis=1)

df["prediksi_confidence"] = [
    id2label[int(idx)]
    for idx in prob_array.argmax(axis=1)
]

# 5. Analisis prediksi neutral
print("\n[4] ANALISIS CONFIDENCE PREDIKSI NEUTRAL")

neutral_df = df[df["prediksi_confidence"] == "neutral"]

print("Jumlah prediksi neutral:", len(neutral_df))

if len(neutral_df) > 0:
    print(
        "Rata-rata confidence neutral:",
        round(neutral_df["prob_neutral"].mean(), 4)
    )

    print(
        "Median confidence neutral:",
        round(neutral_df["prob_neutral"].median(), 4)
    )

# 6. Confidence berdasarkan label asli
print("\n[5] CONFIDENCE BERDASARKAN LABEL ASLI")

summary = df.groupby("label").agg(
    jumlah_data=("text", "count"),
    rata_rata_confidence=("confidence", "mean"),
    rata_rata_prob_neutral=("prob_neutral", "mean"),
    jumlah_prediksi_neutral=(
        "prediksi_confidence",
        lambda x: (x == "neutral").sum()
    )
).round(4)

print(summary)

# 7. Menampilkan contoh prediksi neutral
print("\n[6] 15 CONTOH PREDIKSI NEUTRAL")

columns = [
    "text",
    "label",
    "confidence",
    "prob_neutral"
]

print(
    neutral_df[columns]
    .sort_values("confidence", ascending=False)
    .head(15)
    .to_string(index=False)
)

# 8. Menyimpan hasil
output_path = os.path.join(
    OUTPUT_DIR, "analisis_confidence_emot.csv"
)

summary_path = os.path.join(
    OUTPUT_DIR, "ringkasan_confidence_emot.csv"
)

df.to_csv(output_path, index=False)
summary.to_csv(summary_path)

print("\n[7] HASIL BERHASIL DISIMPAN")
print(output_path)
print(summary_path)

print("\nANALISIS CONFIDENCE SELESAI!")
