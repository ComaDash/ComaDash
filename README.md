# ComaDash — COMASA predictive-energy prototype

Hackathon thin slice: a Python digital twin publishes COMASA UNS MQTT telemetry, Telegraf stores raw points in InfluxDB, and a Python analytics worker writes anomaly/recommendation/KPI events before Grafana visualization.

## Start

```bash
cp .env.example .env
docker compose up -d
```

Useful URLs:

- Grafana: <http://localhost:3000> (`admin` / `admin` by default)
- InfluxDB: <http://localhost:8086>
- MQTT: `localhost:1883`

## Inject a scenario

Edit `.env` and set `SIM_SCENARIO`, then restart the simulator:

```bash
SIM_SCENARIO=fouling_caldera docker compose up -d --force-recreate simulator
```

Supported scenarios: `normal`, `fouling_caldera`, `humedad_biomasa_alta`, `perdida_vapor_condensado`, `desbalance_turbina`, `cavitacion_bomba`, `combustion_inestable`.

## Inspect data

MQTT example:

```bash
docker compose exec mosquitto mosquitto_sub -t 'COMASA/#' -v
```

InfluxDB raw telemetry example:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="telemetry_raw") |> limit(n:20)' --org comasa --token comasa-demo-token
```

Derived analytics example:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="anomaly_event" or r._measurement=="maintenance_recommendation" or r._measurement=="asset_risk" or r._measurement=="kpi")' --org comasa --token comasa-demo-token
```

See `docs/demo.md` for the pitch/runbook.

Grafana auto-loads six dashboards under the `COMASA` folder: decision center, operator, maintenance/risk, boiler/biomass, water/steam/condensate, and executive/finance views. They query `telemetry_raw`, `asset_risk`, `anomaly_event`, `maintenance_recommendation`, and `kpi` from InfluxDB.
