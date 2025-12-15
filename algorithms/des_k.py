import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class DESCipherTR:
    def __init__(self, key: str):
        if not isinstance(key, str) or len(key) != 8:
            raise ValueError("DES anahtarı 8 karakter (64 bit) olmalı")
        self.key = key.encode("utf-8")

    def encrypt(self, plaintext: str) -> str:
        if not isinstance(plaintext, str):
            raise ValueError("DES encrypt: text string olmalı")

        # DES için blok boyutu 8 bayttır.
        # IV her şifreleme için rastgele olmalı
        iv = get_random_bytes(8)  
        cipher = DES.new(self.key, DES.MODE_CBC, iv=iv)
        ct = cipher.encrypt(pad(plaintext.encode("utf-8"), DES.block_size))

        return f"{base64.b64encode(iv).decode()}:{base64.b64encode(ct).decode()}"

    def decrypt(self, ciphertext: str) -> str:
        if not isinstance(ciphertext, str) or ":" not in ciphertext:
            raise ValueError("DES decrypt: format base64(iv):base64(ciphertext) olmalı")

        iv_b64, ct_b64 = ciphertext.split(":", 1)
        iv = base64.b64decode(iv_b64)
        ct = base64.b64decode(ct_b64)

        cipher = DES.new(self.key, DES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), DES.block_size)
        return pt.decode("utf-8")

