
from darter.config import DarterConfig


def test_load():
    config = DarterConfig()
    assert isinstance(config.get("influxdb"), dict)
    assert "host" in config.get("influxdb")
    assert "database" in config.get("influxdb")
    assert "user" in config.get("influxdb")
    assert "pass" in config.get("influxdb")