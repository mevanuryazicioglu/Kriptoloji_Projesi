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
            # Karakter alfabede bulunamazsa, 0 döndür veya uygun bir hata işle
            # Bu hata server.py tarafından zaten handle ediliyor olabilir
            return 0  # Ya da uygun bir varsayılan değer


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

    def _create_matrix_for_decrypt(self):
        det = int(round(np.linalg.det(self.key_matrix))) % self.m
        if det == 0:
            raise ValueError("Determinant 0 olamaz.")

        det_inv = self._modinv(det, self.m)

        # Eşlenik matrisi (adjoint matrix) hesapla
        # 2x2 matris için basitleştirilmiş eşlenik matris
        if self.key_matrix.shape == (2, 2):
            adj = np.array([
                [self.key_matrix[1, 1], -self.key_matrix[0, 1]],
                [-self.key_matrix[1, 0], self.key_matrix[0, 0]]
            ]) % self.m
        elif self.key_matrix.shape == (3, 3):
            # 3x3 için kofaktör matrisinin transpozunu almalıyız
            adj = np.zeros_like(self.key_matrix)
            for i in range(3):
                for j in range(3):
                    minor = np.delete(np.delete(self.key_matrix, i, axis=0), j, axis=1)
                    cofactor = int(round(np.linalg.det(minor))) * ((-1)**(i+j))
                    adj[j, i] = cofactor % self.m # Transpoz alınmış oluyor
        else:
            raise ValueError("Şu an sadece 2x2 ve 3x3 matrisler desteklenmektedir.")

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
