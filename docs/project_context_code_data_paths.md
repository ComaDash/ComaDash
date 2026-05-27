# Project Context, Code Paths, and Data Paths

## Purpose

ComaDash is a hackathon prototype for COMASA predictive energy monitoring. It simulates industrial plant telemetry, sends it through MQTT using a COMASA-style unified namespace, persists raw and derived time-series data in InfluxDB, and visualizes operational, maintenance, and financial signals in Grafana.

The current stack is intentionally small and local:

- Python simulator as a digital twin.
- Mosquitto as the MQTT broker.
- Telegraf as the raw telemetry ingestor.
- InfluxDB 2.x as the time-series database.
- Python analytics worker for KPIs, risk, anomalies, recommendations, and segment ranking.
- Grafana with provisioned dashboards and datasource.

## Top-Level Repository Map

| Path | Role |
|---|---|
| `docker-compose.yml` | Defines all runtime services: Mosquitto, InfluxDB, Telegraf, Grafana, simulator, and analytics. |
| `.env.example` | Default environment variables for local Docker execution. |
| `README.md` | Quick start, scenario injection, and example inspection queries. |
| `docs/architecture.md` | Detailed architecture proposal and industrial context. |
| `simulator/` | Python digital twin that generates and publishes telemetry to MQTT. |
| `analytics/` | Python MQTT consumer that calculates derived measurements and writes them to InfluxDB. |
| `telegraf/telegraf.conf` | Telegraf MQTT-to-InfluxDB raw telemetry pipeline. |
| `mqtt/config/mosquitto.conf` | Mosquitto broker configuration mounted into the container. |
| `grafana/provisioning/` | Datasource and dashboard provisioning for Grafana. |
| `grafana/dashboards/` | JSON dashboards loaded into Grafana under the `COMASA` folder. |
| `info/` | Source/reference material from the COMASA challenge, including PDFs and XLSX references. |
| `scripts/smoke.ps1` | Smoke-test helper script. |

## Runtime Services

`docker-compose.yml` is the executable architecture:

- `mosquitto` exposes MQTT on `localhost:1883` and uses `mqtt/config/mosquitto.conf`.
- `influxdb` exposes InfluxDB on `localhost:8086`, initializes org `comasa`, bucket `comasa`, and token `comasa-demo-token` by default.
- `telegraf` subscribes to `COMASA/#` and writes JSON payloads as `telemetry_raw` into InfluxDB.
- `grafana` exposes `localhost:3000`, provisions the InfluxDB datasource, and loads dashboards from `grafana/dashboards/`.
- `simulator` runs `python main.py` from `simulator/` and publishes plant telemetry.
- `analytics` runs `python main.py` from `analytics/`, consumes MQTT telemetry, computes derived outputs, and writes them to InfluxDB.

## Code Path: Simulator

Entry point:

```text
simulator/main.py
  -> publisher.run()
```

Main execution path:

```text
simulator/publisher.py
  -> reads COMASA_MQTT_HOST, COMASA_MQTT_PORT, COMASA_MQTT_TOPIC_PREFIX, SIM_SCENARIO, SIM_INTERVAL_SECONDS
  -> validates SIM_SCENARIO against scenarios.SCENARIOS
  -> connects MQTT client comadash-simulator
  -> creates PlantState
  -> loops forever:
       PlantState.advance()
       for every Signal in catalog.SIGNALS:
         signals.payload(signal, scenario, tick)
         catalog.topic(prefix, signal)
         MQTT publish
```

Important simulator files:

- `simulator/catalog.py` defines the signal catalog. Each `Signal` contains area, equipment, variable, unit, baseline, noise, optional TAG, and optional segment metadata such as `from_node`, `to_node`, `fluid`, `unit_generator`, `source_sheet`, and `stage`.
- `simulator/scenarios.py` defines supported scenarios and how each scenario changes signal values through multipliers and offsets.
- `simulator/signals.py` builds the final payload, adds timestamp and metadata, applies baseline/noise/scenario logic, and returns JSON-serializable dictionaries.
- `simulator/plant_state.py` stores only a simple increasing `tick` counter.

Supported scenarios:

- `normal`
- `fouling_caldera`
- `humedad_biomasa_alta`
- `perdida_vapor_condensado`
- `desbalance_turbina`
- `cavitacion_bomba`
- `combustion_inestable`

Example MQTT topic shape:

```text
COMASA/Lautaro/Planta1/{Area}/{Equipment}/{OptionalTag}/{Variable}
```

Example topics from the current catalog:

```text
COMASA/Lautaro/Planta1/Caldera/Gases/TemperaturaEscape
COMASA/Lautaro/Planta1/Generacion/Turbina/VibracionRMS
COMASA/Lautaro/Planta1/VaporSobrecalentado/Caldera/FT_5101-1/Flujo
COMASA/Lautaro/Planta1/Condensado/Retorno/FT_3001/Flujo
```

Example payload shape:

```json
{
  "timestamp": "2026-05-27T12:00:00.000Z",
  "site": "Lautaro",
  "plant": "Planta1",
  "area": "Condensado",
  "equipment": "Retorno",
  "tag": "FT_3001",
  "variable": "Flujo",
  "value": 71.0,
  "unit": "ton/h",
  "quality": "GOOD",
  "source": "digital-twin+xlsx-reference",
  "scenario": "normal",
  "from_node": "Proceso/retorno",
  "to_node": "Tanque condensado",
  "fluid": "Condensado",
  "unit_generator": "UG1",
  "operating_condition": "Media carga",
  "source_sheet": "UG_1_MT",
  "stage": "Retorno condensado"
}
```

## Code Path: Raw Telemetry Ingestion

Telegraf is the raw telemetry path:

```text
telegraf/telegraf.conf
  -> [[inputs.mqtt_consumer]] subscribes to COMASA/#
  -> parses JSON payloads with json_v2
  -> stores them as InfluxDB measurement telemetry_raw
  -> [[outputs.influxdb_v2]] writes to INFLUXDB_BUCKET
```

`telemetry_raw` mapping:

- Measurement: `telemetry_raw`
- Timestamp: `timestamp` from the MQTT payload
- Field: `value` as float
- Tags: `site`, `plant`, `area`, `equipment`, `tag`, `variable`, `unit`, `quality`, `scenario`, `source`
- Optional tags: `from_node`, `to_node`, `fluid`, `unit_generator`, `operating_condition`, `source_sheet`, `stage`

This path preserves the simulator payloads as raw time-series readings for dashboard queries and historical inspection.

## Code Path: Analytics Worker

Entry point:

```text
analytics/main.py
  -> AnalyticsConsumer().run()
```

Main execution path:

```text
analytics/consumer.py
  -> reads COMASA_MQTT_HOST and COMASA_MQTT_PORT
  -> creates WindowStore
  -> creates InfluxWriter
  -> connects MQTT client comadash-analytics
  -> subscribes to COMASA/#
  -> on every valid JSON payload:
       WindowStore.add(point)
       InfluxWriter.write_kpis(current_kpis(store))
       InfluxWriter.write_asset_risk(current_asset_risk(store))
       InfluxWriter.write_segment_status(current_segment_status(store))
       for anomaly in rules.evaluate(store):
         if not emitted in the last 30 seconds:
           InfluxWriter.write_anomaly(anomaly)
           InfluxWriter.write_recommendation(build(anomaly))
```

Important analytics files:

- `analytics/window_store.py` keeps a rolling in-memory window of the latest points grouped by `variable`.
- `analytics/kpis.py` calculates demo KPIs such as energy generated, biomass throughput, OEE, MTBF, MTTR, water per MWh, vapor per MWh, condensate recovery, and estimated operating cost.
- `analytics/rules.py` evaluates threshold/trend/FFT-style anomaly rules.
- `analytics/risk.py` calculates current risk by asset and sorts highest risk first.
- `analytics/segment_status.py` calculates ranked water/steam/condensate segment status.
- `analytics/segments.py` maps known TAGs to segment context from the XLSX reference structure.
- `analytics/recommendations.py` maps anomaly types to probable causes, suggested actions, expected impact, and due times.
- `analytics/influx_writer.py` writes all derived analytics measurements to InfluxDB.

## Data Path: End-to-End Flow

The full local data path is:

```text
simulator/catalog.py + simulator/scenarios.py
  -> simulator/signals.py creates payloads
  -> simulator/publisher.py publishes to MQTT topic COMASA/#
  -> Mosquitto broker receives messages
  -> Telegraf subscribes to COMASA/#
  -> InfluxDB stores raw points in telemetry_raw
  -> Analytics worker also subscribes to COMASA/#
  -> WindowStore maintains rolling state
  -> KPI/risk/rule/segment modules calculate derived outputs
  -> InfluxWriter stores derived points in InfluxDB
  -> Grafana queries InfluxDB datasource InfluxDB-COMASA
  -> Dashboards render operational, maintenance, segment, and financial views
```

## InfluxDB Measurements

| Measurement | Writer | Purpose |
|---|---|---|
| `telemetry_raw` | Telegraf | Raw simulator telemetry from MQTT. |
| `kpi` | `analytics/influx_writer.py` | Derived KPI values, tagged by KPI name and unit. |
| `asset_risk` | `analytics/influx_writer.py` | Current risk ranking by equipment/area/status/severity. |
| `segment_status` | `analytics/influx_writer.py` | Decision view for water/steam/condensate segments. |
| `anomaly_event` | `analytics/influx_writer.py` | Emitted anomaly events with severity, score, message, cause, and impacted KPIs. |
| `maintenance_recommendation` | `analytics/influx_writer.py` | Suggested maintenance actions linked to anomalies. |

## Grafana Data Path

Grafana provisioning path:

```text
grafana/provisioning/datasources/influxdb.yml
  -> creates datasource InfluxDB-COMASA using Flux

grafana/provisioning/dashboards/dashboards.yml
  -> loads JSON dashboards from /var/lib/grafana/dashboards
  -> mounted from grafana/dashboards/
```

Dashboard JSON files currently include:

- `grafana/dashboards/master.json`
- `grafana/dashboards/operator.json`
- `grafana/dashboards/maintenance.json`
- `grafana/dashboards/boiler_biomass.json`
- `grafana/dashboards/water_steam_condensate.json`
- `grafana/dashboards/finance.json`
- `grafana/dashboards/problem_first_operations.json`

The dashboards query the InfluxDB bucket configured by `INFLUXDB_BUCKET`, normally `comasa`.

## Configuration Path

Default local configuration starts from `.env.example`:

```text
.env.example
  -> docker compose environment interpolation
  -> service-specific environment variables
```

Key variables:

| Variable | Used By | Meaning |
|---|---|---|
| `COMASA_MQTT_HOST` | simulator, analytics, Telegraf | MQTT broker hostname. |
| `COMASA_MQTT_PORT` | simulator, analytics, Telegraf | MQTT broker port. |
| `COMASA_MQTT_TOPIC_PREFIX` | simulator | Topic prefix for generated telemetry. |
| `SIM_SCENARIO` | simulator | Scenario used to alter generated values. |
| `SIM_INTERVAL_SECONDS` | simulator | Publish interval. |
| `INFLUXDB_URL` | Telegraf, analytics, Grafana | InfluxDB endpoint. |
| `INFLUXDB_ORG` | InfluxDB clients | InfluxDB organization. |
| `INFLUXDB_BUCKET` | InfluxDB clients | Target bucket. |
| `INFLUXDB_ADMIN_TOKEN` | InfluxDB clients | Token used by Telegraf, analytics, and Grafana. |
| `COST_BIOMASS_PER_TON` | analytics | Demo biomass cost constant. |
| `COST_WATER_PER_M3` | analytics | Demo water cost constant. |
| `COST_VAPOR_LOSS_PER_TON` | analytics | Demo vapor-loss cost constant. |
| `CONDENSATE_RECOVERY_BENEFIT_PER_TON` | analytics | Demo condensate recovery benefit. |
| `POWER_NOMINAL_MW` | analytics | Nominal power used in KPI/OEE calculations. |

## Important Domain Data Paths

The water/steam/condensate domain uses metadata from the project reference material:

```text
info/Agua, Vapor y Condensado Planta COMASA.xlsx
  -> referenced manually in docs/architecture.md
  -> represented in simulator/catalog.py as TAG metadata
  -> represented in analytics/segments.py as segment context
  -> emitted in simulator payloads as optional fields
  -> stored by Telegraf as telemetry_raw tags
  -> transformed by analytics/segment_status.py into segment_status
  -> queried by Grafana dashboards for problem-first ranking
```

This is not a full XLSX ingestion pipeline. The XLSX is used as a reference for TAGs, variables, units, source sheets, and segment context.

## Running and Inspecting

Start the stack:

```bash
cp .env.example .env
docker compose up -d
```

Inject a scenario:

```bash
SIM_SCENARIO=perdida_vapor_condensado docker compose up -d --force-recreate simulator
```

Inspect MQTT:

```bash
docker compose exec mosquitto mosquitto_sub -t 'COMASA/#' -v
```

Inspect raw telemetry:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="telemetry_raw") |> limit(n:20)' --org comasa --token comasa-demo-token
```

Inspect derived analytics:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="anomaly_event" or r._measurement=="maintenance_recommendation" or r._measurement=="asset_risk" or r._measurement=="kpi" or r._measurement=="segment_status")' --org comasa --token comasa-demo-token
```

## Mental Model

Think of the project as two consumers of the same MQTT telemetry stream:

- Telegraf is the lossless raw-data path into `telemetry_raw`.
- Analytics is the decision path that converts recent telemetry into KPIs, risks, anomalies, recommendations, and segment status.

Grafana does not calculate the core decisions itself. It reads both raw and derived InfluxDB measurements so the dashboard can show signals, rankings, causes, recommended actions, and estimated operational impact.
