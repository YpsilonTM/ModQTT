# OCPP SIGEN to MQTT – Add-on Documentation

## What it does

This add-on starts an OCPP 1.6 central system (WebSocket server).  Your EV
charger connects to it, and the add-on bridges charger telemetry to MQTT topics
readable by Home Assistant.  Start/stop charging and other commands are sent
via MQTT.

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `ocpp_host` | `0.0.0.0` | Interface to bind the OCPP WebSocket server on. |
| `ocpp_port` | `9200` | TCP port the charger connects to. |
| `mqtt_host` | `core-mosquitto` | MQTT broker hostname. |
| `mqtt_port` | `1883` | MQTT broker port. |
| `mqtt_username` | _(empty)_ | MQTT username. |
| `mqtt_password` | _(empty)_ | MQTT password. |
| `mqtt_client_id` | `ocppsigen2mqtt-addon` | MQTT client ID. |
| `topic_prefix` | `ocpp` | Root topic prefix for all published topics. |
| `log_level` | `INFO` | Log verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |

## MQTT Topics

All topics are prefixed with the configured `topic_prefix` (default `ocpp`).

### Published by bridge

| Topic | Payload | Description |
|-------|---------|-------------|
| `{prefix}/{cp_id}/availability` | `online`/`offline` | Charger connection state |
| `{prefix}/bridge/availability` | `online`/`offline` | Bridge status |
| `{prefix}/{cp_id}/power_w` | float | Active power in Watts |
| `{prefix}/{cp_id}/current_a` | float | Import current in Amps |
| `{prefix}/{cp_id}/total_energy_wh` | float | Total energy in Wh |
| `{prefix}/{cp_id}/voltage_v` | float | Voltage in Volts |
| `{prefix}/{cp_id}/metrics` | JSON | All metrics combined |
| `{prefix}/{cp_id}/status` | JSON | Latest `StatusNotification` payload |
| `{prefix}/{cp_id}/connector/{n}/status` | string | Connector status string |
| `{prefix}/{cp_id}/boot` | JSON | `BootNotification` payload |
| `{prefix}/{cp_id}/transaction/active` | JSON | Active transaction info |
| `{prefix}/{cp_id}/transaction/last` | JSON | Last completed transaction |
| `{prefix}/{cp_id}/command_result/start` | JSON | Result of start command |
| `{prefix}/{cp_id}/command_result/stop` | JSON | Result of stop command |
| `{prefix}/{cp_id}/command_result/reset` | JSON | Result of reset command |
| `{prefix}/{cp_id}/command_result/get_config` | JSON | Result of GetConfiguration |
| `{prefix}/{cp_id}/command_result/set_config` | JSON | Result of ChangeConfiguration |

### Subscribed (commands)

| Topic | Payload (JSON) | Description |
|-------|----------------|-------------|
| `{prefix}/{cp_id}/command/start` | `{"connector_id": 1, "id_tag": "REMOTE"}` | Start charging |
| `{prefix}/{cp_id}/command/stop` | `{"transaction_id": 123}` _(optional if active)_ | Stop charging |
| `{prefix}/{cp_id}/command/reset` | `{"type": "Soft"}` | Reset charger |
| `{prefix}/{cp_id}/command/get_config` | `{"keys": ["HeartbeatInterval"]}` | Read config keys |
| `{prefix}/{cp_id}/command/set_config` | `{"key": "HeartbeatInterval", "value": "60"}` | Write config key |

`{cp_id}` is the last path segment of the WebSocket URL the charger connects on
(e.g. `ws://bridge-host:9200/120A64150210` → cp_id = `120A64150210`).

## Charger setup

Point your charger's OCPP server URL to:
```
ws://<HA-host>:9200/<charge_point_id>
```
Set the subprotocol to `ocpp1.6`.

Ensure port `9200` is exposed in the add-on Network settings.

## Local development

```bash
MQTT_HOST=192.168.50.11 MQTT_USER=homeassistant MQTT_PASS=mqtt \
  OCPP_PORT=9200 MQTT_TOPIC_PREFIX=dev/ocpp \
  python3 src/server.py
```
