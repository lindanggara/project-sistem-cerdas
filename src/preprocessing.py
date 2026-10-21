"""Fungsi preprocessing teks; implementasikan setelah skema data ditetapkan."""


def clean_text(text: str) -> str:
    """Bersihkan teks dasar tanpa menghapus makna yang relevan."""
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().split())
