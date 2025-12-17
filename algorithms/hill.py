import numpy as np
from algorithms.alphabet import TURKISH_ALPHABET, ALPHABET_SIZE


class HillCipherTR:
    def __init__(self, key_matrix=None):
        self.alphabet = TURKISH_ALPHABET
        self.m = ALPHABET_SIZE
        # Server tarafı key'i bazen liste olarak (ör. [[3,3],[2,5]]) gönderiyor.
        # Burada hem numpy array hem de listeyi kabul edip normalize ediyoruz.
        self.key_matrix = None
        if key_matrix is not None:
            self.set_key_matrix(key_matrix)

    def set_key_matrix(self, key_matrix):
        mat = np.array(key_matrix, dtype=int)
        if mat.ndim != 2 or mat.shape[0] != mat.shape[1]:
            raise ValueError("Hill anahtar matrisi kare olmalı (2x2 veya 3x3)")
        if mat.shape[0] not in (2, 3):
            raise ValueError("Şu an sadece 2x2 ve 3x3 matrisler desteklenmektedir.")
        self.key_matrix = mat % self.m

    def _char_to_num(self, char):
        # Sessizce 0 döndürmek hatayı gizleyip yanlış şifre/çözmeye sebep oluyor.
        # Geçersiz karakter gelirse açık hata verelim.
        return self.alphabet.index(char)

    def _num_to_char(self, num):
        return self.alphabet[num % self.m]

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def _egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self._egcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def _modinv(self, a, m):
        g, x, y = self._egcd(a, m)
        if g != 1:
            raise Exception("Mod inverse yok (a ve m aralarında asal değil).")
        return x % m

    def _mod_det(self, matrix):
        n = matrix.shape[0]
        if n == 1:
            return matrix[0, 0] % self.m
        if n == 2:
            return (matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0] + self.m * self.m) % self.m

        det = 0
        for c in range(n):
            minor = np.delete(np.delete(matrix, 0, axis=0), c, axis=1)
            det = (det + ((-1) ** c) * matrix[0, c] * self._mod_det(minor)) % self.m
        return (det + self.m) % self.m

    def _create_matrix_for_decrypt(self):
        det = self._mod_det(self.key_matrix)
        if det == 0:
            raise ValueError("Determinant 0 olamaz. Anahtar matrisi tersi alınamaz.")

        det_inv = self._modinv(det, self.m)

        n = self.key_matrix.shape[0]
        adj = np.zeros_like(self.key_matrix)

        if n == 2:
            adj[0, 0] = self.key_matrix[1, 1]
            # 2x2 için adj(A) = [[d, -b], [-c, a]]
            adj[0, 1] = (-self.key_matrix[0, 1] + self.m) % self.m
            adj[1, 0] = (-self.key_matrix[1, 0] + self.m) % self.m
            adj[1, 1] = self.key_matrix[0, 0]
        elif n == 3:
            for i in range(n):
                for j in range(n):
                    minor_matrix = np.delete(np.delete(self.key_matrix, i, axis=0), j, axis=1)
                    cofactor_val = self._mod_det(minor_matrix)
                    signed_cofactor = cofactor_val * ((-1) ** (i + j))
                    adj[j, i] = (signed_cofactor % self.m + self.m) % self.m
        else:
            raise ValueError("Şu an sadece 2x2 ve 3x3 matrisler desteklenmektedir.")

        inv_key = (det_inv * adj) % self.m
        return inv_key

    def encrypt(self, text):
        if self.key_matrix is None:
            raise ValueError("Hill anahtar matrisi ayarlanmamış")

        n = self.key_matrix.shape[0]
        text = text.replace(" ", "").upper()

        # Dolgu karakteri: Türkçe alfabede var ve kelime sonunda gelmesi nispeten nadir
        pad_char = "Z"
        if len(text) % n != 0:
            text += pad_char * (n - len(text) % n)

        numbers = [self._char_to_num(c) for c in text]
        result = ""
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i + n])
            encrypted_block = np.dot(self.key_matrix, block) % self.m
            result += ''.join(self._num_to_char(x) for x in encrypted_block)
        return result

    def decrypt(self, text):
        if self.key_matrix is None:
            raise ValueError("Hill anahtar matrisi ayarlanmamış")

        n = self.key_matrix.shape[0]
        text = text.replace(" ", "").upper()

        # 1) Harfleri sayıya çevir
        numbers = [self.alphabet.index(c) for c in text]

        # 2) Ters anahtar matrisi
        inv_key = self._create_matrix_for_decrypt()

        # 3) Blok blok çöz
        result = ""
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i+n])
            dec_block = np.dot(inv_key, block) % self.m
            result += "".join(self.alphabet[int(x)] for x in dec_block)

        # 4) Encrypt'te eklenen padding'i temizle
        return result.rstrip("Z")

