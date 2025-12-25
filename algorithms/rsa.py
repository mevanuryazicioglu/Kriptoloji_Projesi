# algorithms/rsa.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class RSACipherTR:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = RSA.import_key(private_key)
            self.public_key = self.private_key.publickey()
        else:
            key = RSA.generate(2048)
            self.private_key = key
            self.public_key = key.publickey()

        self.encryptor = PKCS1_OAEP.new(self.public_key)
        self.decryptor = PKCS1_OAEP.new(self.private_key)

    def encrypt_bytes(self, data: bytes) -> str:
        return base64.b64encode(self.encryptor.encrypt(data)).decode()

    def decrypt_bytes(self, data_b64: str) -> bytes:
        return self.decryptor.decrypt(base64.b64decode(data_b64))

    def export_private_key(self) -> str:
        return self.private_key.export_key().decode()