# algorithms/des_k.py
import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from algorithms.rsa import RSACipherTR

class DESCipherTR:
    def encrypt(self, plaintext: str):
        des_key = get_random_bytes(8)
        iv = get_random_bytes(8)

        cipher = DES.new(des_key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), DES.block_size))

        rsa = RSACipherTR()

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
            "encrypted_key": rsa.encrypt_bytes(des_key),
            "private_key": rsa.export_private_key()
        }

    def decrypt(self, data: dict):
        rsa = RSACipherTR(data["private_key"])
        des_key = rsa.decrypt_bytes(data["encrypted_key"])

        iv = base64.b64decode(data["iv"])
        ciphertext = base64.b64decode(data["ciphertext"])

        cipher = DES.new(des_key, DES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), DES.block_size).decode()