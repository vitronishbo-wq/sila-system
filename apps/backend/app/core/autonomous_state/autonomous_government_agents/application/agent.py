class GovernmentAgent:

    def __init__(self, name):
        self.name = name

    def execute_task(self, task):
        return {'agent': self.name, 'task': task, 'status': 'completed'}