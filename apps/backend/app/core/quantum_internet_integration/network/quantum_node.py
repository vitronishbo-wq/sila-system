class QuantumNode:

    def __init__(self, node_id):
        self.node_id = node_id
        self.links = []

    def connect(self, node):
        self.links.append(node)