import numpy as np
from algorithms.alphabet import TURKISH_ALPHABET, ALPHABET_SIZE


class HillCipherTR:
    def __init__(self, key_matrix=None):
        self.alphabet = TURKISH_ALPHABET
        self.m = ALPHABET_SIZE  
        self.key_matrix = key_matrix  

    def _char_to_num(self, char):
        try:
            return self.alphabet.index(char)
        except ValueError:
            print("Bulunamayan karakter:", char)
            raise HTTPException(status_code=400, detail=f"Geçersiz karakter: {char}")

    def _num_to_char(self, num):
        return self.alphabet[num % self.m]

    def _create_matrix_for_decrypt(self):
        det = int(round(np.linalg.det(self.key_matrix)))
        det_inv = None
        for i in range(self.m):
            if (det * i) % self.m == 1:
                det_inv = i
                break
        if det_inv is None:
            raise ValueError("Anahtar matrisi mod 29'a göre terslenemiyor")
        adj = np.round(det * np.linalg.inv(self.key_matrix)).astype(int)
        inv_key = (det_inv * adj) % self.m
        return inv_key

    def encrypt(self, text):
        n = self.key_matrix.shape[0]
        text = text.replace(" ", "").upper()
        if len(text) % n != 0:
            text += "X" * (n - len(text) % n)

        numbers = [self._char_to_num(c) for c in text]
        result = ""
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i+n])
            encrypted_block = np.dot(self.key_matrix, block) % self.m
            result += ''.join(self._num_to_char(x) for x in encrypted_block)
        return result

    def decrypt(self, text):
        n = self.key_matrix.shape[0]
        numbers = [self._char_to_num(c) for c in text]
        result = ""
        inv_key = self._create_matrix_for_decrypt()
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i+n])
            decrypted_block = np.dot(inv_key, block) % self.m
            result += ''.join(self._num_to_char(x) for x in decrypted_block)
        return result
