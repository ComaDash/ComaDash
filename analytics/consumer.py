import json
import os
import time

import paho.mqtt.client as mqtt

from influx_writer import InfluxWriter
from kpis import current_kpis
from recommendations import build
from rules import evaluate
from window_store import WindowStore


class AnalyticsConsumer:
    def __init__(self) -> None:
        self.host = os.getenv("COMASA_MQTT_HOST", "localhost")
        self.port = int(os.getenv("COMASA_MQTT_PORT", "1883"))
        self.store = WindowStore()
        self.writer = InfluxWriter()
        self.last_emitted: dict[str, float] = {}

    def run(self) -> None:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="comadash-analytics")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.host, self.port, keepalive=30)
        print(f"Analytics consuming COMASA/# from {self.host}:{self.port}", flush=True)
        client.loop_forever()

    def on_connect(self, client: mqtt.Client, _userdata, _flags, reason_code, _properties=None) -> None:
        if int(reason_code) == 0:
            client.subscribe("COMASA/#", qos=0)

    def on_message(self, _client: mqtt.Client, _userdata, msg: mqtt.MQTTMessage) -> None:
        try:
            point = json.loads(msg.payload.decode("utf-8"))
            if "value" not in point or "variable" not in point:
                return
            self.store.add(point)
            self.writer.write_kpis(current_kpis(self.store))
            for anomaly in evaluate(self.store):
                if self._should_emit(anomaly["type"]):
                    self.writer.write_anomaly(anomaly)
                    self.writer.write_recommendation(build(anomaly))
                    print(f"analytics event: {anomaly['type']} {anomaly['severity']} {anomaly['message']}", flush=True)
        except Exception as exc:  # keep demo worker alive on malformed payloads
            print(f"analytics skipped malformed/error payload: {exc}", flush=True)

    def _should_emit(self, anomaly_type: str) -> bool:
        now = time.time()
        last = self.last_emitted.get(anomaly_type, 0.0)
        if now - last < 30:
            return False
        self.last_emitted[anomaly_type] = now
        return True
