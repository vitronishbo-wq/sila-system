class SecurityEvent:
    """Security domain event"""

    def __init__(self, type, payload):
        self.type = type
        self.payload = payload
