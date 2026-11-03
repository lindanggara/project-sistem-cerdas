"""Finalisasi: Simpan model terbaik dan buat grafik untuk laporan.

Jalankan: python src/finalisasi_model.py
Output : 
  - models/logreg_tuned.pkl
  - reports/figures/confusion_matrix_logreg.png
  - reports/figures/perbandingan_model_klasik.png
"""
import sys
from pathlib import Path
import joblib
import pandas as pd

# --- PERBAIKAN: Gunakan backend Agg agar tidak butuh tkinter ---
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Tambahkan path ke src
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseline import normalisasi_teks
from evaluate import evaluate_macro_f1, LABEL_UTAMA

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"
FIGURES_DIR = ROOT / "reports" / "figures"

# Pastikan folder ada
MODELS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def load_data(nama):
    df = pd.read_csv(PROCESSED / f"{nama}.csv")
    df["text"] = df["text"].map(normalisasi_teks)
    return df

def main():
    print("Memuat data...")
    train = load_data("train")
    test = load_data("test")

    print("Melatih ulang model LogReg Tuned (terbaik)...")
    model = Pipeline([
        ("fitur", FeatureUnion([
            ("kata", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ("karakter", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=5000))
        ])),
        ("clf", LogisticRegression(max_iter=2000, random_state=42, class_weight="balanced", C=1.0))
    ])
    model.fit(train["text"], train["label"])

    # --- 1. SIMPAN MODEL ---
    print("Menyimpan model ke models/logreg_tuned.pkl...")
    joblib.dump(model, MODELS_DIR / "logreg_tuned.pkl")
    print("✅ Model tersimpan!")

    # --- 2. BUAT GRAFIK CONFUSION MATRIX ---
    print("Membuat grafik confusion matrix...")
    pred_test = model.predict(test["text"])
    
    # Urutkan label sesuai LABEL_UTAMA
    cm = confusion_matrix(test["label"], pred_test, labels=LABEL_UTAMA)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABEL_UTAMA)
    disp.plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)
    plt.title("Confusion Matrix - LogReg Tuned (Test Set)", fontsize=14, pad=20)
    plt.xlabel("Prediksi", fontsize=12)
    plt.ylabel("Label Asli", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "confusion_matrix_logreg.png", dpi=300)
    plt.close()
    print("✅ Grafik confusion matrix tersimpan!")

    # --- 3. BUAT GRAFIK PERBANDINGAN MODEL ---
    print("Membuat grafik perbandingan model...")
    # Data manual (dari eksperimen.md)
    data_perbandingan = {
        "Model": ["LogReg Baseline", "LogReg + Norm & CW", "SVM Tuned", "Naive Bayes", "LogReg Tuned"],
        "Macro F1": [0.7108, 0.7155, 0.7251, 0.5628, 0.7286]
    }
    df_banding = pd.DataFrame(data_perbandingan)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#a0c4ff", "#9bf6ff", "#caffbf", "#ffc6ff", "#fdffb6"]
    bars = ax.barh(df_banding["Model"], df_banding["Macro F1"], color=colors, edgecolor='grey')
    
    # Tambahkan teks skor di ujung bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.005, bar.get_y() + bar.get_height()/2, 
                f'{width:.4f}', 
                ha='left', va='center', fontweight='bold', fontsize=10)
        
    ax.set_xlim(0, 0.8)
    ax.set_xlabel("Macro F1 Score", fontsize=12)
    ax.set_title("Perbandingan Performa Model Klasik (Test Set)", fontsize=14, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "perbandingan_model_klasik.png", dpi=300)
    plt.close()
    print("✅ Grafik perbandingan model tersimpan!")

if __name__ == "__main__":
    main()