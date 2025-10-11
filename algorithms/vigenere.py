from algorithms.alphabet import TURKISH_ALPHABET, M

class VigenereCipherTR:
    def __init__(self, key="ANAHTAR"):
        self.key = key.upper()
        self.alphabet = TURKISH_ALPHABET
        self.m = M

    def encrypt(self, text):
        result = ""
        key_index = 0
        text = text.upper()
        for char in text:
            if char in self.alphabet:
                shift = self.alphabet.index(self.key[key_index % len(self.key)])
                idx = self.alphabet.index(char)
                result += self.alphabet[(idx + shift) % self.m]
                key_index += 1
            else:
                result += char
        return result

    def decrypt(self, text):
        result = ""
        key_index = 0
        text = text.upper()
        for char in text:
            if char in self.alphabet:
                shift = self.alphabet.index(self.key[key_index % len(self.key)])
                idx = self.alphabet.index(char)
                result += self.alphabet[(idx - shift) % self.m]
                key_index += 1
            else:
                result += char
        return result
