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
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="anomaly_event" or r._measurement=="maintenance_recommendation" or r._measurement=="asset_risk" or r._measurement=="kpi" or r._measurement=="segment_status")' --org comasa --token comasa-demo-token
```

For the `perdida_vapor_condensado` demo, open `COMASA - Revision integrada por problema` and read the first row of the segment ranking. It identifies the critical water/steam/condensate tramo with endpoint nodes, TAG, quality, risk reason, recommended action, and cost/efficiency impact.

See `docs/demo.md` for the pitch/runbook.

Grafana auto-loads the dashboards under the `COMASA` folder: decision center, operator, maintenance/risk, boiler/biomass, water/steam/condensate, executive/finance, and the additive problem-first integrated review. They query `telemetry_raw`, `segment_status`, `asset_risk`, `anomaly_event`, `maintenance_recommendation`, and `kpi` from InfluxDB.
