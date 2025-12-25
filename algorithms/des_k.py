import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from algorithms.rsa import RSACipherTR


class DESCipherTR:
    def encrypt(self, plaintext: str):
        des_key = get_random_bytes(8)

        iv = get_random_bytes(8)

        cipher = DES.new(des_key, DES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), DES.block_size))

        rsa = RSACipherTR()

        return {
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),

            "encrypted_key": rsa.encrypt_bytes(des_key),

            "private_key": rsa.export_private_key()
        }

    def decrypt(self, data: dict):
        if "private_key" not in data:
            raise ValueError("DES Kütüphaneli decrypt: private_key eksik")
        if "encrypted_key" not in data:
            raise ValueError("DES Kütüphaneli decrypt: encrypted_key eksik")
        if "iv" not in data:
            raise ValueError("DES Kütüphaneli decrypt: iv eksik")
        if "ciphertext" not in data:
            raise ValueError("DES Kütüphaneli decrypt: ciphertext eksik")

        rsa = RSACipherTR(data["private_key"])

        des_key = rsa.decrypt_bytes(data["encrypted_key"])

     
        if not isinstance(des_key, (bytes, bytearray)):
            des_key = str(des_key).encode("utf-8")

        if len(des_key) != 8:
          
            if len(des_key) > 8:
                des_key = des_key[:8]
            else:
                des_key = des_key.ljust(8, b"\x00")

        iv = base64.b64decode(data["iv"])
        ciphertext = base64.b64decode(data["ciphertext"])

        if len(iv) != 8:
            raise ValueError(f"DES Kütüphaneli decrypt: IV uzunluğu 8 olmalı, gelen: {len(iv)}")

        cipher = DES.new(des_key, DES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)

        return plaintext.decode("utf-8")
