import re


class Anonymizer:
    PATTERNS = [
        (re.compile(r"\b\d{16}\b"), "[NIK]"),
        (re.compile(r"\b(?:\+62|62|0)8\d{8,11}\b"), "[NOMOR_HP]"),
        (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "[EMAIL]"),
        (re.compile(r"https?://\S+"), "[URL]"),
    ]

    def anonymize(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        for pattern, replacement in self.PATTERNS:
            text = pattern.sub(replacement, text)
        return text
