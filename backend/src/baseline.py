KAMUS_GAUL = {
    "gak": "tidak", "ga": "tidak", "nggak": "tidak", "engga": "tidak",
    "bgt": "banget", "bgtt": "banget", "bngt": "banget",
    "sm": "sama", "sma": "sama", "dgn": "dengan",
    "yg": "yang", "utk": "untuk", "krn": "karena",
    "sdh": "sudah", "udh": "sudah", "blm": "belum",
    "bkn": "bukan", "tp": "tapi", "tpi": "tapi",
    "aja": "saja", "aj": "saja", "doang": "saja",
    "ak": "aku", "aq": "aku", "gw": "aku", "gue": "aku",
    "km": "kamu", "kmu": "kamu", "lu": "kamu", "lo": "kamu",
}


def normalisasi_teks(teks):
    teks = str(teks).lower()
    kata = teks.split()
    kata_normal = [KAMUS_GAUL.get(k, k) for k in kata]
    return " ".join(kata_normal)
