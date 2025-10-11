from algorithms.alphabet import TURKISH_ALPHABET, ALPHABET_SIZE
from math import gcd

class AffineCipherTR:
    def __init__(self, a=5, b=8):
        self.alphabet = TURKISH_ALPHABET
        self.m = ALPHABET_SIZE
        if gcd(a, self.m) != 1:
            raise ValueError("‘a’ sayısı alfabe uzunluğu ile aralarında asal olmalı!")
        self.a = a
        self.b = b

    def encrypt(self, text):
        result = ""
        text = text.upper()
        for char in text:
            if char in self.alphabet:
                idx = self.alphabet.index(char)
                result += self.alphabet[(self.a * idx + self.b) % self.m]
            else:
                result += char
        return result

    def decrypt(self, text):
        result = ""
        text = text.upper()
        # modüler ters
        a_inv = None
        for i in range(self.m):
            if (self.a * i) % self.m == 1:
                a_inv = i
                break
        if a_inv is None:
            raise ValueError("a için modüler ters bulunamadı")

        for char in text:
            if char in self.alphabet:
                idx = self.alphabet.index(char)
                result += self.alphabet[(a_inv * (idx - self.b)) % self.m]
            else:
                result += char
        return result
