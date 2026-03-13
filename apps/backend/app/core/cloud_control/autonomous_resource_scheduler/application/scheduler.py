class AutonomousScheduler:

    def __init__(self, compute_grid):

        self.compute_grid = compute_grid

    def schedule(self, workload):

        for node_id, node in self.compute_grid.nodes.items():

            if node["status"] == "available":

                node["status"] = "busy"

                return {

                    "node": node_id,
                    "workload": workload

                }

        raise Exception("no available nodes")
