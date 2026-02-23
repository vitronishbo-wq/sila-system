from typing import List, Dict


class AggregationService:
    def aggregate_sum(self, series: List[Dict], value_key: str = "value"):
        return sum(item.get(value_key, 0) for item in series)

    def aggregate_avg(self, series: List[Dict], value_key: str = "value"):
        values = [item.get(value_key, 0) for item in series]
        return sum(values) / len(values) if values else 0

    def aggregate_rate(self, series: List[Dict], value_key: str = "value"):
        # placeholder: compute rate using first/last
        if not series:
            return 0
        first = series[-1][value_key]
        last = series[0][value_key]
        return (last - first) / first if first else 0

    def group_by_dimension(self, series: List[Dict], dim_key: str):
        groups = {}
        for item in series:
            key = item.get("dimensions", {}).get(dim_key)
            groups.setdefault(key, []).append(item)
        return groups
