class PolicyOptimizer:

    def __init__(self, simulation_engine):
        self.simulation = simulation_engine

    def optimize(self, policy, scenarios):
        best = None
        for scenario in scenarios:
            result = self.simulation.run(scenario)
            if not best or result['impact'] > best['impact']:
                best = result
        return best