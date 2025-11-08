import numpy as np

class DESCipherTR:
    def __init__(self, key):
        if len(key) != 8:
            raise ValueError("Anahtar 8 karakter olmalı (64 bit)")
        self.key = ''.join(f'{ord(c):08b}' for c in key)
        self.block_size = 8

        self.IP = [58,50,42,34,26,18,10,2,
                   60,52,44,36,28,20,12,4,
                   62,54,46,38,30,22,14,6,
                   64,56,48,40,32,24,16,8,
                   57,49,41,33,25,17,9,1,
                   59,51,43,35,27,19,11,3,
                   61,53,45,37,29,21,13,5,
                   63,55,47,39,31,23,15,7]

        self.FP = [40,8,48,16,56,24,64,32,
                   39,7,47,15,55,23,63,31,
                   38,6,46,14,54,22,62,30,
                   37,5,45,13,53,21,61,29,
                   36,4,44,12,52,20,60,28,
                   35,3,43,11,51,19,59,27,
                   34,2,42,10,50,18,58,26,
                   33,1,41,9,49,17,57,25]

    def _permute(self, bits, table):
        return ''.join(bits[i-1] for i in table)

    def _xor(self, a, b):
        return ''.join('0' if i == j else '1' for i, j in zip(a, b))

    def _feistel(self, right, subkey):
        return self._xor(right[::-1], subkey[:len(right)])  # basitleştirilmiş sahte F fonksiyonu

    def _string_to_bits(self, s):
        return ''.join(f'{ord(c):08b}' for c in s)

    def _bits_to_string(self, b):
        chars = [chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8)]
        return ''.join(chars)

    def encrypt(self, plaintext):
        # Blok uzunluğunu 8'in katına tamamla
        if len(plaintext) % self.block_size != 0:
            plaintext += 'X' * (self.block_size - len(plaintext) % self.block_size)

        result = ""
        for i in range(0, len(plaintext), self.block_size):
            block = self._string_to_bits(plaintext[i:i+self.block_size])
            block = self._permute(block, self.IP)
            L, R = block[:32], block[32:]

            for _ in range(16):  # 16 tur
                temp = R
                R = self._xor(L, self._feistel(R, self.key))
                L = temp

            final_block = self._permute(R+L, self.FP)
            result += self._bits_to_string(final_block)
        return result

    def decrypt(self, ciphertext):
        # Uzunluk kontrolü
        if len(ciphertext) % self.block_size != 0:
            raise ValueError("Geçersiz şifreli metin: uzunluk 8'in katı olmalı!")

        result = ""
        for i in range(0, len(ciphertext), self.block_size):
            block = self._string_to_bits(ciphertext[i:i+self.block_size])
            block = self._permute(block, self.IP)
            L, R = block[:32], block[32:]

            for _ in range(16):  # 16 tur, ama ters sırada işlem
                temp = L
                L = self._xor(R, self._feistel(L, self.key))
                R = temp

            final_block = self._permute(R+L, self.FP)
            result += self._bits_to_string(final_block)

        # Şifre çözüm sonrası X'leri temizle
        return result.rstrip('X')
