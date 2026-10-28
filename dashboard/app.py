import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

LABELS = ["anger", "fear", "joy", "love", "sad", "neutral"]

# --- MOCK: ganti fungsi ini dengan model asli nanti ---
KEYWORDS = {
    "anger": ["marah", "benci", "kesal", "bangsat"],
    "fear": ["takut", "cemas", "khawatir", "ngeri"],
    "joy": ["senang", "bahagia", "gembira", "seru"],
    "love": ["cinta", "sayang", "rindu", "suka"],
    "sad": ["sedih", "nangis", "kecewa", "galau"],
}

def predict_emotion(text: str) -> dict:
    t = text.lower()
    scores = np.full(len(LABELS), 0.05)
    for i, lab in enumerate(LABELS[:-1]):
        scores[i] += sum(0.5 for k in KEYWORDS[lab] if k in t)
    scores[-1] += 0.3  # neutral sebagai default
    probs = scores / scores.sum()
    return dict(zip(LABELS, probs))
# ------------------------------------------------------

st.set_page_config(page_title="TextScope", page_icon="🔍", layout="wide")
st.title("🔍 TextScope: Klasifikasi Emosi Bahasa Indonesia")
st.caption("Mode demo: prediksi masih tiruan (mock), model asli belum dipasang.")

tab1, tab2 = st.tabs(["Prediksi", "Evaluasi Model"])

with tab1:
    text = st.text_area("Masukkan teks:", height=120,
                        placeholder="Contoh: Aku sangat senang hari ini!")
    if st.button("Prediksi", type="primary") and text.strip():
        probs = predict_emotion(text)
        top = max(probs, key=probs.get)
        st.subheader(f"Emosi terdeteksi: **{top}** ({probs[top]:.0%})")
        df = pd.DataFrame({"emosi": list(probs), "probabilitas": list(probs.values())})
        st.plotly_chart(px.bar(df, x="emosi", y="probabilitas"), use_container_width=True)

with tab2:
    st.info("Placeholder: confusion matrix, distribusi label, dan Macro F1 "
            "akan ditampilkan di sini setelah model dan hasil evaluasi tersedia.")