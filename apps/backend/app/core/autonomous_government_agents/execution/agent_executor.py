class AgentExecutor:

    def __init__(self, registry):
        self.registry = registry

    async def execute(self, agent_name, context):
        agent = self.registry.get(agent_name)
        if not agent:
            raise Exception('Agent not found')
        return await agent.act(context)