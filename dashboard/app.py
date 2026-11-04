"""TextScope: dashboard klasifikasi emosi Bahasa Indonesia.

Jalankan dari root proyek:  streamlit run dashboard/app.py
Dashboard hanya MENAMPILKAN hasil. Angka evaluasi dibaca dari reports/results/,
model dipanggil lewat predict_proba() di bawah.
"""
from collections import Counter
from html import escape
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "reports" / "results"
DATA = ROOT / "data" / "processed"

LABELS = ["anger", "fear", "joy", "love", "sad", "neutral"]
# Warna emosi sudah lolos validator (jarak antar-warna aman untuk buta warna).
# Satu emosi = satu warna di semua grafik. Ubah hanya setelah validasi ulang.
COLORS = {"anger": "#E34948", "fear": "#6250D6", "joy": "#EDA100",
          "love": "#E87BA4", "sad": "#2A78D6", "neutral": "#1BAF7A"}
ID_NAME = {"anger": "marah", "fear": "takut", "joy": "senang",
           "love": "cinta", "sad": "sedih", "neutral": "netral"}

# Warna tema (cokelat hangat, krem, dan emas)
INK, MUTED = "#3B2418", "#7A5A48"
B900, B700, B400, B200, B50 = "#3E2218", "#8B4F2B", "#D9A47E", "#EBD3BF", "#FBF3EA"
YEL, CHART_YEL, GRID = "#F2C078", "#D9A47E", "#EFE0D2"
FONT = "Bricolage Grotesque, system-ui, -apple-system, Segoe UI, sans-serif"

# Ubah ke False setelah predict_proba() memakai model asli.
USING_MOCK = True
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

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&display=swap');
.stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-icons) { font-family: __FONT__; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1240px; }
header[data-testid="stHeader"] { background: transparent; }
button[data-baseweb="tab"] p { font-size: 1.02rem; font-weight: 620; }
div[data-baseweb="tab-highlight"] { background-color: __YEL__ !important; height: 4px !important; border-radius: 4px; }
.hero { position: relative; overflow: hidden; display: flex; justify-content: space-between; align-items: flex-end;
  gap: 16px; flex-wrap: wrap; background: __B900__; border-radius: 22px; padding: 26px 32px 26px 40px; margin-bottom: 18px; }
.hero::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 8px; background: __YEL__; }
.hero-title { color: #fff; font-size: 2.6rem; font-weight: 750; letter-spacing: -0.025em; line-height: 1.05; }
.hero-sub { color: #EAD3BF; font-size: 1.05rem; margin-top: 6px; max-width: 48ch; }
.hero-pill { background: __YEL__; color: __B900__; font-weight: 650; font-size: .9rem; padding: 7px 14px; border-radius: 999px; }
.intro { color: __MUTED__; font-size: 1.02rem; line-height: 1.5; margin: 4px 0 16px; max-width: 80ch; }
.card-title { font-size: 1.14rem; font-weight: 680; color: __INK__; margin: 0 0 2px; }
.card-sub { font-size: .92rem; color: __MUTED__; margin: 0 0 8px; }
[class*="st-key-card_"] { background: #fff; border: 1px solid #EBD9C8; border-radius: 16px; padding: 18px 20px 18px; }
.kpi { background: #fff; border: 1px solid #EBD9C8; border-radius: 14px; padding: 14px 18px; min-height: 142px; margin-bottom: 1.1rem; }
.kpi-label { font-size: .88rem; color: __MUTED__; font-weight: 560; }
.kpi-value { font-size: 1.9rem; font-weight: 720; color: __B900__; letter-spacing: -0.02em; line-height: 1.2; margin: 3px 0; overflow-wrap: break-word; }
.kpi-value.kpi-long { font-size: 1.5rem; padding: 4px 0 3px; }
.kpi-value.kpi-xlong { font-size: 1.2rem; padding: 7px 0 5px; }
.kpi-note { font-size: .85rem; color: __MUTED__; }
.kpi-hi { background: __YEL__; border-color: __YEL__; }
.kpi-hi .kpi-label, .kpi-hi .kpi-note { color: #5A3A1A; }
.result { background: __B900__; color: #fff; border-radius: 20px; padding: 22px 26px; }
.result-label { color: #E9CDB5; font-size: .95rem; font-weight: 560; }
.result-emotion { display: flex; align-items: center; flex-wrap: wrap; gap: 12px; margin: 6px 0 2px; }
.result-word { font-size: 3.1rem; font-weight: 760; letter-spacing: -0.03em; line-height: 1.05; }
.result-gloss { color: #E9CDB5; font-size: 1.1rem; }
.dot { width: 14px; height: 14px; border-radius: 50%; display: inline-block; flex: none; box-shadow: 0 0 0 2px #fff; }
.conf { margin: 14px 0 4px; display: flex; align-items: center; gap: 12px; }
.conf-track { flex: 1; height: 10px; border-radius: 999px; background: rgba(255,255,255,.18); overflow: hidden; }
.conf-fill { height: 100%; background: __YEL__; border-radius: 999px; }
.conf-text { font-weight: 650; white-space: nowrap; }
.result-expl { color: #F6E8DA; font-size: 1.03rem; line-height: 1.5; margin: 12px 0 14px; }
.top3 { border-top: 1px solid rgba(255,255,255,.16); padding-top: 12px; display: grid; gap: 8px; }
.top3-row { display: flex; align-items: center; gap: 10px; font-size: .98rem; }
.top3-name { flex: 1; }
.top3-pct { font-weight: 650; }
.result-empty { background: #fff; border: 1.5px dashed __B200__; border-radius: 20px; padding: 34px 28px; color: __MUTED__; font-size: 1.05rem; line-height: 1.5; }
.result-empty b { color: __B900__; }
.howto { margin: 6px 0 0; padding-left: 1.1rem; color: __INK__; font-size: .97rem; line-height: 1.55; }
.howto li { margin-bottom: 7px; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 1.55rem; font-weight: 740; letter-spacing: -0.02em; color: #fff; margin: 4px 0 14px; }
.brand-mark { width: 14px; height: 14px; border-radius: 50%; background: __YEL__; }
.side-note { color: #E9CDB5; font-size: .9rem; line-height: 1.45; margin: 12px 0; }
"""
for _k, _v in {"__FONT__": FONT, "__YEL__": YEL, "__B900__": B900, "__B200__": B200,
               "__MUTED__": MUTED, "__INK__": INK}.items():
    CSS = CSS.replace(_k, _v)
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


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


def level(p: float) -> str:
    return "tinggi" if p >= 0.7 else "sedang" if p >= 0.45 else "rendah"


def explain(probs: dict) -> str:
    """Kalimat penjelasan hasil prediksi dalam bahasa sehari-hari."""
    (l1, p1), (l2, p2) = sorted(probs.items(), key=lambda kv: -kv[1])[:2]
    a, b, gap = ID_NAME[l1], ID_NAME[l2], (p1 - p2) * 100
    if gap < 10:
        return (f"Model ragu-ragu: {a} ({p1:.0%}) dan {b} ({p2:.0%}) nyaris sama kuat. "
                "Anggap ini sebagai petunjuk, bukan kepastian.")
    if p1 >= 0.6:
        return (f"Model cukup yakin: teks ini paling mirip emosi {a} ({p1:.0%}). "
                f"Emosi terdekat berikutnya, {b}, hanya {p2:.0%}.")
    return (f"Model condong ke {a} ({p1:.0%}), tetapi {b} ({p2:.0%}) juga cukup mungkin. "
            f"Selisihnya {gap:.0f} poin persentase.")


# ---------- Komponen tampilan ----------
def fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", ".")


def intro(text: str):
    st.markdown(f'<p class="intro">{escape(text)}</p>', unsafe_allow_html=True)


def card(key: str):
    return st.container(key=f"card_{key}")


def card_title(title: str, sub: str = ""):
    sub_html = f'<p class="card-sub">{escape(sub)}</p>' if sub else ""
    st.markdown(f'<div class="card-title">{escape(title)}</div>{sub_html}', unsafe_allow_html=True)


def kpi(label: str, value: str, note: str = "", hi: bool = False):
    cls = "kpi kpi-hi" if hi else "kpi"
    size = "kpi-xlong" if len(str(value)) > 16 else "kpi-long" if len(str(value)) > 9 else ""
    st.markdown(f'<div class="{cls}"><div class="kpi-label">{escape(label)}</div>'
                f'<div class="kpi-value {size}">{escape(str(value))}</div>'
                f'<div class="kpi-note">{escape(note)}</div></div>', unsafe_allow_html=True)


# ---------- Komponen grafik ----------
SCALE = [[0.0, "#FBF3EA"], [0.45, "#E3B792"], [1.0, B900]]


def style_fig(fig, height=320, grid="y", legend=False):
    """Gaya seragam untuk semua grafik: font, margin, grid tipis, hover."""
    fig.update_layout(
        height=height, margin=dict(l=6, r=6, t=10, b=6), showlegend=legend,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=14, color=INK), bargap=0.38, bargroupgap=0.06,
        hoverlabel=dict(bgcolor=B900, font=dict(family=FONT, size=14, color="#fff")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""))
    for axis, name in ((fig.update_xaxes, "x"), (fig.update_yaxes, "y")):
        axis(showgrid=(grid == name), gridcolor=GRID, zeroline=False, linecolor=GRID,
             ticks="", tickfont=dict(size=13), title_font=dict(size=13, color=MUTED))
    return fig


def round_bars(fig, radius=5):
    try:
        fig.update_traces(marker_cornerradius=radius, selector=dict(type="bar"))
    except ValueError:  # versi Plotly lama tidak mendukung sudut membulat
        pass
    return fig


def heatmap(cm: pd.DataFrame, normalize: bool):
    z = cm.div(cm.sum(axis=1), axis=0) if normalize else cm
    fig = px.imshow(z, text_auto=".0%" if normalize else "d", aspect="auto",
                    color_continuous_scale=SCALE,
                    labels=dict(x="Tebakan model", y="Label sebenarnya"))
    fig.update_traces(xgap=3, ygap=3, textfont=dict(size=14))
    fig.update_layout(coloraxis_showscale=False)
    return style_fig(fig, 430, grid="none")


def top_confusions(cm: pd.DataFrame, n: int = 6) -> pd.DataFrame:
    rows = [{"pasangan": f"{t} → {p}", "jumlah": int(cm.loc[t, p])}
            for t in cm.index for p in cm.columns if t != p]
    return pd.DataFrame(rows).nlargest(n, "jumlah")


# ---------- Sidebar ----------
comp = read_csv(str(RESULTS / "model_comparison.csv"))
models = comp["model"].tolist() if comp is not None else ["mock"]

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark"></span>TextScope</div>',
                unsafe_allow_html=True)
    model = st.selectbox("Model aktif", models)
    st.markdown('<p class="side-note">Klasifikasi emosi teks Bahasa Indonesia ke dalam enam '
                'kelas: anger, fear, joy, love, sad, dan neutral.</p>', unsafe_allow_html=True)
    with st.expander("Tentang proyek"):
        st.markdown(
            "- **Data utama:** Emotion Dataset from Indonesian Public Opinion (6 kelas)\n"
            "- **Uji lintas domain:** EmoT IndoNLU (5 kelas)\n"
            "- **Metrik utama:** Macro F1\n"
            "- **Tim:** Yuhanidz, Linda, Chila, Zura\n\n"
            "Mata kuliah Sistem Cerdas, 2026.")

pill = '<div class="hero-pill">Angka evaluasi masih data contoh</div>' if IS_DUMMY else ""
st.markdown('<div class="hero"><div><div class="hero-title">TextScope</div>'
            '<div class="hero-sub">Tebak emosi dari teks Bahasa Indonesia, lalu lihat '
            f'seberapa andal modelnya.</div></div>{pill}</div>', unsafe_allow_html=True)

tab_pred, tab_eval, tab_cross, tab_err, tab_data = st.tabs(
    ["Prediksi", "Evaluasi model", "Lintas domain", "Analisis error", "Data"])

# ---------- 1. Prediksi ----------
with tab_pred:
    intro("Ketik atau tempel satu kalimat. Model menebak emosinya dan menunjukkan seberapa yakin ia.")
    st.session_state.setdefault("input_text", "")
    left, right = st.columns([5, 6], gap="large")
    with left:
        with card("input"):
            card_title("Teks yang dianalisis", "Satu kalimat atau satu komentar sudah cukup.")
            st.text_area("Teks yang dianalisis", key="input_text", height=150,
                         label_visibility="collapsed",
                         placeholder="Tempel komentar atau kalimat di sini")
            st.caption("Atau pilih salah satu contoh:")
            cols = st.columns(len(EXAMPLES))
            for col, (name, txt) in zip(cols, EXAMPLES.items()):
                col.button(name, key=f"ex_{name}", width="stretch",
                           on_click=lambda t=txt: st.session_state.update(input_text=t))

    text = st.session_state.input_text.strip()
    probs = predict_proba(text, model) if text else None
    ranked = sorted(probs.items(), key=lambda kv: -kv[1]) if probs else []

    with right:
        if not probs:
            st.markdown('<div class="result-empty"><b>Belum ada teks.</b><br>Ketik kalimat di '
                        'sebelah kiri, atau klik salah satu contoh untuk melihat bagaimana '
                        'model menebak emosinya.</div>', unsafe_allow_html=True)
        else:
            top, p1 = ranked[0]
            rows = "".join(
                f'<div class="top3-row"><span class="dot" style="background:{COLORS[l]}"></span>'
                f'<span class="top3-name">{l} ({ID_NAME[l]})</span>'
                f'<span class="top3-pct">{p:.0%}</span></div>' for l, p in ranked[:3])
            st.markdown(
                '<div class="result"><div class="result-label">Emosi terdeteksi</div>'
                f'<div class="result-emotion"><span class="dot" style="background:{COLORS[top]}"></span>'
                f'<span class="result-word">{top}</span><span class="result-gloss">{ID_NAME[top]}</span></div>'
                f'<div class="conf"><div class="conf-track"><div class="conf-fill" style="width:{p1 * 100:.0f}%"></div></div>'
                f'<span class="conf-text">Keyakinan {p1:.0%} ({level(p1)})</span></div>'
                f'<div class="result-expl">{escape(explain(probs))}</div>'
                f'<div class="top3">{rows}</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([6, 5], gap="large")
    with c1:
        with card("chart"):
            card_title("Peluang tiap emosi", "Keenam batang dijumlahkan menjadi 100%.")
            if not probs:
                st.caption("Grafik muncul setelah ada teks.")
            else:
                df = pd.DataFrame({"emosi": [l for l, _ in ranked],
                                   "probabilitas": [p for _, p in ranked]})
                fig = px.bar(df, x="probabilitas", y="emosi", orientation="h", color="emosi",
                             color_discrete_map=COLORS, text="probabilitas",
                             category_orders={"emosi": df["emosi"].tolist()[::-1]})
                fig.update_traces(texttemplate="%{x:.0%}", textposition="outside",
                                  cliponaxis=False, textfont=dict(color=INK, size=14))
                fig.update_xaxes(tickformat=".0%", range=[0, 1.08], title_text=None)
                fig.update_yaxes(title_text=None)
                st.plotly_chart(round_bars(style_fig(fig, 320, grid="x")), width="stretch")
    with c2:
        with card("howto"):
            card_title("Cara membaca hasil ini")
            mock_note = ("<li>Saat ini prediksi memakai model tiruan berbasis kata kunci, jadi "
                         "hasilnya belum mewakili model asli.</li>") if USING_MOCK else ""
            st.markdown(
                '<ul class="howto">'
                '<li>Setiap batang adalah peluang emosi itu menurut model. Totalnya 100%.</li>'
                '<li>Angka keyakinan adalah peluang tertinggi untuk teks ini, bukan akurasi model. '
                'Akurasi model ada di tab Evaluasi model.</li>'
                '<li>Keyakinan tinggi mulai 70%, sedang 45 sampai 69%, rendah di bawah 45%. '
                'Dengan enam emosi, tebakan asal hanya benar sekitar 17%.</li>'
                '<li>Kalimat sangat pendek, sindiran, atau campuran beberapa emosi lebih sulit '
                f'ditebak.</li>{mock_note}</ul>', unsafe_allow_html=True)

# ---------- 2. Evaluasi model ----------
with tab_eval:
    intro("Model mana yang paling andal? Semua model dinilai dengan cara yang sama, memakai "
          "Macro F1 pada data uji yang tidak pernah dilihat model saat belajar.")
    if comp is None:
        missing("model_comparison.csv")
    else:
        best = comp.loc[comp["macro_f1_test"].idxmax()]
        worst = comp.loc[comp["macro_f1_test"].idxmin()]
        k = st.columns(4, gap="medium")
        with k[0]:
            kpi("Model terbaik", best["model"], "Macro F1 data uji tertinggi", hi=True)
        with k[1]:
            kpi("Macro F1 terbaik", f"{best['macro_f1_test']:.3f}", "pada data uji")
        with k[2]:
            kpi("Model dibandingkan", str(len(comp)), "dengan pembagian data yang sama")
        with k[3]:
            gain = best["macro_f1_test"] - worst["macro_f1_test"]
            kpi("Rentang skor", f"+{gain:.3f}", f"selisih dengan {worst['model']}")

        with card("compare"):
            card_title("Perbandingan Macro F1", "Makin tinggi makin baik. Maksimalnya 1.")
            long = comp.melt(id_vars="model", value_vars=["macro_f1_valid", "macro_f1_test"],
                             var_name="data", value_name="macro_f1")
            long["data"] = long["data"].map({"macro_f1_valid": "validasi", "macro_f1_test": "uji"})
            fig = px.bar(long, x="model", y="macro_f1", color="data", barmode="group",
                         text="macro_f1", color_discrete_map={"validasi": B400, "uji": B700},
                         category_orders={"data": ["validasi", "uji"]})
            fig.update_traces(texttemplate="%{y:.2f}", textposition="outside",
                              cliponaxis=False, textfont=dict(color=INK, size=13))
            fig.update_yaxes(range=[0, 1.05], title_text="Macro F1")
            fig.update_xaxes(title_text=None)
            st.plotly_chart(round_bars(style_fig(fig, 340, legend=True)), width="stretch")
            with st.expander("Lihat sebagai tabel"):
                st.dataframe(comp.round(3), hide_index=True, width="stretch")

        pc = read_csv(str(RESULTS / f"per_class_{model}.csv"))
        cm = read_csv(str(RESULTS / f"confusion_{model}.csv"), index_col=0)
        c1, c2 = st.columns([1.1, 1], gap="large")
        with c1:
            with card("perclass"):
                card_title(f"Skor per emosi: {model}", "Seberapa baik model mengenali tiap emosi.")
                if pc is None:
                    missing(f"per_class_{model}.csv")
                else:
                    st.dataframe(
                        pc, hide_index=True, width="stretch",
                        column_config={
                            "label": "Emosi",
                            "precision": st.column_config.NumberColumn("Precision", format="%.2f"),
                            "recall": st.column_config.NumberColumn("Recall", format="%.2f"),
                            "f1": st.column_config.ProgressColumn(
                                "F1", min_value=0, max_value=1, format="%.2f"),
                            "support": st.column_config.NumberColumn("Teks", format="%d")})
                    hard, easy = pc.loc[pc["f1"].idxmin()], pc.loc[pc["f1"].idxmax()]
                    st.caption(f"Paling sulit dikenali: {hard['label']} (F1 {hard['f1']:.2f}). "
                               f"Paling mudah: {easy['label']} (F1 {easy['f1']:.2f}).")
        with c2:
            with card("matrix"):
                card_title("Confusion matrix", "Baris: label sebenarnya. Kolom: tebakan model.")
                norm = st.toggle("Tampilkan persentase per baris", value=True, key="norm_eval")
                if cm is None:
                    missing(f"confusion_{model}.csv")
                else:
                    st.plotly_chart(heatmap(cm, norm), width="stretch")
        with st.expander("Apa arti angka-angka ini?"):
            st.markdown(
                "- **Macro F1:** rata-rata skor F1 dari semua emosi, dengan bobot sama. Emosi yang "
                "jarang muncul (misalnya love) tetap dihitung sama pentingnya dengan yang sering.\n"
                "- **Precision:** dari semua teks yang ditebak joy, berapa persen yang benar joy.\n"
                "- **Recall:** dari semua teks yang sebenarnya joy, berapa persen yang berhasil ditemukan.\n"
                "- **F1:** gabungan precision dan recall dalam satu angka.\n"
                "- **Confusion matrix:** diagonal yang gelap berarti tebakan benar. Sel gelap di luar "
                "diagonal menunjukkan dua emosi yang sering tertukar.")

# ---------- 3. Lintas domain ----------
with tab_cross:
    intro("Model dilatih pada dataset utama, lalu diuji pada EmoT yang gaya bahasanya berbeda. "
          "Apakah model benar-benar memahami emosi, atau hanya hafal pola dataset pertama? "
          "Hasilnya dilaporkan terpisah dari evaluasi utama.")
    has_emot = comp is not None and "macro_f1_emot" in comp
    if has_emot:
        row = comp[comp["model"] == model].iloc[0]
        drop = row["macro_f1_test"] - row["macro_f1_emot"]
        k = st.columns(3, gap="medium")
        with k[0]:
            kpi("Macro F1 data utama", f"{row['macro_f1_test']:.3f}", f"model {model}")
        with k[1]:
            kpi("Macro F1 EmoT", f"{row['macro_f1_emot']:.3f}", "data dari sumber lain")
        with k[2]:
            kpi("Perubahan skor", f"{-drop:+.3f}", "turun di domain baru itu wajar", hi=True)

        with card("crosscompare"):
            card_title("Data utama dibandingkan EmoT", "Semua model, Macro F1.")
            fig = px.bar(comp, x="model", y=["macro_f1_test", "macro_f1_emot"], barmode="group",
                         text_auto=".2f", color_discrete_sequence=[B700, CHART_YEL])
            fig.for_each_trace(lambda t: t.update(
                name={"macro_f1_test": "data uji utama", "macro_f1_emot": "EmoT"}[t.name]))
            fig.update_traces(textposition="outside", cliponaxis=False,
                              textfont=dict(color=INK, size=13))
            fig.update_yaxes(range=[0, 1.05], title_text="Macro F1")
            fig.update_xaxes(title_text=None)
            st.plotly_chart(round_bars(style_fig(fig, 340, legend=True)), width="stretch")
            d = comp.assign(turun=comp["macro_f1_test"] - comp["macro_f1_emot"])
            tough = d.loc[d["turun"].idxmin()]
            st.caption(f"Paling tahan beda domain: {tough['model']} "
                       f"(skor turun {tough['turun']:.2f}).")

    cd = read_csv(str(RESULTS / f"cross_domain_{model}.csv"), index_col=0)
    with card("crossmatrix"):
        card_title(f"Confusion matrix EmoT: {model}",
                   "EmoT tidak punya kelas neutral, jadi tidak ada baris neutral. "
                   "Kolom neutral hanya muncul sebagai tebakan model.")
        if cd is None:
            missing(f"cross_domain_{model}.csv")
        else:
            norm = st.toggle("Tampilkan persentase per baris", value=True, key="norm_cross")
            st.plotly_chart(heatmap(cd, norm), width="stretch")

# ---------- 4. Analisis error ----------
with tab_err:
    intro("Di mana model sering keliru? Tab ini menunjukkan pasangan emosi yang paling sering "
          "tertukar dan contoh kalimat yang salah ditebak. Ini bahan utama untuk analisis di laporan.")
    cm = read_csv(str(RESULTS / f"confusion_{model}.csv"), index_col=0)
    if cm is None:
        missing(f"confusion_{model}.csv")
    else:
        total = int(cm.values.sum())
        wrong = total - int(np.trace(cm.values))
        tc = top_confusions(cm)
        t1 = tc.iloc[0]
        k = st.columns(3, gap="medium")
        with k[0]:
            kpi("Pasangan paling sering tertukar", t1["pasangan"],
                f"{t1['jumlah']} kali pada data uji", hi=True)
        with k[1]:
            kpi("Total kesalahan", fmt_int(wrong), f"dari {fmt_int(total)} teks uji")
        with k[2]:
            kpi("Tingkat kesalahan", f"{wrong / total:.0%}", f"model {model}")
        with card("pairs"):
            card_title("Pasangan yang paling sering tertukar",
                       "Format: label sebenarnya → tebakan model.")
            fig = px.bar(tc, x="jumlah", y="pasangan", orientation="h", text="jumlah",
                         color_discrete_sequence=[B700])
            fig.update_traces(textposition="outside", cliponaxis=False,
                              textfont=dict(color=INK, size=14))
            fig.update_yaxes(autorange="reversed", title_text=None)
            fig.update_xaxes(title_text="jumlah teks")
            st.plotly_chart(round_bars(style_fig(fig, 320, grid="x")), width="stretch")

    err = read_csv(str(RESULTS / "error_examples.csv"))
    with card("examples"):
        card_title("Contoh teks yang salah ditebak", "Saring berdasarkan label atau tebakan model.")
        if err is None:
            missing("error_examples.csv")
        else:
            f1, f2 = st.columns(2)
            true_f = f1.multiselect("Label sebenarnya", LABELS, placeholder="Semua label")
            pred_f = f2.multiselect("Tebakan model", LABELS, placeholder="Semua label")
            view = err[err["model"] == model] if "model" in err else err
            if true_f:
                view = view[view["true_label"].isin(true_f)]
            if pred_f:
                view = view[view["pred_label"].isin(pred_f)]
            st.dataframe(view.drop(columns="model", errors="ignore"), hide_index=True,
                         width="stretch",
                         column_config={"text": "Teks", "true_label": "Label sebenarnya",
                                        "pred_label": "Tebakan model"})

# ---------- 5. Data ----------
with tab_data:
    intro("Gambaran dataset utama setelah dibersihkan. Sebaran yang tidak seimbang adalah alasan "
          "model dinilai dengan Macro F1, bukan akurasi biasa.")
    df = read_csv(str(DATA / "emosi_bersih.csv"))
    if df is None:
        st.info("Berkas `data/processed/emosi_bersih.csv` belum ada. "
                "Jalankan `python src/download_data.py`.")
    else:
        # Nama kolom disesuaikan otomatis; cek isi emosi_bersih.csv jika tampilan aneh.
        lab_col = "label" if "label" in df.columns else df.columns[-1]
        txt_col = next((c for c in ("text", "teks", "tweet", "kalimat") if c in df.columns),
                       next(c for c in df.columns if c != lab_col))
        counts = df[lab_col].value_counts().reindex(LABELS).dropna().astype(int)
        k = st.columns(4, gap="medium")
        with k[0]:
            kpi("Total teks", fmt_int(len(df)), "setelah dibersihkan", hi=True)
        with k[1]:
            kpi("Kelas terbanyak", counts.idxmax(), f"{fmt_int(counts.max())} teks")
        with k[2]:
            kpi("Kelas tersedikit", counts.idxmin(), f"{fmt_int(counts.min())} teks")
        with k[3]:
            kpi("Ketimpangan", f"{counts.max() / counts.min():.1f}x",
                "kelas terbanyak dibanding tersedikit")

        c1, c2 = st.columns([1, 1.2], gap="large")
        with c1:
            with card("dist"):
                card_title("Sebaran label", "Jumlah teks per emosi.")
                cdf = counts.sort_values(ascending=False).reset_index()
                cdf.columns = ["emosi", "jumlah"]
                fig = px.bar(cdf, x="emosi", y="jumlah", color="emosi", text="jumlah",
                             color_discrete_map=COLORS)
                fig.update_traces(textposition="outside", cliponaxis=False,
                                  textfont=dict(color=INK, size=13))
                fig.update_xaxes(title_text=None)
                fig.update_yaxes(title_text="jumlah teks")
                st.plotly_chart(round_bars(style_fig(fig, 340)), width="stretch")
        with c2:
            with card("length"):
                card_title("Panjang teks per emosi", "Jumlah kata. Garis tengah adalah median.")
                tmp = df.assign(kata=df[txt_col].astype(str).str.split().str.len())
                fig = px.box(tmp, x=lab_col, y="kata", color=lab_col, color_discrete_map=COLORS,
                             category_orders={lab_col: LABELS})
                fig.update_xaxes(title_text=None)
                fig.update_yaxes(title_text="jumlah kata")
                st.plotly_chart(style_fig(fig, 340), width="stretch")

        with card("words"):
            card_title("Kata paling sering per emosi", "Kata umum seperti 'yang' dan 'di' sudah dibuang.")
            pick = st.selectbox("Pilih emosi", LABELS, key="word_pick")
            words = Counter(w for t in df.loc[df[lab_col] == pick, txt_col].astype(str)
                            for w in t.lower().split() if w not in STOP and len(w) > 2)
            wd = pd.DataFrame(words.most_common(15), columns=["kata", "frekuensi"])
            fig = px.bar(wd, x="frekuensi", y="kata", orientation="h", text="frekuensi",
                         color_discrete_sequence=[COLORS[pick]])
            fig.update_traces(textposition="outside", cliponaxis=False,
                              textfont=dict(color=INK, size=13))
            fig.update_yaxes(autorange="reversed", title_text=None)
            fig.update_xaxes(title_text="jumlah kemunculan")
            st.plotly_chart(round_bars(style_fig(fig, 440, grid="x")), width="stretch")

        with st.expander("Contoh data"):
            st.dataframe(df.sample(min(20, len(df)), random_state=1), hide_index=True,
                         width="stretch")