"""Fungsi evaluasi standar untuk semua model TextScope.

Semua model (baseline & transformer) WAJIB dinilai dengan fungsi ini
supaya perbandingan adil. Metrik utama: Macro F1.
"""
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
)


def evaluate_macro_f1(y_true, y_pred, label_names=None):
    """Hitung Macro F1 + laporan per kelas + confusion matrix.

    Args:
        y_true: array-like label asli
        y_pred: array-like label prediksi
        label_names: list nama kelas (opsional, untuk urutan laporan)

    Returns:
        dict berisi macro_f1, report, confusion_matrix
    """
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    report = classification_report(
        y_true, y_pred, labels=label_names, digits=4, zero_division=0
    )
    cm = confusion_matrix(y_true, y_pred, labels=label_names)

    return {
        "macro_f1": macro_f1,
        "report": report,
        "confusion_matrix": cm,
    }


def print_evaluation(result, title="Evaluasi"):
    """Cetak hasil evaluasi dengan rapi."""
    print(f"\n===== {title} =====")
    print(f"Macro F1: {result['macro_f1']:.4f}")
    print("\nLaporan per kelas:")
    print(result["report"])
    print("Confusion matrix:")
    print(result["confusion_matrix"])


if __name__ == "__main__":
    # Contoh pemakaian (dummy) — untuk tes fungsi jalan
    y_true = ["joy", "sad", "anger", "joy", "sad"]
    y_pred = ["joy", "sad", "joy", "joy", "anger"]
    labels = ["anger", "fear", "joy", "love", "sad", "neutral"]
    hasil = evaluate_macro_f1(y_true, y_pred, label_names=labels)
    print_evaluation(hasil, title="Contoh Dummy")