# ADR 0001: Stack tecnológico para ComaDash

## Estado

Aceptado

## Fecha

2026-05-28

## Contexto

ComaDash es un prototipo de monitoreo predictivo para COMASA orientado a integrar datos operacionales IT/OT, simular señales industriales, detectar riesgos de falla y visualizar decisiones de mantenimiento y operación en tiempo casi real.

El sistema debe demostrar una cadena completa de valor:

1. Generar o recibir telemetría industrial con estructura tipo Unified Namespace.
2. Transportar eventos de proceso desacoplados de los consumidores.
3. Persistir series temporales y eventos derivados.
4. Ejecutar analítica simple pero explicable para anomalías, riesgo de activos, recomendaciones y KPIs.
5. Exponer dashboards operacionales, de mantenimiento, ejecutivos y de revisión por problema.

Para esta etapa, el foco no es desplegar una plataforma industrial productiva completa, sino validar un flujo funcional, demostrable y extensible hacia una arquitectura real con sensores, PLC/SCADA, Kepserver, OPC UA, edge gateway y prácticas de ciberseguridad IT/OT.

## Decisión

Se adopta el siguiente stack tecnológico base:

| Capa | Tecnología | Uso en el proyecto |
|---|---|---|
| Contenedores | Docker Compose | Orquestación local reproducible del prototipo |
| Simulación OT | Python 3.11 | Digital twin y generación de escenarios de falla |
| Mensajería | MQTT con Eclipse Mosquitto 2 | Broker Pub/Sub para telemetría bajo namespace `COMASA/#` |
| Ingesta | Telegraf 1.30 | Consumo MQTT y escritura de telemetría cruda en InfluxDB |
| Base de datos temporal | InfluxDB 2.7 | Almacenamiento de series temporales, KPIs, anomalías y recomendaciones |
| Analítica | Python 3.11 | Consumer de reglas, scoring de riesgo, FFT simple, eventos y recomendaciones |
| Visualización | Grafana 11 | Dashboards operacionales, mantenimiento predictivo, finanzas y revisión integrada |
| Librerías Python | `paho-mqtt`, `influxdb-client`, `numpy`, `pandas`, `scipy`, `python-dotenv`, `typer` | Publicación/consumo MQTT, escritura en InfluxDB, cálculos numéricos y configuración |

El flujo principal queda definido así:

```text
Python simulator
  -> MQTT / Mosquitto
  -> Telegraf
  -> InfluxDB
  -> Python analytics worker
  -> InfluxDB derived measurements
  -> Grafana dashboards
```

Mediciones principales en InfluxDB:

| Measurement | Propósito |
|---|---|
| `telemetry_raw` | Señales crudas de proceso ingeridas desde MQTT |
| `segment_status` | Estado analítico de tramos de agua, vapor, condensado y otras señales contextualizadas |
| `asset_risk` | Riesgo actual por equipo, causa probable y acción recomendada |
| `anomaly_event` | Eventos de anomalía detectados por reglas/analítica |
| `maintenance_recommendation` | Recomendaciones accionables de mantenimiento preventivo |
| `kpi` | Indicadores operacionales y económicos derivados |

## Justificación

### MQTT y Mosquitto

MQTT permite desacoplar fuentes de datos y consumidores. Para un contexto IT/OT, esto es útil porque evita conectar dashboards o analítica directamente a equipos de control. Mosquitto es liviano, simple de operar y suficiente para el prototipo.

La estructura de tópicos `COMASA/Lautaro/Planta1/...` acerca el diseño a un Unified Namespace, lo que facilita ordenar variables por sitio, planta, área, equipo y variable.

### Telegraf

Telegraf reduce código propio en la ingesta. Consume `COMASA/#`, interpreta JSON y escribe en InfluxDB con tags relevantes como `site`, `plant`, `area`, `equipment`, `variable`, `unit`, `quality`, `scenario` y `source`.

Esto deja al código Python enfocado en simulación y analítica, no en tareas repetitivas de ETL.

### InfluxDB

InfluxDB calza con el dominio porque la mayor parte del dato es temporal: sensores, KPIs, eventos de anomalía y evolución de riesgos. Frente a una base relacional tradicional, simplifica consultas por ventana de tiempo, últimos valores, tendencias y visualización con Grafana.

### Python

Python se usa tanto para el simulador como para el worker analítico porque permite desarrollar rápido, expresar reglas de negocio de forma clara y usar librerías conocidas para cálculo numérico. En esta etapa se prioriza explicabilidad sobre modelos complejos: reglas, scoring, tendencias y FFT simple son más defendibles para un prototipo de mantenimiento predictivo.

### Grafana

Grafana es la herramienta principal de visualización porque es fuerte en monitoreo operacional, series temporales, paneles en tiempo real y alertas. Además, su provisioning por archivos permite versionar dashboards JSON junto al repositorio.

### Docker Compose

Docker Compose permite levantar el stack completo con un comando, manteniendo bajo el costo de instalación y reduciendo diferencias entre equipos de desarrollo o demostración.

## Alternativas consideradas

| Alternativa | Motivo para no seleccionarla como núcleo |
|---|---|
| Power BI | Bueno para gerencia y reportabilidad, pero menos adecuado como núcleo de monitoreo industrial en tiempo real |
| Looker Studio | Simple para dashboards web, pero débil para integración OT, series temporales y operación en vivo |
| ThingsBoard | Potente para IoT, pero más pesado para el alcance del prototipo y menos flexible para analítica Python propia |
| TimescaleDB | Sólido para series temporales con SQL, pero requiere más diseño inicial que InfluxDB para este caso |
| Kafka | Robusto para streaming, pero sobredimensionado para un prototipo local y para el volumen esperado en la demo |

## Consecuencias

### Positivas

1. El prototipo es reproducible localmente con `docker compose up -d`.
2. La arquitectura separa simulación, mensajería, ingesta, persistencia, analítica y visualización.
3. El diseño es coherente con una evolución industrial hacia OPC UA, Kepserver, edge gateways y Sparkplug B.
4. Grafana e InfluxDB permiten inspeccionar rápidamente señales crudas y datos derivados.
5. Python mantiene bajo el costo de implementar nuevas reglas, escenarios y KPIs.

### Negativas o riesgos

1. Docker Compose no reemplaza una plataforma productiva con alta disponibilidad, backups, observabilidad y control de despliegues.
2. Mosquitto está configurado para demo local; producción requeriría usuarios, TLS, ACLs y segmentación de red.
3. InfluxDB necesita políticas de retención, estrategia de buckets y respaldo antes de usarse con datos productivos.
4. Las reglas de analítica son explicables pero no equivalen a un modelo predictivo validado con histórico real.
5. Grafana es muy fuerte operacionalmente, pero reportes ejecutivos formales podrían requerir BI complementario.

## Implicaciones para producción

Para industrializar esta decisión se deben agregar, como mínimo:

1. Integración con fuentes reales OT mediante Kepserver, OPC UA, base operacional o gateway de borde.
2. Seguridad MQTT con TLS, usuarios, contraseñas, ACLs y separación de redes IT/OT.
3. Gestión de secretos fuera del repositorio y rotación de credenciales.
4. Retención y respaldo de InfluxDB según criticidad de datos.
5. Dashboards y alertas con responsables, severidades y runbooks operacionales.
6. Validación de reglas/modelos con histórico real de fallas, mantenimiento y producción.

## Decisión final

Se mantiene `Python + MQTT/Mosquitto + Telegraf + InfluxDB + Grafana + Docker Compose` como stack oficial del prototipo ComaDash.

La decisión privilegia velocidad de demostración, trazabilidad técnica, monitoreo en tiempo real y evolución razonable hacia una arquitectura IT/OT productiva.
