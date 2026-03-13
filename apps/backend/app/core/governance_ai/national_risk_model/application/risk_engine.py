class NationalRiskEngine:

    def __init__(self):

        self.risks = {}

    def register_risk(

        self,
        risk_name,
        probability,
        severity

    ):

        self.risks[risk_name] = {

            "probability": probability,
            "severity": severity

        }

    def evaluate(self):

        results = {}

        for name, data in self.risks.items():

            score = data["probability"] * data["severity"]

            results[name] = score

        return results
