class CrisisResponseAI:
    def __init__(self):
        self.responses = {}

    def register_response(self, crisis_type, action):
        self.responses[crisis_type] = action

    def respond(self, crisis_type):
        action = self.responses.get(crisis_type)
        if not action:
            return "no response defined"
        return action
