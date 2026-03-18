class SovereignDataPlatform:

    def __init__(self, data_lake, warehouse, stream, training):
        self.data_lake = data_lake
        self.warehouse = warehouse
        self.stream = stream
        self.training = training

    def ingest_data(self, dataset, record):
        self.data_lake.ingest(dataset, record)
        self.stream.publish(dataset, record)

    def train_ai(self, dataset):
        prepared = self.training.prepare_dataset(dataset)
        return self.training.train_model(prepared)