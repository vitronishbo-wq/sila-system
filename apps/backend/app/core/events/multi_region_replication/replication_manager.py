class ReplicationManager:
    def __init__(self):
        self.nodes = []

    def register_node(self, node):
        self.nodes.append(node)

    async def replicate(self, event):
        for node in self.nodes:
            await node.replicate(event)
