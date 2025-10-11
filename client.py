from server import Server

class Client:
    def __init__(self):
        self.server = Server()

    def send_encrypt_request(self, algorithm, text, key1=None, key2=None):
        return self.server.encrypt(algorithm, text, key1, key2)

    def send_decrypt_request(self, algorithm, text, key1=None, key2=None):
        return self.server.decrypt(algorithm, text, key1, key2)
