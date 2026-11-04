"""TextScope: dashboard klasifikasi emosi Bahasa Indonesia.

Jalankan dari root proyek:  streamlit run dashboard/app.py
Dashboard hanya MENAMPILKAN hasil. Angka evaluasi dibaca dari reports/results/,
model dipanggil lewat predict_proba() di bawah.
"""
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "reports" / "results"
DATA = ROOT / "data" / "processed"

LABELS = ["anger", "fear", "joy", "love", "sad", "neutral"]
COLORS = {"anger": "#C8453B", "fear": "#6B4FA0", "joy": "#E4A81C",
          "love": "#D9608C", "sad": "#3C78B4", "neutral": "#8A929B"}
IS_DUMMY = (RESULTS / "DUMMY.txt").exists()

EXAMPLES = {
    "Senang": "Akhirnya lulus juga, seneng banget hari ini!",
    "Takut": "Aku takut banget sendirian di rumah malam-malam.",
    "Marah": "Kesel banget sama pelayanannya, benar-benar bikin emosi.",
    "Netral": "Rapat besok dimulai jam sembilan di ruang A.",
}
STOP = set("yang dan di ke dari ini itu aku kamu saya dengan untuk nya tidak ga gak ya yg "
           "sih aja juga udah ada kalo kalau bisa mau jadi pas lagi sama banget lebih".split())

st.set_page_config(page_title="TextScope", page_icon="🔍", layout="wide")


# ---------- Pemuatan data ----------
@st.cache_data
def read_csv(path: str, index_col=None):
    p = Path(path)
    return pd.read_csv(p, index_col=index_col) if p.exists() else None


def missing(name: str):
    st.info(f"Berkas `{name}` belum ada di `reports/results/`. "
            "Jalankan `python dashboard/make_dummy_results.py` untuk data contoh, "
            "atau tunggu hasil dari tim.")


# ---------- Model ----------
KEYWORDS = {"anger": ["marah", "benci", "kesal", "kesel", "emosi"],
            "fear": ["takut", "cemas", "khawatir", "ngeri"],
            "joy": ["senang", "seneng", "bahagia", "gembira", "seru"],
            "love": ["cinta", "sayang", "rindu", "suka"],
            "sad": ["sedih", "nangis", "kecewa", "galau"]}


def predict_proba(text: str, model_name: str) -> dict:
    """MOCK berbasis kata kunci. Ganti isi fungsi ini dengan model asli
    (kembalikan dict label -> probabilitas, urutan LABELS)."""
    t = text.lower()
    s = np.full(len(LABELS), 0.05)
    for i, lab in enumerate(LABELS[:-1]):
        s[i] += sum(0.5 for k in KEYWORDS[lab] if k in t)
    s[-1] += 0.3
    return dict(zip(LABELS, s / s.sum()))


# ---------- Komponen grafik ----------
def heatmap(cm: pd.DataFrame, normalize: bool):
    z = cm.div(cm.sum(axis=1), axis=0) if normalize else cm
    fig = px.imshow(z, text_auto=".0%" if normalize else "d", aspect="auto",
                    color_continuous_scale="Blues",
                    labels=dict(x="Prediksi model", y="Label sebenarnya"))
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0), height=420)
    return fig


def top_confusions(cm: pd.DataFrame, n: int = 6) -> pd.DataFrame:
    rows = [{"pasangan": f"{t} → {p}", "jumlah": int(cm.loc[t, p])}
            for t in cm.index for p in cm.columns if t != p]
    return pd.DataFrame(rows).nlargest(n, "jumlah")


# ---------- Sidebar ----------
comp = read_csv(str(RESULTS / "model_comparison.csv"))
models = comp["model"].tolist() if comp is not None else ["mock"]

with st.sidebar:
    st.header("TextScope")
    model = st.selectbox("Model aktif", models)
    st.caption("Klasifikasi emosi teks Bahasa Indonesia: anger, fear, joy, love, sad, neutral.")
    with st.expander("Tentang proyek"):
        st.markdown(
            "- **Data utama:** Emotion Dataset from Indonesian Public Opinion (6 kelas)\n"
            "- **Uji lintas domain:** EmoT IndoNLU (5 kelas)\n"
            "- **Metrik utama:** Macro F1\n"
            "- **Tim:** Yuhanidz, Linda, Chila, Zura\n\n"
            "Mata kuliah Sistem Cerdas, 2026.")
    if IS_DUMMY:
        st.warning("Angka evaluasi masih **data contoh**, bukan hasil model asli.")

st.title("TextScope")
st.write("Tebak emosi dari teks, lalu lihat seberapa andal modelnya.")

tab_pred, tab_eval, tab_cross, tab_err, tab_data = st.tabs(
    ["Prediksi", "Evaluasi model", "Lintas domain", "Analisis error", "Data"])

# ---------- 1. Prediksi ----------
with tab_pred:
    st.session_state.setdefault("input_text", "")
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.text_area("Teks yang ingin dianalisis", key="input_text", height=140,
                     placeholder="Tempel komentar atau kalimat di sini")
        st.caption("Coba contoh:")
        cols = st.columns(len(EXAMPLES))
        for col, (name, txt) in zip(cols, EXAMPLES.items()):
            col.button(name, key=f"ex_{name}", width="stretch",
                       on_click=lambda t=txt: st.session_state.update(input_text=t))
    with right:
        text = st.session_state.input_text.strip()
        if not text:
            st.write("Hasil prediksi akan muncul di sini setelah kamu mengisi teks.")
        else:
            probs = predict_proba(text, model)
            top = max(probs, key=probs.get)
            st.metric("Emosi terdeteksi", top, f"{probs[top]:.0%} yakin", delta_color="off")
            df = pd.DataFrame({"emosi": LABELS, "probabilitas": [probs[l] for l in LABELS]})
            fig = px.bar(df, x="probabilitas", y="emosi", orientation="h", color="emosi",
                         color_discrete_map=COLORS, category_orders={"emosi": LABELS[::-1]})
            fig.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=10, b=0),
                              xaxis_tickformat=".0%", xaxis_range=[0, 1])
            st.plotly_chart(fig, width="stretch")

# ---------- 2. Evaluasi model ----------
with tab_eval:
    if comp is None:
        missing("model_comparison.csv")
    else:
        st.subheader("Perbandingan model (Macro F1)")
        long = comp.melt(id_vars="model", value_vars=["macro_f1_valid", "macro_f1_test"],
                         var_name="data", value_name="macro_f1")
        long["data"] = long["data"].map({"macro_f1_valid": "validasi", "macro_f1_test": "uji"})
        fig = px.bar(long, x="model", y="macro_f1", color="data", barmode="group",
                     color_discrete_sequence=["#9DB4D6", "#2F4B8F"])
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), yaxis_range=[0, 1])
        st.plotly_chart(fig, width="stretch")
        best = comp.loc[comp["macro_f1_test"].idxmax()]
        st.caption(f"Skor uji tertinggi: **{best['model']}** ({best['macro_f1_test']:.3f}).")

        st.subheader(f"Detail model: {model}")
        c1, c2 = st.columns([1, 1.2], gap="large")
        pc = read_csv(str(RESULTS / f"per_class_{model}.csv"))
        cm = read_csv(str(RESULTS / f"confusion_{model}.csv"), index_col=0)
        with c1:
            st.write("Skor per kelas")
            if pc is None:
                missing(f"per_class_{model}.csv")
            else:
                st.dataframe(pc, hide_index=True, width="stretch")
        with c2:
            norm = st.toggle("Tampilkan persentase per baris", value=True, key="norm_eval")
            if cm is None:
                missing(f"confusion_{model}.csv")
            else:
                st.plotly_chart(heatmap(cm, norm), width="stretch")

# ---------- 3. Lintas domain ----------
with tab_cross:
    st.subheader("Uji lintas domain: EmoT (IndoNLU)")
    st.write("Model dilatih di dataset utama, lalu diuji pada EmoT yang gaya bahasanya berbeda. "
             "Hasil ini dilaporkan terpisah dari evaluasi utama. EmoT tidak punya kelas "
             "*neutral*, jadi kolom neutral hanya muncul sebagai tebakan model.")
    if comp is not None and "macro_f1_emot" in comp:
        fig = px.bar(comp, x="model", y=["macro_f1_test", "macro_f1_emot"], barmode="group",
                     color_discrete_sequence=["#2F4B8F", "#E4A81C"])
        fig.for_each_trace(lambda t: t.update(
            name={"macro_f1_test": "data uji utama", "macro_f1_emot": "EmoT"}[t.name]))
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0),
                          yaxis_title="Macro F1", yaxis_range=[0, 1], legend_title_text="")
        st.plotly_chart(fig, width="stretch")
    cd = read_csv(str(RESULTS / f"cross_domain_{model}.csv"), index_col=0)
    if cd is None:
        missing(f"cross_domain_{model}.csv")
    else:
        st.write(f"Confusion matrix EmoT untuk **{model}**")
        norm = st.toggle("Tampilkan persentase per baris", value=True, key="norm_cross")
        st.plotly_chart(heatmap(cd, norm), width="stretch")

# ---------- 4. Analisis error ----------
with tab_err:
    st.subheader("Emosi yang sering tertukar")
    cm = read_csv(str(RESULTS / f"confusion_{model}.csv"), index_col=0)
    if cm is None:
        missing(f"confusion_{model}.csv")
    else:
        tc = top_confusions(cm)
        fig = px.bar(tc, x="jumlah", y="pasangan", orientation="h",
                     color_discrete_sequence=["#2F4B8F"])
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0),
                          yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, width="stretch")
        st.caption("Format: label sebenarnya → tebakan model.")

    st.subheader("Contoh teks yang salah ditebak")
    err = read_csv(str(RESULTS / "error_examples.csv"))
    if err is None:
        missing("error_examples.csv")
    else:
        f1, f2 = st.columns(2)
        true_f = f1.multiselect("Label sebenarnya", LABELS)
        pred_f = f2.multiselect("Tebakan model", LABELS)
        view = err[err["model"] == model] if "model" in err else err
        if true_f:
            view = view[view["true_label"].isin(true_f)]
        if pred_f:
            view = view[view["pred_label"].isin(pred_f)]
        st.dataframe(view.drop(columns="model", errors="ignore"), hide_index=True, width="stretch")

# ---------- 5. Data ----------
with tab_data:
    df = read_csv(str(DATA / "emosi_bersih.csv"))
    if df is None:
        st.info("Berkas `data/processed/emosi_bersih.csv` belum ada. "
                "Jalankan `python src/download_data.py`.")
    else:
        # Nama kolom disesuaikan otomatis; cek isi emosi_bersih.csv jika tampilan aneh.
        lab_col = "label" if "label" in df.columns else df.columns[-1]
        txt_col = next((c for c in ("text", "teks", "tweet", "kalimat") if c in df.columns),
                       next(c for c in df.columns if c != lab_col))
        st.subheader("Sebaran label")
        counts = df[lab_col].value_counts().reindex(LABELS).dropna().reset_index()
        counts.columns = ["emosi", "jumlah"]
        fig = px.bar(counts, x="emosi", y="jumlah", color="emosi", color_discrete_map=COLORS)
        fig.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")

        st.subheader("Panjang teks per kelas (jumlah kata)")
        tmp = df.assign(kata=df[txt_col].astype(str).str.split().str.len())
        fig = px.box(tmp, x=lab_col, y="kata", color=lab_col, color_discrete_map=COLORS,
                     category_orders={lab_col: LABELS})
        fig.update_layout(showlegend=False, height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, width="stretch")

        st.subheader("Kata paling sering per kelas")
        pick = st.selectbox("Kelas", LABELS, key="word_pick")
        words = Counter(w for t in df.loc[df[lab_col] == pick, txt_col].astype(str)
                        for w in t.lower().split() if w not in STOP and len(w) > 2)
        wd = pd.DataFrame(words.most_common(15), columns=["kata", "frekuensi"])
        fig = px.bar(wd, x="frekuensi", y="kata", orientation="h",
                     color_discrete_sequence=[COLORS[pick]])
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=0),
                          yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, width="stretch")

        with st.expander("Contoh data"):
            st.dataframe(df.sample(min(20, len(df)), random_state=1), hide_index=True,
                         width="stretch")
