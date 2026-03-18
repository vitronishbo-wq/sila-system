class IntelligenceEvent:
    """Intelligence domain event"""

    def __init__(self, category, payload):
        self.category = category
        self.payload = payload