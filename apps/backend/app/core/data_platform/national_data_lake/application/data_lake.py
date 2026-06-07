class NationalDataLake:
    def __init__(self):
        self.storage = {}

    def ingest(self, dataset_name, data):
        if dataset_name not in self.storage:
            self.storage[dataset_name] = []
        self.storage[dataset_name].append(data)

    def read(self, dataset_name):
        return self.storage.get(dataset_name, [])
