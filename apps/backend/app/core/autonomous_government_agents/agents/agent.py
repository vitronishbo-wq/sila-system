class GovernmentAgent:

    def __init__(self, name):
        self.name = name

    async def act(self, context):
        raise NotImplementedError