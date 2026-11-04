"""Buat data DUMMY di reports/results/ supaya semua tab dashboard bisa dibangun
sebelum hasil asli dari Linda, Chila, dan Yuhanidz tersedia.

Jalankan dari root proyek:  python dashboard/make_dummy_results.py
Saat hasil asli sudah ada: timpa file-filenya, lalu HAPUS reports/results/DUMMY.txt.
"""
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / "reports" / "results"
LABELS = ["anger", "fear", "joy", "love", "sad", "neutral"]
TEST_SUPPORT = np.array([168, 136, 188, 113, 151, 298])  # ~15% dari emosi_bersih
EMOT_SUPPORT = np.array([1099, 642, 1009, 636, 994])      # sesuai log download_data
ACC = {"tfidf_nb": 0.62, "tfidf_logreg": 0.68, "tfidf_svm": 0.70,
       "indobert": 0.78, "indobertweet": 0.80}
SAMPLES = ["Capek banget hari ini, pengen nangis", "Makasih ya, kamu selalu ada buat aku",
           "Kesel banget sama pelayanannya", "Deg-degan nunggu pengumuman besok",
           "Akhirnya lulus juga, seneng banget!", "Hari ini rapat jam 9 di ruang A",
           "Rindu masa kecil di kampung", "Jangan sampai kejadian itu terulang lagi",
           "Aku takut sendirian di rumah", "Cuaca hari ini cerah"]

rng = np.random.default_rng(42)


def make_cm(support, acc, n_cols):
    cm = np.zeros((len(support), n_cols), dtype=int)
    for i, s in enumerate(support):
        w = rng.random(n_cols) + 0.2
        w[i] = 0
        w = w / w.sum() * (1 - acc)
        w[i] = acc
        cm[i] = rng.multinomial(s, w / w.sum())
    return cm


def per_class(cm):
    tp = np.diag(cm).astype(float)
    p = tp / np.maximum(cm.sum(axis=0), 1)
    r = tp / np.maximum(cm.sum(axis=1), 1)
    f1 = 2 * p * r / np.maximum(p + r, 1e-9)
    return pd.DataFrame({"label": LABELS, "precision": p.round(3), "recall": r.round(3),
                         "f1": f1.round(3), "support": cm.sum(axis=1)})


OUT.mkdir(parents=True, exist_ok=True)
rows, errors = [], []
for model, acc in ACC.items():
    cm = make_cm(TEST_SUPPORT, acc, 6)
    pc = per_class(cm)
    f1_test = pc["f1"].mean()
    # EmoT: 5 baris (aktual) x 6 kolom (prediksi), karena model masih bisa menebak "neutral"
    cd = make_cm(EMOT_SUPPORT, acc - 0.18, 6)
    cd_f1 = per_class(np.vstack([cd, np.zeros((1, 6), dtype=int)]))["f1"][:5].mean()
    rows.append({"model": model, "macro_f1_valid": round(f1_test + rng.normal(0, .01), 3),
                 "macro_f1_test": round(f1_test, 3), "macro_f1_emot": round(cd_f1, 3)})
    pd.DataFrame(cm, index=LABELS, columns=LABELS).to_csv(OUT / f"confusion_{model}.csv")
    pd.DataFrame(cd, index=LABELS[:5], columns=LABELS).to_csv(OUT / f"cross_domain_{model}.csv")
    pc.to_csv(OUT / f"per_class_{model}.csv", index=False)
    for _ in range(15):
        t, p = rng.choice(6, 2, replace=False)
        errors.append({"text": rng.choice(SAMPLES), "true_label": LABELS[t],
                       "pred_label": LABELS[p], "model": model})

pd.DataFrame(rows).to_csv(OUT / "model_comparison.csv", index=False)
pd.DataFrame(errors).to_csv(OUT / "error_examples.csv", index=False)
(OUT / "DUMMY.txt").write_text("Data dummy. Hapus file ini setelah hasil asli dipasang.\n")
print(f"Selesai: {len(list(OUT.glob('*.csv')))} file CSV dummy di {OUT}")
