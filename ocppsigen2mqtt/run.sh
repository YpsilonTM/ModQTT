#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import json
from pathlib import Path

import yaml

options_path = Path('/data/options.json')
if not options_path.exists():
    # Running outside Home Assistant – env vars used directly by the app
    import sys
    print("No /data/options.json found – using environment variables", flush=True)
    sys.exit(0)

with options_path.open('r', encoding='utf-8') as fh:
    options = json.load(fh)

config = {
    'ocpp': {
        'host': options.get('ocpp_host', '0.0.0.0'),
        'port': int(options.get('ocpp_port', 9200)),
    },
    'charger_id': options.get('charger_id', '120A64150210'),
    'usable_phases': int(options.get('usable_phases', 2)),
    'mqtt': {
        'host': options.get('mqtt_host', 'core-mosquitto'),
        'port': int(options.get('mqtt_port', 1883)),
        'username': options.get('mqtt_username') or None,
        'password': options.get('mqtt_password') or None,
        'client_id': options.get('mqtt_client_id', 'ocppsigen2mqtt-addon'),
        'topic_prefix': options.get('topic_prefix', 'ocpp'),
    },
    'log_level': options.get('log_level', 'INFO'),
}

out = Path('/data/ocppsigen2mqtt.yaml')
with out.open('w', encoding='utf-8') as fh:
    yaml.safe_dump(config, fh, sort_keys=False)

print(f"Runtime config written to {out}", flush=True)
PY

if [ -f /data/ocppsigen2mqtt.yaml ]; then
    exec python3 /app/src/server.py --config /data/ocppsigen2mqtt.yaml
else
    exec python3 /app/src/server.py
fi
