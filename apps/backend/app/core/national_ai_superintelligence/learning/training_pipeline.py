class TrainingPipeline:

    def __init__(self, data_lake):
        self.data_lake = data_lake

    async def train(self, model):
        dataset = await self.data_lake.query()
        model.parameters['trained_on'] = len(dataset)
        return model