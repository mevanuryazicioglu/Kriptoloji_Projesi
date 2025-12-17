from algorithms.alphabet import TURKISH_ALPHABET, ALPHABET_SIZE


class VigenereCipherTR:
    def __init__(self, key="ANAHTAR"):
        self.alphabet = TURKISH_ALPHABET
        self.m = ALPHABET_SIZE

        # Harf -> index (string/list fark etmez, güvenli)
        self.pos = {ch: i for i, ch in enumerate(self.alphabet)}

        cleaned_key = "".join([c for c in (key or "").upper() if c in self.pos])
        if not cleaned_key:
            raise ValueError("Vigenere anahtarı boş veya geçersiz (alfabe dışı karakter var).")
        self.key = cleaned_key

    def encrypt(self, text: str) -> str:
        out = []
        key_i = 0
        for ch in (text or "").upper():
            if ch in self.pos:
                shift = self.pos[self.key[key_i % len(self.key)]]
                idx = self.pos[ch]
                out.append(self.alphabet[(idx + shift) % self.m])
                key_i += 1
            else:
                out.append(ch)
        return "".join(out)

    def decrypt(self, text: str) -> str:
        out = []
        key_i = 0
        for ch in (text or "").upper():
            if ch in self.pos:
                shift = self.pos[self.key[key_i % len(self.key)]]
                idx = self.pos[ch]
                out.append(self.alphabet[(idx - shift) % self.m])
                key_i += 1
            else:
                out.append(ch)
        return "".join(out)
