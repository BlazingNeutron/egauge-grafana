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
    testmetric.build_metrics(
        [
            {
                "type": "gauge",
                "id": "test_gauge",
                "name": "Test Gauge",
                "description": "test desc",
                "labels": ["test_label"],
            }
        ]
    )
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert metric_map["Test Gauge"] is not None
    assert isinstance(metric_map["Test Gauge"], Gauge)


@pytest.mark.usefixtures("before_each_test")
def test_counter_metric():
    testmetric = Metrics()
    testmetric.build_metrics(
        [
            {
                "type": "COUNTER",
                "id": "test_counter",
                "name": "Test Counter",
                "description": "test desc",
                "labels": ["test_label"],
            }
        ]
    )
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert metric_map["Test Counter"] is not None
    assert isinstance(metric_map["Test Counter"], Counter)


@pytest.mark.usefixtures("before_each_test")
def test_metrics_labels():
    testmetric = Metrics()
    testmetric.build_metrics(
        [
            {
                "type": "COUNTER",
                "id": "test_counter",
                "name": "Test Counter",
                "description": "test desc",
                "labels": ["test_label1", "test_label2"],
            }
        ]
    )
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert metric_map["Test Counter"] is not None
    assert isinstance(metric_map["Test Counter"], Counter)
    assert len(metric_map["Test Counter"]._labelnames) == 2


@pytest.mark.usefixtures("before_each_test")
def test_type_misspelled():
    testmetric = Metrics()
    testmetric.build_metrics(
        [
            {
                "type": "gOuge",
                "id": "test_gauge",
                "name": "Test Gauge",
                "description": "test desc",
                "labels": ["test_label"],
            }
        ]
    )
    metric_map = testmetric.get_metrics()
    assert metric_map is not None
    assert len(metric_map) == 0
