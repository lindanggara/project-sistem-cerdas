
"""
TEXTSCOPE - FINE-TUNING INDOBERT

Uji awal:
    python src/train_indobert.py --smoke-test

Training penuh:
    python src/train_indobert.py

Input:
    data/processed/train.csv
    data/processed/valid.csv
    data/processed/test.csv

Output:
    models/indobert_smoke_test/
    models/indobert/
"""

import argparse
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader

from transformers import (
    AutoTokenizer,
    AutoConfig,
    AutoModelForSequenceClassification,
)

from evaluate import (
    LABEL_UTAMA,
    evaluate_macro_f1,
    print_evaluation,
)


# ============================================================
# 1. KONFIGURASI
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "models"

MODEL_NAME = "indobenchmark/indobert-base-p1"

LABEL_TO_ID = {
    label: index
    for index, label in enumerate(LABEL_UTAMA)
}

ID_TO_LABEL = {
    index: label
    for label, index in LABEL_TO_ID.items()
}

NUM_LABELS = len(LABEL_UTAMA)

MAX_LENGTH = 128
BATCH_SIZE = 4
EPOCHS = 1
LEARNING_RATE = 2e-5
RANDOM_STATE = 42

DEVICE = torch.device("cpu")

# Membatasi penggunaan thread CPU.
torch.set_num_threads(4)


# ============================================================
# 2. RANDOM SEED
# ============================================================

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# ============================================================
# 3. MEMUAT DATASET
# ============================================================

def load_data(smoke_test=False):

    train_df = pd.read_csv(DATA_DIR / "train.csv")
    valid_df = pd.read_csv(DATA_DIR / "valid.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    datasets = {
        "train": train_df,
        "valid": valid_df,
        "test": test_df,
    }

    for name, df in datasets.items():

        if not {"text", "label"}.issubset(df.columns):
            raise ValueError(
                f"{name}.csv harus memiliki kolom text dan label."
            )

        df.dropna(subset=["text", "label"], inplace=True)

        df["text"] = df["text"].astype(str).str.strip()

        df["label"] = (
            df["label"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        df.drop(
            df[df["text"] == ""].index,
            inplace=True,
        )

        invalid_labels = set(df["label"].unique()) - set(LABEL_UTAMA)

        if invalid_labels:
            raise ValueError(
                f"Label tidak dikenal pada {name}: {invalid_labels}"
            )

    # Smoke test dengan sampel stratified.
    if smoke_test:

        print("\nMODE UJI AWAL: menggunakan sampel stratified.")

        train_df = (
            train_df.groupby("label", group_keys=False)
            .sample(n=10, random_state=RANDOM_STATE)
            .reset_index(drop=True)
        )

        valid_df = (
            valid_df.groupby("label", group_keys=False)
            .sample(n=4, random_state=RANDOM_STATE)
            .reset_index(drop=True)
        )

        test_df = (
            test_df.groupby("label", group_keys=False)
            .sample(n=4, random_state=RANDOM_STATE)
            .reset_index(drop=True)
        )

    # Memastikan semua kelas tersedia.
    for name, df in [
        ("train", train_df),
        ("valid", valid_df),
        ("test", test_df),
    ]:

        missing = set(LABEL_UTAMA) - set(df["label"].unique())

        if missing:
            raise ValueError(
                f"Kelas berikut tidak ditemukan di {name}: {missing}"
            )

    print("\nJumlah data yang digunakan:")
    print("Train     :", len(train_df))
    print("Validation:", len(valid_df))
    print("Test      :", len(test_df))

    print("\nSebaran label training:")
    print(train_df["label"].value_counts().to_string())

    return train_df, valid_df, test_df


# ============================================================
# 4. DATASET PYTORCH
# ============================================================

class EmotionDataset(Dataset):

    def __init__(self, dataframe, tokenizer):

        self.texts = dataframe["text"].tolist()

        self.labels = [
            LABEL_TO_ID[label]
            for label in dataframe["label"].tolist()
        ]

        self.encodings = tokenizer(
            self.texts,
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):

        item = {
            key: value[index]
            for key, value in self.encodings.items()
        }

        item["labels"] = torch.tensor(
            self.labels[index],
            dtype=torch.long,
        )

        return item


# ============================================================
# 5. MEMUAT TOKENIZER
# ============================================================

def load_tokenizer():

    print("\nMemuat tokenizer IndoBERT...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    return tokenizer


# ============================================================
# 6. MEMUAT MODEL INDOBERT
# ============================================================

def load_model():

    print("\nMemuat konfigurasi IndoBERT...")

    config = AutoConfig.from_pretrained(MODEL_NAME)

    # Mengatur enam kelas emosi TextScope.
    config.num_labels = NUM_LABELS
    config.id2label = ID_TO_LABEL
    config.label2id = LABEL_TO_ID

    print("Jumlah kelas:", config.num_labels)
    print("Mapping label:", config.id2label)

    print("\nMemuat model pretrained...")

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        config=config,
        ignore_mismatched_sizes=True,
    )

    model.to(DEVICE)

    return model


# ============================================================
# 7. TRAINING SATU EPOCH
# ============================================================

def train_one_epoch(model, loader, optimizer):

    model.train()

    total_loss = 0.0

    start_time = time.time()

    for step, batch in enumerate(loader, start=1):

        optimizer.zero_grad()

        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )

        loss = outputs.loss

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0,
        )

        optimizer.step()

        total_loss += loss.item()

        if step % 10 == 0 or step == len(loader):

            print(
                f"Batch {step}/{len(loader)} "
                f"| Loss: {loss.item():.4f}"
            )

    average_loss = total_loss / len(loader)

    duration = time.time() - start_time

    print(f"\nRata-rata training loss: {average_loss:.4f}")
    print(f"Waktu training: {duration:.2f} detik")

    return average_loss


# ============================================================
# 8. PREDIKSI
# ============================================================

def predict(model, loader):

    model.eval()

    all_predictions = []
    all_labels = []

    with torch.no_grad():

        for batch in loader:

            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

            predictions = torch.argmax(
                outputs.logits,
                dim=1,
            )

            all_predictions.extend(
                predictions.cpu().tolist()
            )

            all_labels.extend(
                labels.cpu().tolist()
            )

    y_true = [
        ID_TO_LABEL[index]
        for index in all_labels
    ]

    y_pred = [
        ID_TO_LABEL[index]
        for index in all_predictions
    ]

    return y_true, y_pred


# ============================================================
# 9. EVALUASI
# ============================================================

def evaluate_model(model, loader, title):

    y_true, y_pred = predict(model, loader)

    result = evaluate_macro_f1(
        y_true,
        y_pred,
        label_names=LABEL_UTAMA,
    )

    print_evaluation(result, title)

    return result, y_true, y_pred


# ============================================================
# 10. MENYIMPAN HASIL
# ============================================================

def save_results(
    output_dir,
    validation_result,
    test_result,
    test_df,
    y_test_true,
    y_test_pred,
    train_size,
    valid_size,
    smoke_test,
):

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Ringkasan evaluasi.
    summary = pd.DataFrame([
        {
            "model": MODEL_NAME,
            "macro_f1_validation": validation_result["macro_f1"],
            "accuracy_validation": validation_result["accuracy"],
            "macro_f1_test": test_result["macro_f1"],
            "accuracy_test": test_result["accuracy"],
            "training_data": train_size,
            "validation_data": valid_size,
            "test_data": len(test_df),
            "smoke_test": smoke_test,
        }
    ])

    summary.to_csv(
        output_dir / "hasil_evaluasi.csv",
        index=False,
    )

    # Prediksi harus sesuai dengan sampel test yang benar.
    prediction_df = pd.DataFrame({
        "text": test_df["text"].tolist(),
        "label_asli": y_test_true,
        "label_prediksi": y_test_pred,
    })

    prediction_df.to_csv(
        output_dir / "prediksi_test.csv",
        index=False,
        encoding="utf-8",
    )

    print("\nFile evaluasi berhasil disimpan.")


# ============================================================
# 11. PROGRAM UTAMA
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Menjalankan uji awal dengan sebagian kecil data.",
    )

    args = parser.parse_args()

    set_seed(RANDOM_STATE)

    print("=" * 55)
    print("TEXTSCOPE - FINE-TUNING INDOBERT")
    print("=" * 55)

    print("Device:", DEVICE)
    print("Model :", MODEL_NAME)
    print("Kelas :", NUM_LABELS)

    # Memuat data.
    train_df, valid_df, test_df = load_data(
        smoke_test=args.smoke_test
    )

    # Menentukan folder output.
    if args.smoke_test:
        output_dir = MODEL_DIR / "indobert_smoke_test"
    else:
        output_dir = MODEL_DIR / "indobert"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Memuat tokenizer.
    tokenizer = load_tokenizer()

    # Membuat dataset.
    train_dataset = EmotionDataset(train_df, tokenizer)
    valid_dataset = EmotionDataset(valid_df, tokenizer)
    test_dataset = EmotionDataset(test_df, tokenizer)

    # Membuat DataLoader.
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
    )

    valid_loader = DataLoader(
        valid_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
    )

    # Memuat model.
    model = load_model()

    # Optimizer.
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    best_valid_f1 = -1.0
    best_epoch = 0
    best_valid_result = None

    # --------------------------------------------------------
    # TRAINING
    # --------------------------------------------------------

    for epoch in range(EPOCHS):

        print("\n" + "=" * 55)
        print(f"EPOCH {epoch + 1}/{EPOCHS}")
        print("=" * 55)

        train_one_epoch(
            model,
            train_loader,
            optimizer,
        )

        # Evaluasi validation.
        valid_result, _, _ = evaluate_model(
            model,
            valid_loader,
            "VALIDATION",
        )

        # Simpan model terbaik.
        if valid_result["macro_f1"] > best_valid_f1:

            best_valid_f1 = valid_result["macro_f1"]
            best_epoch = epoch + 1
            best_valid_result = valid_result

            model.save_pretrained(
                output_dir,
                safe_serialization=True,
            )

            tokenizer.save_pretrained(output_dir)

            print("\nModel terbaik berhasil disimpan.")

    # --------------------------------------------------------
    # MEMUAT MODEL TERBAIK
    # --------------------------------------------------------

    print("\nMemuat model terbaik...")

    best_model = AutoModelForSequenceClassification.from_pretrained(
        output_dir
    )

    best_model.to(DEVICE)

    # --------------------------------------------------------
    # EVALUASI TEST
    # --------------------------------------------------------

    print("\nEpoch terbaik:", best_epoch)

    test_result, y_test_true, y_test_pred = evaluate_model(
        best_model,
        test_loader,
        "TEST",
    )

    # --------------------------------------------------------
    # MENYIMPAN HASIL
    # --------------------------------------------------------

    save_results(
        output_dir=output_dir,
        validation_result=best_valid_result,
        test_result=test_result,
        test_df=test_df,
        y_test_true=y_test_true,
        y_test_pred=y_test_pred,
        train_size=len(train_df),
        valid_size=len(valid_df),
        smoke_test=args.smoke_test,
    )

    print("\n" + "=" * 55)
    print("EKSPERIMEN SELESAI")
    print("=" * 55)

    print("Macro F1 Validation:", round(best_valid_f1, 4))
    print("Macro F1 Test      :", round(test_result["macro_f1"], 4))

    print("Lokasi model :", output_dir)
    print("Lokasi hasil :", output_dir / "hasil_evaluasi.csv")


if __name__ == "__main__":
    main()
