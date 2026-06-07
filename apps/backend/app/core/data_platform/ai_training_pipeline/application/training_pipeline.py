class AITrainingPipeline:
    def __init__(self, data_lake):
        self.data_lake = data_lake

    def prepare_dataset(self, dataset_name):
        data = self.data_lake.read(dataset_name)
        return {"records": len(data), "dataset": data}

    def train_model(self, dataset):
        model = {"trained_on": dataset["records"], "status": "trained"}
        return model
