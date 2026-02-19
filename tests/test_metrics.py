import pytest
from egaugepolling.metrics import Metrics
from prometheus_client import Gauge, Counter, REGISTRY

@pytest.fixture
def before_each_test():
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    yield
    
@pytest.mark.usefixtures("before_each_test")
def test_build_a_metric():
    testmetric = Metrics()
    testmetric.build_metrics([{
            "type": "gauge",
            "name": "test_gauge",
            "description": "test desc",
            "labels": [
                "test_label"
            ]
        }])
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert metric_map["test_gauge"] is not None
    assert isinstance(metric_map["test_gauge"], Gauge)

@pytest.mark.usefixtures("before_each_test")
def test_counter_metric():
    testmetric = Metrics()
    testmetric.build_metrics([{
            "type": "COUNTER",
            "name": "test_counter",
            "description": "test desc",
            "labels": [
                "test_label"
            ]
        }])
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert metric_map["test_counter"] is not None
    assert isinstance(metric_map["test_counter"], Counter)

@pytest.mark.usefixtures("before_each_test")
def test_metrics_labels():
    testmetric = Metrics()
    testmetric.build_metrics([{
            "type": "COUNTER",
            "name": "test_counter",
            "description": "test desc",
            "labels": [
                "test_label1", "test_label2"
            ]
        }])
    metric_map = testmetric.get_metrics()
    # c = Counter("na", "desc", ["l1", "l2"])
    assert metric_map is not None
    assert metric_map["test_counter"] is not None
    assert isinstance(metric_map["test_counter"], Counter)
    assert len(metric_map["test_counter"]._labelnames) == 2

@pytest.mark.usefixtures("before_each_test")
def test_type_misspelled():
    testmetric = Metrics()
    testmetric.build_metrics([{
            "type": "gOuge",
            "name": "test_gauge",
            "description": "test desc",
            "labels": [
                "test_label"
            ]
        }])
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert len(metric_map) == 0