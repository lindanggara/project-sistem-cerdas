import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

try:
    from baseline import normalisasi_teks
except ImportError as e:
    raise ImportError(
        "normalisasi_teks() tidak ditemukan di src/baseline.py. "
        "Pastikan file baseline.py ada di backend/src/."
    ) from e


def preprocess(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    return normalisasi_teks(text)
