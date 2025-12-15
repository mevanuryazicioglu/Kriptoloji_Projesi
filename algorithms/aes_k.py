# algorithms/aes.py
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipherTR:
    """
    Key: 16/24/32 karakter (UTF-8'e çevrilir)
    Encrypt output: base64(iv):base64(ciphertext)
    """

    def __init__(self, key: str):
        if not isinstance(key, str) or len(key) not in (16, 24, 32):
            raise ValueError("AES anahtarı 16, 24 veya 32 karakter olmalı")
        self.key = key.encode("utf-8")

    def encrypt(self, plaintext: str) -> str:
        if not isinstance(plaintext, str):
            raise ValueError("AES encrypt: text string olmalı")

        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        ct = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))

        return f"{base64.b64encode(iv).decode()}:{base64.b64encode(ct).decode()}"

    def decrypt(self, ciphertext: str) -> str:
        if not isinstance(ciphertext, str) or ":" not in ciphertext:
            raise ValueError("AES decrypt: format base64(iv):base64(ciphertext) olmalı")

        iv_b64, ct_b64 = ciphertext.split(":", 1)
        iv = base64.b64decode(iv_b64)
        ct = base64.b64decode(ct_b64)

        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode("utf-8")
