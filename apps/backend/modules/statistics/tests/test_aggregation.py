from app.modules.statistics.application.services.aggregation_service import AggregationService


def test_aggregate_sum_avg():
    svc = AggregationService()
    series = [{"value": 1}, {"value": 2}, {"value": 3}]
    assert svc.aggregate_sum(series) == 6
    assert svc.aggregate_avg(series) == 2


def test_group_by_dimension():
    svc = AggregationService()
    series = [{"value": 1, "dimensions": {"k": "a"}}, {"value": 2, "dimensions": {"k": "b"}}, {"value": 3, "dimensions": {"k": "a"}}]
    groups = svc.group_by_dimension(series, "k")
    assert len(groups.get("a")) == 2
