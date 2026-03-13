class CivilizationSimulator:

    def __init__(self, engine):
        self.engine = engine

    def simulate(self, steps=10):
        state = []
        for _ in range(steps):
            state.append(self.engine.state())
        return state