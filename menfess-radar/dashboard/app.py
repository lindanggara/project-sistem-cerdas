import streamlit as st

st.set_page_config(page_title="Menfess Radar", page_icon="📡", layout="wide")
st.title("Menfess Radar")
st.caption("Analisis topik menfess dan prediksi balasan")
st.info(
    "Dashboard starter. Hubungkan dataset yang sudah diizinkan, hasil pemodelan topik, "
    "dan model prediksi setelah pipeline analisis siap."
)

left, right = st.columns(2)
with left:
    st.subheader("Analisis topik")
    st.write("Ringkasan distribusi topik dan tren akan ditampilkan di bagian ini.")
with right:
    st.subheader("Prediksi balasan")
    st.write("Prediksi baru diaktifkan setelah definisi target, fitur, dan evaluasi model tersedia.")
