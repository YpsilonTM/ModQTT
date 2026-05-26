"""Tests for config loading."""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import Config


def test_defaults_from_env_no_vars(monkeypatch):
    for key in ["OCPP_HOST", "OCPP_PORT", "MQTT_HOST", "MQTT_PORT",
                "MQTT_USER", "MQTT_PASS", "MQTT_TOPIC_PREFIX", "CHARGER_ID", "OCPP_USABLE_PHASES", "LOG_LEVEL"]:
        monkeypatch.delenv(key, raising=False)
    cfg = Config.from_env()
    assert cfg.ocpp.host == "0.0.0.0"
    assert cfg.ocpp.port == 9200
    assert cfg.mqtt.host == "core-mosquitto"
    assert cfg.mqtt.topic_prefix == "ocpp"
    assert cfg.charger_id == "CHARGER01"
    assert cfg.usable_phases == 2
    assert cfg.log_level == "INFO"


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("OCPP_PORT", "9300")
    monkeypatch.setenv("MQTT_HOST", "192.168.1.10")
    monkeypatch.setenv("MQTT_TOPIC_PREFIX", "dev/ocpp")
    monkeypatch.setenv("CHARGER_ID", "120A64150210")
    monkeypatch.setenv("OCPP_USABLE_PHASES", "3")
    cfg = Config.from_env()
    assert cfg.ocpp.port == 9300
    assert cfg.mqtt.host == "192.168.1.10"
    assert cfg.mqtt.topic_prefix == "dev/ocpp"
    assert cfg.charger_id == "120A64150210"
    assert cfg.usable_phases == 3


def test_yaml_load(monkeypatch):
    for key in ["OCPP_HOST", "OCPP_PORT", "MQTT_HOST", "MQTT_PORT",
                "MQTT_USER", "MQTT_PASS", "MQTT_TOPIC_PREFIX", "CHARGER_ID", "OCPP_USABLE_PHASES", "LOG_LEVEL"]:
        monkeypatch.delenv(key, raising=False)

    data = {
        "ocpp": {"host": "0.0.0.0", "port": 9100},
        "charger_id": "120A64150210",
        "usable_phases": 3,
        "mqtt": {"host": "broker.local", "port": 1884, "topic_prefix": "prod/ocpp"},
        "log_level": "DEBUG",
    }
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
        yaml.safe_dump(data, fh)
        path = fh.name

    try:
        cfg = Config.from_yaml(path)
        assert cfg.ocpp.port == 9100
        assert cfg.mqtt.host == "broker.local"
        assert cfg.mqtt.topic_prefix == "prod/ocpp"
        assert cfg.charger_id == "120A64150210"
        assert cfg.usable_phases == 3
        assert cfg.log_level == "DEBUG"
    finally:
        os.unlink(path)
