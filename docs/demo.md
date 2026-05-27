# COMASA demo runbook

## 1. Start the stack

```bash
cp .env.example .env
docker compose up -d
```

## 2. Show normal operation

Keep `SIM_SCENARIO=normal`. Open Grafana at <http://localhost:3000> and use the provisioned dashboards in the `COMASA` folder:

- `COMASA - Centro de decisión operacional`: jury overview with risk ranking and recommended actions.
- `COMASA - Vista operador de turno`: live variables, alarms, and immediate action.
- `COMASA - Mantenimiento predictivo y riesgo de falla`: ordered list of assets close to failure, MTBF/MTTR, and maintenance backlog.
- `COMASA - Caldera y biomasa`: fouling, biomass quality, combustion stability, and biomass cost impact.
- `COMASA - Agua, vapor y condensado`: thermal circuit efficiency, TAG traceability, losses, and recommended action.
- `COMASA - Vista ejecutiva y finanzas`: OEE, energy, biomass, water, vapor, condensate, downtime, and cost impact.
- `COMASA - Revision integrada por problema`: problem-first view organized by operational questions and ranked `segment_status` rows.

Inspect MQTT or InfluxDB raw points using the commands in `README.md` if you need to prove the data path.

## 3. Inject failures

Run one scenario at a time:

```bash
SIM_SCENARIO=fouling_caldera docker compose up -d --force-recreate simulator
SIM_SCENARIO=humedad_biomasa_alta docker compose up -d --force-recreate simulator
SIM_SCENARIO=perdida_vapor_condensado docker compose up -d --force-recreate simulator
SIM_SCENARIO=desbalance_turbina docker compose up -d --force-recreate simulator
SIM_SCENARIO=cavitacion_bomba docker compose up -d --force-recreate simulator
SIM_SCENARIO=combustion_inestable docker compose up -d --force-recreate simulator
```

Expected pitch beat: the simulator changes causal signals, the analytics worker persists `asset_risk`, `anomaly_event`, `maintenance_recommendation`, and `kpi`, then Grafana/Influx can show the decision layer.

Recommended live sequence: start with the master dashboard, switch to operator for the alarm, open maintenance for the preventive action, then close with finance/jefatura to show cost and KPI impact.

### 3.1 Critical segment in under 10 seconds

For the water-loss narrative, use `SIM_SCENARIO=perdida_vapor_condensado` and open `COMASA - Revision integrada por problema`.

Under 10 seconds, point to the first row of **Ranking de tramos con razón, calidad y acción**:

1. **Status/risk**: the highest `risk_score` row is the segment to inspect first.
2. **Segment**: `from_node`, `to_node`, `fluid`, and `tag` identify the operational tramo, not only a generic asset.
3. **Reason**: `reason` explains the vapor-condensate gap or low condensate recovery.
4. **Action**: `recommendation_link` names the operator/maintenance action.
5. **Impact**: `cost_efficiency_impact` links the segment to water, steam, condensate recovery, and cost.

Suggested spoken line: "The problem is not just that condensate recovery fell; the ranked segment table says which tramo is critical, why, how reliable the data is, and what action reduces the thermal and water-loss cost."

## 4. Reset demo data

```bash
docker compose down -v
docker compose up -d
```

## 5. Fallback if live services fail

First run the quick smoke check so the team can identify whether Docker, Grafana, InfluxDB, or the derived analytics path is the failing piece:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke.ps1
```

If the live stack is not presentable, switch to the backup pitch instead of debugging in front of the jury:

1. Show `docs/architecture.md` and explain the data path: simulator -> MQTT/UNS -> Telegraf/InfluxDB plus analytics -> Grafana.
2. Show the MQTT topic and JSON payload contract from `simulator/catalog.py` and `simulator/signals.py`. Emphasize that the prototype preserves real water/vapor/condensate TAG examples such as `FT_5001`, `FT_3001`, `FT_5101-1`, and `TIC_5101-1`.
3. Show screenshots or a short video captured before the demo, if available. Minimum capture set: master dashboard normal operation, operator alarm, maintenance recommendation, finance/jefatura cost impact.
4. If screenshots/video are missing, open the dashboard JSON files under `grafana/dashboards/` and describe what each role would see: raw telemetry, `segment_status`, `asset_risk`, `anomaly_event`, `maintenance_recommendation`, and `kpi` measurements.

Suggested spoken fallback: "The live Docker stack is a local prototype, but the architecture and demo evidence are reproducible. The important part is the decision layer: explainable events and recommendations are generated before Grafana, with KPI and cost impact visible by role."
