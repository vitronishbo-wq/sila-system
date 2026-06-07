import hashlib


class SignatureVerifier:
    def verify(self, payload, signature):
        calc = hashlib.sha256(payload.encode()).hexdigest()
        return calc == signature
