from algorithms.caesar import CaesarCipherTR
from algorithms.vigenere import VigenereCipherTR
from algorithms.affine import AffineCipherTR

class Server:
    def __init__(self):
        self.algorithms = {
            "Caesar": CaesarCipherTR(),
            "Vigenere": VigenereCipherTR(),
            "Affine": AffineCipherTR()
        }

    def encrypt(self, algorithm, text, key1=None, key2=None):
        if algorithm == "Caesar":
            if key1 is not None:
                self.algorithms[algorithm].shift = key1
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Vigenere":
            if key1 is not None:
                self.algorithms[algorithm].key = key1
            return self.algorithms[algorithm].encrypt(text)
        elif algorithm == "Affine":
            if key1 is not None and key2 is not None:
                self.algorithms[algorithm].a = key1
                self.algorithms[algorithm].b = key2
            return self.algorithms[algorithm].encrypt(text)

    def decrypt(self, algorithm, text, key1=None, key2=None):
        if algorithm == "Caesar":
            if key1 is not None:
                self.algorithms[algorithm].shift = key1
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Vigenere":
            if key1 is not None:
                self.algorithms[algorithm].key = key1
            return self.algorithms[algorithm].decrypt(text)
        elif algorithm == "Affine":
            if key1 is not None and key2 is not None:
                self.algorithms[algorithm].a = key1
                self.algorithms[algorithm].b = key2
            return self.algorithms[algorithm].decrypt(text)
