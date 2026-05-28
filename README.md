# ComaDash

ComaDash es un prototipo local para monitoreo predictivo energetico de COMASA. Simula telemetria industrial de una planta, la publica por MQTT usando una estructura tipo Unified Namespace, persiste senales crudas y datos derivados en InfluxDB, y las visualiza en dashboards Grafana orientados a operacion, mantenimiento y finanzas.

El objetivo del proyecto no es solo mostrar graficos: es demostrar una cadena completa de decision operacional.

```text
Simulador Python
  -> MQTT / Mosquitto
  -> Telegraf
  -> InfluxDB
  -> Analytics Worker
  -> Grafana
```

## Contexto

Este repositorio corresponde a un prototipo de hackaton para abordar problemas de monitoreo industrial, fragmentacion de datos OT/IT, reportabilidad en tiempo real y mantenimiento predictivo en COMASA.

La solucion implementa un gemelo digital simplificado que genera variables operacionales de una planta de biomasa, incluyendo caldera, combustion, generacion, turbina, agua, vapor y condensado.

El sistema permite simular operacion normal y fallas para observar:

- Telemetria industrial en tiempo real.
- Riesgos por activo.
- Anomalias detectadas.
- Recomendaciones de mantenimiento.
- KPIs operacionales y financieros.
- Trazabilidad de TAGs del circuito agua-vapor-condensado.
- Impacto estimado en eficiencia, costo y disponibilidad.

## Stack Tecnico

- Python 3.11
- Docker Compose
- Mosquitto MQTT
- Telegraf
- InfluxDB 2.7
- Grafana 11
- `paho-mqtt`
- `influxdb-client`
- `numpy`
- `pandas`
- `scipy`

## Servicios

| Servicio | Rol | URL / Puerto |
|---|---|---|
| Mosquitto | Broker MQTT | `localhost:1883` |
| InfluxDB | Base de datos de series temporales | <http://localhost:8086> |
| Telegraf | Ingesta MQTT hacia InfluxDB | Interno |
| Grafana | Visualizacion y dashboards | <http://localhost:3000> |
| Simulator | Gemelo digital Python | Interno |
| Analytics | Motor de KPIs, riesgos y anomalias | Interno |

## Estructura del Repositorio

```text
.
|-- analytics/                 # Worker Python de analitica, KPIs, riesgos y recomendaciones
|-- docs/                      # Documentacion tecnica, arquitectura y guia de demo
|-- grafana/
|   |-- dashboards/            # Dashboards provisionados en Grafana
|   `-- provisioning/          # Datasource y configuracion de dashboards
|-- info/                      # Material de referencia del desafio COMASA
|-- mqtt/config/               # Configuracion de Mosquitto
|-- scripts/                   # Scripts auxiliares y smoke test
|-- simulator/                 # Gemelo digital y publicador MQTT
|-- telegraf/                  # Configuracion de ingesta MQTT -> InfluxDB
|-- docker-compose.yml
|-- .env.example
`-- README.md
```

## Flujo de Datos

1. El simulador Python genera senales industriales.
2. Cada senal se publica en MQTT bajo el prefijo `COMASA/Lautaro/Planta1`.
3. Telegraf consume `COMASA/#` y guarda los datos crudos en InfluxDB como `telemetry_raw`.
4. El worker de analitica tambien consume MQTT.
5. La analitica calcula KPIs, riesgos, anomalias, recomendaciones y estado de segmentos.
6. Los resultados derivados se escriben en InfluxDB.
7. Grafana consulta InfluxDB y muestra dashboards por rol y por problema.

## Refinamiento del Proyecto

El proyecto paso por un refinamiento progresivo para evitar quedar como un dashboard generico de variables aisladas. La direccion final fue transformar datos industriales simulados y referencias de TAGs reales en una herramienta de diagnostico operacional.

La evolucion principal fue:

1. **Base inicial: monitoreo en tiempo real.**
   Se implemento un flujo funcional con simulador Python, MQTT, Telegraf, InfluxDB y Grafana para demostrar telemetria viva.

2. **Separacion operacion-finanzas.**
   Se distinguieron vistas para operador, mantenimiento y jefatura/finanzas, porque cada perfil toma decisiones distintas.

3. **Analitica antes de la visualizacion.**
   El dashboard no calcula toda la decision por si solo. El worker de analitica genera KPIs, riesgos, anomalias, recomendaciones y estado de segmentos antes de que Grafana los consulte.

4. **Unidad de analisis: tramo operacional.**
   El refinamiento mas importante fue dejar de mirar solo variables como flujo, presion o temperatura, y representar tramos del proceso agua-vapor-condensado como entidades consultables.

   ```text
   Desde -> Hasta + Fluido + Unidad + Condicion + Variable + TAG + Medicion
   ```

5. **Trazabilidad con TAGs del XLSX.**
   El archivo `info/Agua, Vapor y Condensado Planta COMASA.xlsx` se uso como referencia para conservar estructura operacional, origen/destino, fluido, unidad, medicion y TAGs como `FT_5001`, `FT_2101-1`, `FT_5101-1`, `TIC_5101-1` y `FT_3001`.

6. **Ranking de decision por segmento.**
   Se agrego la medicion derivada `segment_status`, que permite responder que tramo revisar primero, por que, con que calidad de dato, que accion tomar y cual es el impacto operativo/costo.

7. **Refinamiento GQM.**
   Se aplico el enfoque Goal-Question-Metric para que cada panel tenga una justificacion clara:

   ```text
   Dolor -> Goal -> Question -> Metric -> Panel -> Decision -> Accion
   ```

8. **Narrativa de demo compacta.**
   Se agregaron dashboards `GQM - ...`, especialmente `GQM - COMASA Decision Narrative`, para contar la historia completa en pocos minutos: tramo critico, causa, evidencia, costo, biomasa, accion recomendada y cierre ejecutivo.

Este refinamiento alinea el prototipo con las bases de la hackaton y la presentacion del desafio: reportabilidad en tiempo real, integracion OT/IT, analitica avanzada, prediccion de fallas, seguridad, escalabilidad y compatibilidad futura con infraestructura industrial.

## Preguntas que Responde

El prototipo refinado esta disenado para responder preguntas operacionales concretas:

- Que tramo agua-vapor-condensado requiere atencion primero.
- Donde podria estar ocurriendo una perdida de condensado, vapor o eficiencia termica.
- Como se relacionan humedad de biomasa, consumo y potencia generada.
- Que activo presenta mayor riesgo operacional o de mantenimiento.
- Que anomalia fue detectada y cual es su causa probable.
- Que accion preventiva se recomienda y con que impacto esperado.
- Como se traduce una desviacion tecnica en costo, OEE o eficiencia energetica.

## Alcance Actual y Roadmap

El alcance actual es un prototipo funcional de baja fidelidad para demo. Usa datos simulados, reglas explicables y referencias del XLSX para demostrar la arquitectura y la logica de decision.

Implementado actualmente:

- Simulador Python con escenarios de falla.
- Publicacion MQTT en estructura tipo UNS.
- Ingesta cruda con Telegraf hacia `telemetry_raw`.
- Worker de analitica con KPIs, riesgos, anomalias, recomendaciones y `segment_status`.
- Dashboards Grafana originales y dashboards GQM aditivos.
- Ruta de demo compacta para pitch.

Roadmap natural hacia produccion:

- Sustituir simulador por datos reales exportados desde base operacional, SCADA, Kepserver u OPC UA.
- Incorporar Sparkplug B o contratos de payload industriales mas estrictos.
- Integrar historicos reales, turnos, operadores, setpoints, alarmas e intervenciones.
- Validar costos y KPIs con valores oficiales de COMASA.
- Evolucionar desde reglas explicables hacia modelos predictivos entrenados con historico real.
- Agregar metricas de calidad de datos y medicion de impacto antes/despues.

## Mediciones en InfluxDB

| Measurement | Descripcion |
|---|---|
| `telemetry_raw` | Senales crudas publicadas por el simulador |
| `kpi` | KPIs operacionales y financieros derivados |
| `asset_risk` | Ranking de riesgo por equipo o sistema |
| `segment_status` | Estado de tramos agua-vapor-condensado |
| `anomaly_event` | Eventos de anomalia detectados |
| `maintenance_recommendation` | Recomendaciones de mantenimiento preventivo |

## Requisitos

- Docker
- Docker Compose
- PowerShell si se desea ejecutar `scripts/smoke.ps1`

## Puesta en Marcha

Crear el archivo de entorno local:

```bash
cp .env.example .env
```

Levantar todos los servicios:

```bash
docker compose up -d
```

URLs utiles:

- Grafana: <http://localhost:3000> (`admin` / `admin` por defecto)
- InfluxDB: <http://localhost:8086>
- MQTT: `localhost:1883`

## Escenarios de Simulacion

El simulador soporta los siguientes escenarios:

| Escenario | Descripcion |
|---|---|
| `normal` | Operacion base sin falla inducida |
| `fouling_caldera` | Ensuciamiento de caldera, mayor temperatura de escape y presion diferencial |
| `humedad_biomasa_alta` | Biomasa humeda, mayor consumo y menor potencia |
| `perdida_vapor_condensado` | Perdida de vapor o condensado, menor recuperacion y mayor costo termico |
| `desbalance_turbina` | Vibracion elevada en turbina |
| `cavitacion_bomba` | Senal mecanica e hidraulica compatible con cavitacion |
| `combustion_inestable` | CO elevado, O2 inestable y combustion deficiente |

Para ejecutar un escenario:

```bash
SIM_SCENARIO=perdida_vapor_condensado docker compose up -d --force-recreate simulator
```

Tambien se puede editar `.env`:

```env
SIM_SCENARIO=normal
SIM_INTERVAL_SECONDS=2
```

Luego reiniciar el simulador:

```bash
docker compose up -d --force-recreate simulator
```

## Dashboards Grafana

Grafana carga automaticamente dashboards en la carpeta `COMASA`.

| Dashboard | Uso |
|---|---|
| `GQM - COMASA Decision Narrative` | Ruta compacta recomendada para demo |
| `COMASA - Revision integrada por problema` | Vista problem-first para priorizar tramos y acciones |
| `COMASA - Agua, vapor y condensado` | Diagnostico del circuito termico con TAGs |
| `COMASA - Centro de decision operacional` | Vista general de operacion |
| `COMASA - Vista operador de turno` | Vista operacional inmediata |
| `COMASA - Mantenimiento predictivo y riesgo de falla` | Riesgo, anomalias y backlog preventivo |
| `COMASA - Caldera y biomasa` | Diagnostico de caldera, combustion y biomasa |
| `COMASA - Vista ejecutiva y finanzas` | KPIs, OEE, costos y eficiencia |

Ruta recomendada para demo corta:

1. Abrir `GQM - COMASA Decision Narrative`.
2. Mostrar el tramo critico actual.
3. Revisar el ranking de tramos con causa, calidad y accion.
4. Conectar eficiencia agua-vapor-condensado con costo.
5. Mostrar impacto de biomasa en consumo y potencia.
6. Cerrar con OEE, energia generada y costo operacional estimado.

Para la demo `perdida_vapor_condensado`, abrir `COMASA - Revision integrada por problema` y revisar la primera fila del ranking de segmentos. Esa fila identifica el tramo agua-vapor-condensado critico con nodos origen/destino, TAG, calidad, razon de riesgo, accion recomendada e impacto costo/eficiencia.

## Inspeccionar MQTT

Ver mensajes publicados por el simulador:

```bash
docker compose exec mosquitto mosquitto_sub -t 'COMASA/#' -v
```

Ejemplo de topico:

```text
COMASA/Lautaro/Planta1/VaporSobrecalentado/Caldera/FT_5101-1/Flujo
```

Ejemplo de payload:

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
  "scenario": "normal"
}
```

## Consultar Datos en InfluxDB

Datos crudos:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="telemetry_raw") |> limit(n:20)' --org comasa --token comasa-demo-token
```

Datos derivados:

```bash
docker compose exec influxdb influx query 'from(bucket:"comasa") |> range(start:-10m) |> filter(fn:(r)=>r._measurement=="anomaly_event" or r._measurement=="maintenance_recommendation" or r._measurement=="asset_risk" or r._measurement=="kpi" or r._measurement=="segment_status")' --org comasa --token comasa-demo-token
```

## Smoke Test

Con los servicios levantados, ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke.ps1
```

El script verifica:

- Estado de Docker Compose.
- Salud de Grafana.
- Mediciones disponibles en InfluxDB.
- Existencia de datos recientes en mediciones clave.

## Reiniciar Demo desde Cero

Para eliminar volumenes y datos generados:

```bash
docker compose down -v
docker compose up -d
```

## Variables de Entorno Principales

| Variable | Descripcion |
|---|---|
| `COMASA_MQTT_HOST` | Host MQTT |
| `COMASA_MQTT_PORT` | Puerto MQTT |
| `COMASA_MQTT_TOPIC_PREFIX` | Prefijo de topicos publicados |
| `SIM_SCENARIO` | Escenario de simulacion |
| `SIM_INTERVAL_SECONDS` | Intervalo de publicacion del simulador |
| `INFLUXDB_URL` | URL de InfluxDB |
| `INFLUXDB_ORG` | Organizacion InfluxDB |
| `INFLUXDB_BUCKET` | Bucket de datos |
| `INFLUXDB_ADMIN_TOKEN` | Token de acceso |
| `GRAFANA_ADMIN_USER` | Usuario administrador Grafana |
| `GRAFANA_ADMIN_PASSWORD` | Password administrador Grafana |
| `COST_BIOMASS_PER_TON` | Costo demo por tonelada de biomasa |
| `COST_WATER_PER_M3` | Costo demo por m3 de agua |
| `COST_VAPOR_LOSS_PER_TON` | Costo demo por tonelada de vapor perdido |
| `CONDENSATE_RECOVERY_BENEFIT_PER_TON` | Beneficio demo por recuperacion de condensado |
| `POWER_NOMINAL_MW` | Potencia nominal usada para KPIs |

## Notas Importantes

- Los costos configurados son constantes de demostracion, no valores financieros oficiales de COMASA.
- El simulador es un gemelo digital de baja fidelidad pensado para demostrar flujo, arquitectura y toma de decision.
- El archivo XLSX de agua, vapor y condensado se usa como referencia de TAGs, variables y estructura operacional, no como pipeline automatico de ingesta.
- La solucion esta disenada para hackaton, pero la arquitectura puede evolucionar hacia integracion industrial con OPC UA, Kepserver, Edge Gateway, Sparkplug B y modelos predictivos mas avanzados.

## Documentacion Adicional

- `docs/architecture.md`: arquitectura tecnica e industrial.
- `docs/project_context_code_data_paths.md`: mapa de codigo y rutas de datos.
- `docs/demo.md`: runbook de demo.
- `docs/dashboard_panel_guide.md`: guia de dashboards y narrativa de pitch.
- `docs/gqm_dashboard_implementation.md`: implementacion de dashboards GQM.
- `info/`: documentos de referencia del desafio COMASA.

## Licencia

MIT.
