# COMASA demo runbook

## 1. Start the stack

```bash
cp .env.example .env
docker compose up -d
```

## 2. Show normal operation

Keep `SIM_SCENARIO=normal`. Inspect MQTT or InfluxDB raw points using the commands in `README.md`.

## 3. Inject failures

Run one scenario at a time:

```bash
SIM_SCENARIO=fouling_caldera docker compose up -d --force-recreate simulator
SIM_SCENARIO=humedad_biomasa_alta docker compose up -d --force-recreate simulator
SIM_SCENARIO=perdida_vapor_condensado docker compose up -d --force-recreate simulator
SIM_SCENARIO=desbalance_turbina docker compose up -d --force-recreate simulator
```

Expected pitch beat: the simulator changes causal signals, the analytics worker persists `anomaly_event`, `maintenance_recommendation`, and `kpi`, then Grafana/Influx can show the decision layer.

## 4. Reset demo data

```bash
docker compose down -v
docker compose up -d
```

## 5. Fallback if live services fail

Explain the architecture from `docs/architecture.md`, then show MQTT topics and JSON payload contracts from `simulator/catalog.py`. The code preserves real water/vapor/condensate TAG examples such as `FT_5001`, `FT_3001`, `FT_5101-1`, and `TIC_5101-1`.
