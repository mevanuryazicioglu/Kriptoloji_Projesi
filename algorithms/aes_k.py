# algorithms/aes_k.py
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from algorithms.rsa import RSACipherTR

class AESCipherTR:
    def encrypt(self, plaintext: str):
        aes_key = get_random_bytes(16)
        iv = get_random_bytes(16)

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

        rsa = RSACipherTR()

        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
            "encrypted_key": rsa.encrypt_bytes(aes_key),
            "private_key": rsa.export_private_key()
        }

    def decrypt(self, data: dict):
        rsa = RSACipherTR(data["private_key"])
        aes_key = rsa.decrypt_bytes(data["encrypted_key"])

        iv = base64.b64decode(data["iv"])
        ciphertext = base64.b64decode(data["ciphertext"])

        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()