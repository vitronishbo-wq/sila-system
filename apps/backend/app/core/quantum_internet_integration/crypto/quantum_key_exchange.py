import secrets


class QuantumKeyExchange:
    def generate_key(self):
        return secrets.token_hex(32)
