import hashlib


class PostQuantumCrypto:
    def encrypt(self, data):
        return hashlib.sha512(data.encode()).hexdigest()

    def decrypt(self, token):
        return token
