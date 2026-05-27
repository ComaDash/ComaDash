import json
import os
import time

import paho.mqtt.client as mqtt

from catalog import SIGNALS, topic
from plant_state import PlantState
from scenarios import SCENARIOS
from signals import payload


def run() -> None:
    host = os.getenv("COMASA_MQTT_HOST", "localhost")
    port = int(os.getenv("COMASA_MQTT_PORT", "1883"))
    prefix = os.getenv("COMASA_MQTT_TOPIC_PREFIX", "COMASA/Lautaro/Planta1")
    scenario = os.getenv("SIM_SCENARIO", "normal")
    interval = float(os.getenv("SIM_INTERVAL_SECONDS", "2"))
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown SIM_SCENARIO={scenario}. Valid: {sorted(SCENARIOS)}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="comadash-simulator")
    client.connect(host, port, keepalive=30)
    client.loop_start()
    state = PlantState(scenario=scenario)
    print(f"Publishing COMASA telemetry to {host}:{port} scenario={scenario}", flush=True)

    while True:
        tick = state.advance()
        for signal in SIGNALS:
            client.publish(topic(prefix, signal), json.dumps(payload(signal, scenario, tick)), qos=0)
        time.sleep(interval)
