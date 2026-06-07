class GlobalIdentity:
    def __init__(self):
        self.registry = {}

    def register(self, entity_id, data):
        self.registry[entity_id] = data
