class SovereignComputeGrid:

    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, cpu, memory):
        self.nodes[node_id] = {'cpu': cpu, 'memory': memory, 'status': 'available'}

    def list_nodes(self):
        return self.nodes