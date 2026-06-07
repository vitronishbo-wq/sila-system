class CivilizationEngine:
    def __init__(self):
        self.entities = []
        self.events = []

    def register(self, entity):
        self.entities.append(entity)

    def emit(self, event):
        self.events.append(event)

    def state(self):
        return {"entities": len(self.entities), "events": len(self.events)}
