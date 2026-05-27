# Implemented Plans

This file tracks the plans implemented during the project so future changes have a single place to reference what was changed, why, and where.

## 2026-05-27: Project Context Documentation

### Goal

Create a Markdown guide that explains the repository context, code paths, and data paths.

### Implemented

- Added `docs/project_context_code_data_paths.md`.
- Documented the top-level repository map.
- Documented Docker services from `docker-compose.yml`.
- Documented simulator code path from `simulator/main.py` to MQTT publishing.
- Documented Telegraf raw ingestion into InfluxDB measurement `telemetry_raw`.
- Documented analytics worker path from MQTT consumption to derived InfluxDB measurements.
- Documented Grafana provisioning and dashboard data flow.

### Key Files

- `docs/project_context_code_data_paths.md`
- `docker-compose.yml`
- `simulator/`
- `analytics/`
- `telegraf/telegraf.conf`
- `grafana/provisioning/`
- `grafana/dashboards/`

## 2026-05-27: Grafana Legend Normalization

### Goal

Fix noisy Grafana legends like:

```text
value {area="Caldera", equipment="Gases", plant="Planta1", quality="GOOD", scenario="normal", site="Lautaro", source="digital-twin", topic="COMASA/...", unit="mbar", variable="PresionDiferencial"}
```

### Cause

Grafana was using the full InfluxDB series label set because dashboard panels did not define explicit display names. Telegraf correctly stores metadata tags such as `area`, `equipment`, `plant`, `quality`, `scenario`, `site`, `source`, `unit`, and `variable`; Grafana then included all of them in default series names.

### Implemented

- Added `fieldConfig.defaults.displayName` to affected visualization panels.
- Added Flux `group(columns: [...])` to reduce labels used for series identity.
- Kept Telegraf metadata intact because it is useful for raw telemetry debugging and filtering.
- First validated the approach on `grafana/dashboards/boiler_biomass.json` panel `id: 5`.
- Expanded the same pattern across the remaining dashboards.

### Display Name Patterns Used

```text
${__field.labels.variable} (${__field.labels.unit})
${__field.labels.kpi} (${__field.labels.unit})
${__field.labels.tag} ${__field.labels.variable} (${__field.labels.unit})
${__field.labels.area} ${__field.labels.variable} (${__field.labels.unit})
${__field.labels.equipment}
${__field.labels.equipment} (${__field.labels.status})
```

### Changed Files

- `grafana/dashboards/boiler_biomass.json`
- `grafana/dashboards/finance.json`
- `grafana/dashboards/maintenance.json`
- `grafana/dashboards/master.json`
- `grafana/dashboards/operator.json`
- `grafana/dashboards/problem_first_operations.json`
- `grafana/dashboards/water_steam_condensate.json`

### Validation

- Validated modified dashboard JSON with `python -m json.tool`.
- Confirmed the first test panel rendered cleaner labels before applying the change broadly.

## 2026-05-27: Grafana Query Downsampling

### Goal

Fix Grafana errors like:

```text
A query returned too many datapoints and the results have been truncated at 10221 points to prevent memory issues.
At the current graph size, Grafana can only draw 1022.
Try using the aggregateWindow() function in your query to reduce the number of points returned.
```

### Cause

Some panels queried raw high-frequency `telemetry_raw` and `kpi` time-series points directly. With multiple signals and long dashboard ranges, Grafana received more points than it could draw for the panel size.

### Implemented

- Added Flux downsampling to dense time-series queries:

```flux
|> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
```

- Used Grafana's `v.windowPeriod` so the aggregation interval adapts to panel width and selected time range.
- Applied only to trend-style `timeseries` panels that return dense telemetry/KPI streams.
- Preserved the existing legend normalization.
- Did not apply this to table panels, stat panels, or already reduced `last()` queries unless they were dense trend queries.

### Changed Files

- `grafana/dashboards/boiler_biomass.json`
- `grafana/dashboards/finance.json`
- `grafana/dashboards/maintenance.json`
- `grafana/dashboards/master.json`
- `grafana/dashboards/operator.json`
- `grafana/dashboards/problem_first_operations.json`
- `grafana/dashboards/water_steam_condensate.json`

### Validation

- Validated modified dashboard JSON with `python -m json.tool`.

## 2026-05-27: Fixed-Window Operational Trends

### Goal

Fix operational trend charts that rendered as isolated points after using `v.windowPeriod` for downsampling.

### Cause

`v.windowPeriod` is useful for long/adaptive dashboard ranges, but on some fixed operational panels Grafana selected a window that was too large. This collapsed short-range trends into only one or a few points per series.

### Implemented

- Converted dense time-series dashboard queries to group first and then aggregate.
- Replaced `v.windowPeriod` with fixed windows based on query range:

```text
-20m / -30m -> 10s
-2h        -> 30s
-6h        -> 2m
-12h       -> 5m
```

- Applied this convention across Grafana dashboard time-series panels.
- Preserved label normalization with `fieldConfig.defaults.displayName`.

### Example

```flux
from(bucket: "${bucket}")
  |> range(start: -30m)
  |> filter(fn: (r) => r._measurement == "telemetry_raw" and r._field == "value")
  |> group(columns: ["tag", "variable", "unit"])
  |> aggregateWindow(every: 10s, fn: mean, createEmpty: false)
```

### Validation

- Validated modified dashboard JSON with `python -m json.tool`.

## Current Grafana Query Convention

For raw or KPI time-series panels, use this order:

```flux
from(bucket: "${bucket}")
  |> range(start: -30m)
  |> filter(fn: (r) => r._measurement == "telemetry_raw" and r._field == "value")
  |> group(columns: ["variable", "unit"])
  |> aggregateWindow(every: 10s, fn: mean, createEmpty: false)
```

Use fixed aggregation windows for fixed operational ranges. Avoid `v.windowPeriod` on short operational panels if it collapses the graph into too few visible points.

For current-value panels, keep reduced queries such as:

```flux
|> last()
```

For tables, use explicit `keep(columns: [...])` so Grafana shows only useful columns.

## Operational Notes

- After changing dashboard JSON files, restart Grafana to reload provisioned dashboards:

```bash
docker compose restart grafana
```

- Keep this file updated whenever a new implementation plan is completed.
- Prefer dashboard-level normalization before changing Telegraf tag ingestion, because the raw tags are useful for debugging and traceability.
