class GovernmentSDK:
    def __init__(self, event_bus, identity):
        self.event_bus = event_bus
        self.identity = identity

    def emit_event(self, topic, payload):
        self.event_bus.publish(topic, payload)

    def authenticate(self, token):
        return self.identity.verify(token)
