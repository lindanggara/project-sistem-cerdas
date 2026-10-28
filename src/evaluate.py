"""Fungsi evaluasi standar untuk semua model TextScope.

Semua model (baseline & transformer) WAJIB dinilai dengan fungsi ini
supaya perbandingan adil. Metrik utama: Macro F1.

Catatan penting soal `label_names`:
- Data utama (6 kelas)        -> pakai LABEL_UTAMA
- Uji lintas EmoT (5 kelas)   -> pakai LABEL_LINTAS (tanpa 'neutral')
  Prediksi 'neutral' pada data EmoT tetap dihitung sebagai kesalahan,
  tetapi 'neutral' tidak ikut dirata-ratakan di Macro F1.
"""
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

LABEL_UTAMA = ["anger", "fear", "joy", "love", "sad", "neutral"]
LABEL_LINTAS = ["anger", "fear", "joy", "love", "sad"]


def evaluate_macro_f1(y_true, y_pred, label_names=None):
    """Hitung Macro F1 + laporan per kelas + confusion matrix.

    Args:
        y_true: array-like label asli
        y_pred: array-like label prediksi
        label_names: list kelas yang dihitung. Kelas ini menentukan rata-rata
            Macro F1, isi laporan, dan urutan confusion matrix. Selalu isi
            secara eksplisit (LABEL_UTAMA atau LABEL_LINTAS).

    Returns:
        dict berisi macro_f1, accuracy, report (teks), report_dict,
        confusion_matrix, dan labels.
    """
    macro_f1 = f1_score(
        y_true, y_pred, average="macro", labels=label_names, zero_division=0
    )
    report = classification_report(
        y_true, y_pred, labels=label_names, digits=4, zero_division=0
    )
    report_dict = classification_report(
        y_true, y_pred, labels=label_names, digits=4, zero_division=0,
        output_dict=True,
    )
    cm = confusion_matrix(y_true, y_pred, labels=label_names)

    return {
        "macro_f1": macro_f1,
        "accuracy": accuracy_score(y_true, y_pred),
        "report": report,
        "report_dict": report_dict,
        "confusion_matrix": cm,
        "labels": list(label_names) if label_names is not None else None,
    }


def print_evaluation(result, title="Evaluasi"):
    """Cetak hasil evaluasi dengan rapi."""
    print(f"\n===== {title} =====")
    print(f"Macro F1: {result['macro_f1']:.4f}")
    print(f"Akurasi : {result['accuracy']:.4f}")
    print("\nLaporan per kelas:")
    print(result["report"])
    print("Confusion matrix:")
    print(result["confusion_matrix"])


if __name__ == "__main__":
    # Contoh pemakaian (dummy) untuk mengecek fungsi berjalan.
    y_true = ["joy", "sad", "anger", "joy", "sad", "neutral"]
    y_pred = ["joy", "sad", "joy", "joy", "anger", "neutral"]

    print_evaluation(evaluate_macro_f1(y_true, y_pred, LABEL_UTAMA), "Dummy: data utama (6 kelas)")

    # Uji lintas: label asli tanpa 'neutral'; prediksi 'neutral' tetap dihitung salah.
    y_true_x = ["joy", "sad", "anger", "joy", "sad", "love"]
    y_pred_x = ["joy", "sad", "joy", "neutral", "anger", "love"]
    print_evaluation(evaluate_macro_f1(y_true_x, y_pred_x, LABEL_LINTAS), "Dummy: uji lintas (5 kelas)")