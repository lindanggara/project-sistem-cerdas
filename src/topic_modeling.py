"""Topic Modeling untuk Analisis Media Sosial (TextScope).

Jalankan: python src/topic_modeling.py
Output : reports/results/topik_media_sosial.csv
"""
import sys
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baseline import normalisasi_teks

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RESULTS_DIR = ROOT / "reports" / "results"

def main():
    print("Memuat data (emosi_bersih.csv)...")
    # Kita pakai seluruh data bersih (7.031 baris)
    df = pd.read_csv(PROCESSED / "emosi_bersih.csv")
    df["text"] = df["text"].map(normalisasi_teks)

    print("Mengekstrak fitur TF-IDF...")
    # Kita gunakan stop_words bahasa Indonesia sederhana
    stopwords_id = ["yang", "dan", "di", "ke", "dari", "ini", "itu", "untuk", "dengan", "pada", "adalah", "juga", "atau", "tidak", "ga", "gak", "nggak", "tak", "ya", "aja", "saja", "sih", "deh", "dong", "lah", "kok", "kan", "nya", "ada", "akan", "sudah", "udah", "belum", "bisa", "dapat", "jadi", "karena", "sama", "lebih", "sangat", "banget", "yg", "dg", "dgn", "utk", "tp", "tapi", "dalam", "oleh", "saya", "aku", "kamu", "kita", "kami", "mereka", "dia", "anda", "gue", "gw", "lu", "lo", "kau", "mu", "ku", "buat", "bgt", "apa", "siapa", "bagaimana", "kenapa", "mengapa", "kalau", "kalo", "jika", "agar", "supaya", "sebagai", "para", "pun", "hanya", "masih", "telah", "sedang", "harus", "mau", "lagi", "lg", "nih", "tu", "tuh", "se", "per", "kalian", "sebuah", "semua", "setiap"]
    
    tfidf = TfidfVectorizer(
        max_features=1000, 
        ngram_range=(1, 2), 
        stop_words=stopwords_id,
        min_df=5, # Kata harus muncul minimal di 5 teks
        max_df=0.95 # Abaikan kata yang muncul di 95% teks (terlalu umum)
    )
    X = tfidf.fit_transform(df['text'])

    print("Melatih model NMF untuk 5 topik...")
    # Kita cari 5 topik utama
    nmf = NMF(n_components=5, random_state=42, init='nndsvd')
    nmf.fit(X)

    # --- MENAMPILKAN KATA KUNCI PER TOPIK ---
    feature_names = tfidf.get_feature_names_out()
    topik_data = []
    
    print("\n=== Hasil Topic Modeling (Topik yang Ramai di Media Sosial) ===")
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
        topik_name = ", ".join(top_words[:3]) # Ambil 3 kata teratas sebagai nama topik
        print(f"\nTopik #{topic_idx + 1} ({topik_name}):")
        print(", ".join(top_words))
        
        # Simpan untuk CSV
        for word in top_words:
            topik_data.append({
                "Topik_ID": topic_idx + 1,
                "Nama_Topik": topik_name,
                "Kata_Kunci": word
            })

    # Simpan hasil ke CSV agar bisa dibaca Zura untuk dashboard
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df_topik = pd.DataFrame(topik_data)
    df_topik.to_csv(RESULTS_DIR / "topik_media_sosial.csv", index=False)
    print(f"\n✅ Hasil disimpan ke {RESULTS_DIR / 'topik_media_sosial.csv'}")

    # --- MENGHUBUNGKAN TOPIK DENGAN EMOSI ---
    print("\n=== Hubungan Topik dengan Emosi Dominan ===")
    # Cari topik paling dominan untuk setiap teks
    W = nmf.transform(X)
    df['Topik_Dominan'] = W.argmax(axis=1) + 1
    
    # Hitung emosi dominan per topik
    for i in range(1, 6):
        teks_topik = df[df['Topik_Dominan'] == i]
        if len(teks_topik) > 0:
            emosi_dominan = teks_topik['label'].mode()[0]
            print(f"Topik #{i} didominasi oleh emosi: {emosi_dominan.upper()} ({len(teks_topik)} teks)")

if __name__ == "__main__":
    main()