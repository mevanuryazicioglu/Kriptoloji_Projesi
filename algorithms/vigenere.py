from algorithms.alphabet import TURKISH_ALPHABET


class VigenereCipherTR:
    def __init__(self, key="ANAHTAR"):
        self.alphabet = TURKISH_ALPHABET
        self.m = len(self.alphabet)
        self.pos = {ch: i for i, ch in enumerate(self.alphabet)}
        self.set_key(key)

    def set_key(self, key):
        cleaned_key = "".join(c for c in (key or "").upper() if c in self.pos)
        if not cleaned_key:
            raise ValueError("Vigenere anahtarı boş veya geçersiz (alfabe dışı karakter var).")
        self.key = cleaned_key

    def encrypt(self, text: str) -> str:
        # Ek güvenlik: key bir şekilde bozulduysa toparla
        if any((c not in self.pos) for c in self.key):
            self.set_key(self.key)

        out = []
        key_i = 0
        for ch in (text or "").upper():
            if ch in self.pos:
                kch = self.key[key_i % len(self.key)]
                shift = self.pos[kch]
                idx = self.pos[ch]
                out.append(self.alphabet[(idx + shift) % self.m])
                key_i += 1
            else:
                out.append(ch)
        return "".join(out)

    def decrypt(self, text: str) -> str:
        if any((c not in self.pos) for c in self.key):
            self.set_key(self.key)

        out = []
        key_i = 0
        for ch in (text or "").upper():
            if ch in self.pos:
                kch = self.key[key_i % len(self.key)]
                shift = self.pos[kch]
                idx = self.pos[ch]
                out.append(self.alphabet[(idx - shift) % self.m])
                key_i += 1
            else:
                out.append(ch)
        return "".join(out)
