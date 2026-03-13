import uuid

class KeyManager:

    def __init__(self):
        self.keys = {}

    def generate_key(self, owner):
        key = str(uuid.uuid4())
        self.keys[owner] = key
        return key