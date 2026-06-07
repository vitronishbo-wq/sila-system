class AggregationService:
    def aggregate_sum(self, series: list[dict], value_key: str = "value"):
        return sum(item.get(value_key, 0) for item in series)

    def aggregate_avg(self, series: list[dict], value_key: str = "value"):
        values = [item.get(value_key, 0) for item in series]
        return sum(values) / len(values) if values else 0

    def aggregate_rate(self, series: list[dict], value_key: str = "value"):
        if not series:
            return 0
        first = series[-1][value_key]
        last = series[0][value_key]
        return (last - first) / first if first else 0

    def group_by_dimension(self, series: list[dict], dim_key: str):
        groups = {}
        for item in series:
            key = item.get("dimensions", {}).get(dim_key)
            groups.setdefault(key, []).append(item)
        return groups
