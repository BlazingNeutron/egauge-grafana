from egaugepolling.config import Config
import pytest
from unittest.mock import patch, MagicMock
import json
from prometheus_client import REGISTRY


@pytest.fixture
def before_each_test():
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)
    yield


@pytest.fixture
def full_config_json() -> object:
    with open("tests/test_configs/test_config_full.json", "r") as f:
        return json.load(f)


@pytest.fixture
def no_metrics_config_json() -> object:
    with open("tests/test_configs/test_config_no_metrics.json", "r") as f:
        return json.load(f)


@pytest.fixture
def no_devices_config_json() -> object:
    with open("tests/test_configs/test_config_no_devices.json", "r") as f:
        return json.load(f)


@pytest.fixture
def empty_metrics_config_json() -> object:
    with open("tests/test_configs/test_config_empty_metrics.json", "r") as f:
        return json.load(f)


@pytest.fixture
def empty_devices_config_json() -> object:
    with open("tests/test_configs/test_config_empty_devices.json", "r") as f:
        return json.load(f)


@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_init_config(mockJson, mockOpen, mockOS, full_config_json):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = full_config_json

    config = Config()
    assert config.get_url("test") == "http://test/test"
    assert isinstance(config.get_metrics(), dict)
    assert len(config.get_metrics()) == 2


@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_config_no_metrics(mockJson, mockOpen, mockOS, no_metrics_config_json):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = no_metrics_config_json
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = Config()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "No metrics found in config.json"


@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_config_no_devices(mockJson, mockOpen, mockOS, no_devices_config_json):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = no_devices_config_json
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = Config()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "No devices found in config.json"


@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_config_empty_metrics(mockJson, mockOpen, mockOS, empty_metrics_config_json):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = empty_metrics_config_json
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = Config()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "No metrics found in config.json"


@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_config_empty_devices(mockJson, mockOpen, mockOS, empty_devices_config_json):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = empty_devices_config_json
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        config = Config()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "No devices found in config.json"


@patch("egaugepolling.config.start_http_server")
@patch("egaugepolling.config.webapi")
@patch("egaugepolling.config.os")
@patch("egaugepolling.config.open")
@patch("egaugepolling.config.json")
@pytest.mark.usefixtures("before_each_test")
def test_get_token(
    mockJson, mockOpen, mockOS, mockWebAPI, mockPrometheus, full_config_json
):
    mockOS.getenv.side_effect = ["user", "password"]
    mockJson.load.return_value = full_config_json

    config = Config()
    mockWebAPI.JWTAuth.return_value = "TEST_TOKEN"
    assert config.get_token() == "TEST_TOKEN"
    assert config.get_token() == "TEST_TOKEN"
    mockWebAPI.JWTAuth.assert_called_once()
