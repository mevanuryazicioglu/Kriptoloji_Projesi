from algorithms.alphabet import TURKISH_ALPHABET, M


class CaesarCipherTR:
    def __init__(self, shift=3):
        self.shift = shift
        self.alphabet = TURKISH_ALPHABET
        self.m = M  # 29 harf

    def encrypt(self, text):
        result = ""
        text = text.upper()
        for char in text:
            if char in self.alphabet:
                idx = self.alphabet.index(char)
                result += self.alphabet[(idx + self.shift) % self.m]
            else:
                result += char
        return result

    def decrypt(self, text):
        result = ""
        text = text.upper()
        for char in text:
            if char in self.alphabet:
                idx = self.alphabet.index(char)
                result += self.alphabet[(idx - self.shift) % self.m]
            else:
                result += char
        return result
