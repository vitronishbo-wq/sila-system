class NationalAnalytics:
    """National-scale analytics aggregation"""

    def aggregate(self, datasets):
        """Aggregate datasets computing min, max, average"""
        result = {}

        for name, values in datasets.items():
            if values:
                result[name] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values)
                }
            else:
                result[name] = {
                    "min": None,
                    "max": None,
                    "avg": None
                }

        return result
