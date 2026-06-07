class DigitalTwinCountry:
    def __init__(self):
        self.models = {}

    def update_model(self, sector, data):
        self.models[sector] = data

    def get_model(self, sector):
        return self.models.get(sector)
