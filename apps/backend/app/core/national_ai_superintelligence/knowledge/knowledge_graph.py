class KnowledgeGraph:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, data):
        self.nodes[node_id] = data

    def add_edge(self, source, target, relation):
        self.edges.append((source, target, relation))