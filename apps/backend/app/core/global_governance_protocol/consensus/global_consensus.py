class GlobalConsensus:

    def __init__(self):
        self.votes = {}

    def vote(self, member, proposal):
        self.votes.setdefault(proposal, []).append(member)

    def result(self, proposal):
        return len(self.votes.get(proposal, []))