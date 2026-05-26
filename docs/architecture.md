# Arquitectura Técnica — COMASA Energía Predictiva 2026

**Fase:** Planificación y Diseño de Arquitectura IT/OT  
**Dominio:** Arquitectura industrial · Stack técnico · Modelo de datos · Gemelo digital · Monitoreo predictivo

---

## Verificación de fuentes

Esta propuesta fue contrastada contra los documentos locales del proyecto, ubicados en `info/`:

- `info/Bases Hackatón FICA 2026 1S (1).pdf`
- `info/4. Presentación Desafío COMASA.pdf`
- `info/Hackatón COMASA_ Análisis y Propuesta.pdf`
- FAQ COMASA-UFRO actualizado al `25/05/2026`
- `info/Preguntas Frecuentes Hackatón COMASA-UFRO.pdf`
- `info/Agua, Vapor y Condensado Planta COMASA.xlsx`
- `info/nota de audio.txt`

Los documentos respaldan los siguientes puntos:

- fragmentación de información crítica entre sistemas OT e IT;
- necesidad de reportabilidad y analítica en tiempo real;
- predicción de fallas y mantenimiento proactivo;
- monitoreo de variables como temperatura, vibración, presión, consumo energético, combustible/biomasa, agua y vapor;
- requisitos de confiabilidad, ciberseguridad, escalabilidad y compatibilidad con infraestructura existente;
- posibilidad de usar herramientas como Power BI, Grafana, bases de series temporales, Looker Studio y ThingsBoard;
- enfoque de prototipo funcional de baja fidelidad para hackatón.

El FAQ nuevo agrega una precisión importante para la arquitectura productiva: COMASA ya utiliza sensores industriales con tecnologías `fieldbus`, `HART`, `Ethernet` y otras; sus sistemas están en proceso de actualización, por lo que **no se debe asumir tecnología antigua ni una planta que parte desde cero**. La integración es viable mediante conectores como `Kepserver`; las variables pueden exportarse desde una `base de datos` y ser consumidas por otros servicios según el reporte requerido. El objetivo técnico declarado es unificar la red TI con la información de la red OT para gestión.

KPIs explícitos a cubrir desde la presentación del desafío:

- energía generada;
- throughput de biomasa;
- energía por tonelada de biomasa;
- OEE;
- MTBF;
- MTTR;
- horas de detención no programada.

Además, la retroalimentación docente incorporada a esta versión enfatiza tres ajustes de diseño: usar un simulador que publique datos directamente al broker para probar el flujo completo desde el inicio, separar la visualización operacional de la financiera y adelantar el motor de reglas/anomalías para que la visualización consuma eventos, recomendaciones y KPIs ya procesados, no solo señales crudas.

> **Nota de cautela:** datos como `25 MW` o `85.000 m³/mes de biomasa` aparecen en el documento de análisis, pero no quedaron confirmados por las bases ni por la presentación oficial extraída. No deberían tratarse como dato oficial sin validación adicional.

### Hallazgos del XLSX de agua, vapor y condensado

El archivo `info/Agua, Vapor y Condensado Planta COMASA.xlsx` contiene hojas por unidad generadora y régimen de operación: `UG_1_MT`, `UG_1_BL1`, `UG_1_BL2`, `UG_2_MT`, `UG_2_BL1`, `UG_2_BL2`, más una hoja resumen `Hoja1`. Las hojas operativas usan una estructura tabular con columnas `Desde`, `Hasta`, `Variable`, `Variable de medición`, `U. de medida`, `Medición`, `TAG` y, en varios casos, una nota de etapa.

La estructura observada fortalece directamente el modelo de gasto operacional porque no solo hay señales genéricas: hay trazabilidad de circuitos y TAGs reales para agua, vapor y condensado. Las variables disponibles incluyen `Agua Industrial`, `Agua Desmineralizada`, `Agua Alimentación`, `Agua Refrigeración`, `Condensado`, `Vapor Saturado` y `Vapor Sobrecalentado`. Las mediciones incluyen `Flujo`, `Presión`, `Nivel`, `Carga`, `Temperatura`, `Presion de descarga bomba` y `Revolución`, con unidades como `m3/h`, `ton/h`, `bar`, `%`, `A`, `°C`, `rpm`, `ppm` y `mmH2C`.

Ejemplos de TAGs reales encontrados: `FT_5001`, `FT_5002`, `FT_4002`, `FT_4502`, `FT_5003`, `FE-48`, `FE-14`, `FT-5007`, `FT_2101-1`, `FIC_2103-1`, `TIC_5101-1`, `FT_3001`, `FT-4040-814`, `TT_3104-1`, `PT_3101-1`, `FT_5101-1`, `TT_5101-1` y `PT_5101-1`. No se calculan promedios ni totales en esta propuesta; los valores del XLSX se usan como referencia de estructura, variables, unidades y puntos de medición.

---

## 1. Resumen ejecutivo

La arquitectura recomendada para COMASA debe resolver un problema de fondo: **la planta no necesita solo gráficos; necesita una arquitectura IT/OT que convierta datos industriales fragmentados en decisiones operacionales y económicas**.

Para la hackatón, la mejor solución es:

> **Python Digital Twin + MQTT / UNS + InfluxDB + Grafana + Telegraf + alertas predictivas simples**

Para producción, debe evolucionar hacia:

> **Sensores fieldbus/HART/Ethernet + PLC/SCADA/base de datos/Kepserver → Edge Gateway / OPC UA → MQTT Sparkplug B / UNS → InfluxDB/Data Lake → Analítica predictiva → Grafana/BI ejecutivo**

Esto permite demostrar:

- monitoreo operacional en tiempo real;
- detección temprana de anomalías;
- mantenimiento predictivo con recordatorios y sugerencias accionables de mantención;
- simulación de fallas;
- impacto en energía generada, throughput de biomasa, energía por tonelada de biomasa, OEE, MTBF, MTTR, horas de detención no programada, consumo de combustible/biomasa, agua, vapor y riesgo de detención;
- evolución realista hacia infraestructura industrial.

---

## 2. Arquitectura recomendada

| Capa | Componente | Función | Justificación |
|---|---|---|---|
| OT | Sensores fieldbus, HART, Ethernet, PLC, SCADA y base de datos operacional | Fuente de temperatura, presión, vibración, energía, estados ON/OFF, agua, vapor, condensado y TAGs de proceso | Es donde nace el problema operacional; el FAQ confirma que existen sensores y sistemas actualizándose, no una planta desde cero |
| Edge | Simulador Python en hackatón / Kepserver, OPC UA o Edge Gateway en producción | Normaliza y publica datos exportables desde OT o base de datos | Desacopla OT de IT, permite consumir variables existentes y evita exponer control industrial |
| Mensajería | MQTT + UNS | Bus industrial Pub/Sub | Reduce fragmentación y permite interoperabilidad |
| Estandarización futura | Sparkplug B | Modelo payload industrial | Útil en producción para estado, birth/death certificates y estructura |
| Ingesta | Telegraf | Consume MQTT y escribe en InfluxDB | Rápido, probado y configurable |
| Series temporales | InfluxDB | Guarda lecturas industriales | Mejor que SQL tradicional para señales continuas |
| Analítica temprana | Python consumer / motor de reglas | Reglas, z-score, tendencias, FFT, cálculo de KPIs y recomendaciones | Debe ejecutarse antes de la visualización final para que Grafana muestre decisiones, no solo datos crudos |
| Visualización operacional | Grafana | Tiempo real, alarmas, tendencias y recomendaciones de mantención | Superior para monitoreo industrial |
| Reportabilidad ejecutiva | Grafana ejecutivo / Power BI futuro | KPIs financieros, operacionales y gastos por combustible/biomasa, agua y vapor | Gerencia necesita impacto económico, no solo señales |
| Seguridad | TLS, usuarios MQTT, segmentación, DMZ, ISA/IEC 62443 | Protección IT/OT | La solución debe ser industrializable |

Arquitectura lógica:

```text
Sensores fieldbus / HART / Ethernet / PLC / SCADA / base de datos OT
        ↓
Kepserver / OPC UA / Simulador Python
        ↓
Edge Gateway / Digital Twin
        ↓
MQTT Broker + Unified Namespace
        ↓
Telegraf / Python Consumer
        ↓
InfluxDB
        ↓
Motor de anomalías + alertas
        ↓
Grafana Operacional
        ↓
Dashboard Ejecutivo / KPIs / impacto económico
```

El motor de reglas debe ejecutarse inmediatamente después de la ingesta/persistencia —o en paralelo mediante un consumidor MQTT propio— para publicar anomalías, recomendaciones y KPIs derivados antes de que los dashboards finales consulten la información. Esto corrige el riesgo de tener un dashboard meramente reactivo: la visualización debe mostrar señales procesadas, alertas y acciones sugeridas.

---

## 3. Comparación de alternativas

| Alternativa | Ventajas | Desventajas | Hackatón | Escalabilidad industrial | Tiempo real | Reportabilidad ejecutiva |
|---|---|---|---|---|---|---|
| Power BI | Excelente para gerencia, KPIs y análisis financiero | Débil para alta frecuencia y monitoreo industrial vivo | Alta | Media | Baja/media | Excelente |
| Grafana + InfluxDB | Muy fuerte en series temporales, alertas y tiempo real | Menos natural para reportes corporativos paginados | Alta | Alta | Alta | Media |
| Looker Studio | Simple, rápido, web | Poco industrial, débil para OT/SCADA | Alta | Baja/media | Baja | Buena |
| ThingsBoard | IoT nativo, MQTT, widgets, reglas | Más pesado y menos flexible para ciencia de datos | Media | Alta | Alta | Media |
| TimescaleDB + Grafana | SQL + series temporales, robusto | Más trabajo inicial que InfluxDB | Media | Alta | Alta | Buena |

**Decisión:** Grafana + InfluxDB gana para la hackatón porque el problema central es monitoreo industrial en tiempo real, no solo reporting ejecutivo.

Power BI puede quedar como evolución para gerencia, pero no como núcleo operacional.

---

## 4. Stack técnico final

| Necesidad | Stack recomendado |
|---|---|
| Lenguaje principal | Python 3.11+ |
| Broker MQTT | Mosquitto |
| Base temporal | InfluxDB |
| Ingesta | Telegraf |
| Visualización | Grafana |
| Alertas | Grafana Alerting + eventos MQTT |
| Simulador | Python digital twin |
| Infraestructura | Docker Compose local |
| Librerías Python | `paho-mqtt`, `numpy`, `pandas`, `scipy`, `influxdb-client`, `python-dotenv`, `typer`, opcional `scikit-learn` |

Este stack es superior para este contexto porque:

- es prototipable en pocos días;
- usa herramientas reales de monitoreo industrial;
- evita Excel y dashboards estáticos;
- soporta tiempo real;
- escala naturalmente hacia OPC UA, Edge Gateway y Sparkplug B;
- permite explicar valor técnico y económico al jurado.

---

## 5. Diseño del Espacio de Nombres Unificado

Estructura base:

```text
COMASA/Lautaro/Planta1/{Area}/{Equipo}/{Variable}
```

Ejemplos:

```text
COMASA/Lautaro/Planta1/Caldera/Gases/TemperaturaEscape
COMASA/Lautaro/Planta1/Caldera/Gases/PresionDiferencial
COMASA/Lautaro/Planta1/Caldera/Combustion/HumedadBiomasa
COMASA/Lautaro/Planta1/Caldera/Combustion/ConsumoBiomasa
COMASA/Lautaro/Planta1/Caldera/Servicios/ConsumoAgua
COMASA/Lautaro/Planta1/Caldera/Servicios/FlujoVapor
COMASA/Lautaro/Planta1/AguaIndustrial/Captacion/FT_5001/Flujo
COMASA/Lautaro/Planta1/AguaDesmineralizada/Osmosis/FE-48/Flujo
COMASA/Lautaro/Planta1/AguaAlimentacion/ECOI/FT_2101-1/Flujo
COMASA/Lautaro/Planta1/VaporSobrecalentado/Caldera/FT_5101-1/Flujo
COMASA/Lautaro/Planta1/VaporSaturado/Domo/PT_3101-1/Presion
COMASA/Lautaro/Planta1/Condensado/Condensador/TIC_5101-1/Temperatura
COMASA/Lautaro/Planta1/Condensado/Retorno/FT_3001/Flujo
COMASA/Lautaro/Planta1/Caldera/Combustion/O2
COMASA/Lautaro/Planta1/Caldera/Combustion/CO
COMASA/Lautaro/Planta1/Generacion/Turbina/VibracionRMS
COMASA/Lautaro/Planta1/Generacion/Turbina/VibracionFFT
COMASA/Lautaro/Planta1/Generacion/Generador/PotenciaMW
COMASA/Lautaro/Planta1/KPI/EnergiaGenerada
COMASA/Lautaro/Planta1/KPI/ThroughputBiomasa
COMASA/Lautaro/Planta1/KPI/EnergiaEspecifica
COMASA/Lautaro/Planta1/KPI/CostoBiomasaPorMWh
COMASA/Lautaro/Planta1/KPI/AguaPorMWh
COMASA/Lautaro/Planta1/KPI/VaporPorMWh
COMASA/Lautaro/Planta1/KPI/CondensadoRecuperado
COMASA/Lautaro/Planta1/KPI/CostoAguaVaporCondensado
COMASA/Lautaro/Planta1/KPI/OEE
COMASA/Lautaro/Planta1/KPI/MTBF
COMASA/Lautaro/Planta1/KPI/MTTR
COMASA/Lautaro/Planta1/KPI/HorasDetencionNoProgramada
COMASA/Lautaro/Planta1/Alertas/RiesgoFalla
COMASA/Lautaro/Planta1/Recomendaciones/Mantencion
```

Payload recomendado:

```json
{
  "timestamp": "2026-05-25T15:04:05.123Z",
  "site": "Lautaro",
  "plant": "Planta1",
  "area": "Caldera",
  "equipment": "CalderaBiomasa01",
  "variable": "TemperaturaEscape",
  "value": 184.7,
  "unit": "°C",
  "quality": "GOOD",
  "source": "digital-twin",
  "scenario": "normal"
}
```

Esta estructura ayuda porque separa claramente:

- empresa;
- sitio;
- planta;
- área;
- equipo;
- variable.

Eso facilita mantenimiento, escalabilidad e integración futura con SCADA, OPC UA o BI.

Para las variables del XLSX conviene conservar el `TAG` original dentro del tópico o del payload. Esto permite mapear señales como `FT_5001`, `FT_2101-1`, `FT_5101-1` o `TIC_5101-1` contra su origen real sin perder la semántica industrial del circuito agua-vapor-condensado.

---

## 6. Modelo de datos industrial

| Entidad | Campos principales | Relación |
|---|---|---|
| Sensor | `sensor_id`, `equipment_id`, `variable_id`, `type`, `unit`, `sample_rate_hz`, `mqtt_topic`, `status` | Pertenece a un equipo y mide una variable |
| Equipo | `equipment_id`, `name`, `area`, `asset_type`, `criticality`, `parent_equipment_id` | Agrupa sensores |
| Variable operacional | `variable_id`, `name`, `unit`, `normal_min`, `normal_max`, `warning_threshold`, `critical_threshold` | Define límites y semántica |
| Lectura temporal | `time`, `sensor_id`, `equipment_id`, `variable_id`, `value`, `quality`, `scenario_id` | Serie temporal en InfluxDB |
| Alerta | `alert_id`, `time`, `equipment_id`, `severity`, `message`, `trigger_variable`, `ack_status` | Resultado de regla/anomalía |
| Anomalía | `anomaly_id`, `start_time`, `end_time`, `equipment_id`, `type`, `score`, `detector`, `probable_cause` | Evento detectado |
| Recomendación de mantención | `recommendation_id`, `time`, `equipment_id`, `severity`, `probable_cause`, `suggested_action`, `due_before`, `expected_impact` | Convierte anomalías en acciones preventivas |
| Evento mantenimiento | `maintenance_id`, `equipment_id`, `time`, `type`, `description`, `downtime_minutes`, `cost_estimate` | Conecta falla con mantenimiento |
| Consumo operacional | `time`, `equipment_id`, `resource`, `value`, `unit`, `unit_cost`, `cost_estimate` | Registra gasto de combustible/biomasa, agua y vapor |
| Circuito agua-vapor-condensado | `circuit_id`, `from_node`, `to_node`, `resource`, `measurement_type`, `unit`, `tag`, `source_sheet`, `operating_block` | Representa la estructura del XLSX: origen/destino, variable, medición, unidad, TAG y régimen operativo |
| KPI operacional | `kpi_id`, `name`, `period_start`, `period_end`, `value`, `unit`, `formula` | Vista ejecutiva |
| Simulación de falla | `scenario_id`, `name`, `affected_equipment_id`, `duration`, `variables_modified`, `expected_detection` | Controla el gemelo digital |

Ejemplo de sensor:

```json
{
  "sensor_id": "SEN-TURB-VIB-001",
  "equipment_id": "EQ-TURBINA-001",
  "variable_id": "VAR-VIB-RMS",
  "type": "vibration",
  "unit": "mm/s",
  "sample_rate_hz": 10,
  "mqtt_topic": "COMASA/Lautaro/Planta1/Generacion/Turbina/VibracionRMS",
  "status": "active"
}
```

Ejemplo de recomendación de mantención:

```json
{
  "recommendation_id": "REC-CALD-FOULING-001",
  "equipment_id": "EQ-CALDERA-001",
  "severity": "warning",
  "probable_cause": "Ensuciamiento progresivo por ceniza o escoria",
  "suggested_action": "Programar limpieza de superficie de intercambio y revisar calidad de biomasa",
  "due_before": "2026-05-26T08:00:00Z",
  "expected_impact": "Reducir consumo de biomasa por MWh y evitar caída de potencia"
}
```

Ejemplo de anomalía:

```json
{
  "anomaly_id": "ANOM-FOULING-001",
  "equipment_id": "EQ-CALDERA-001",
  "type": "fouling_caldera",
  "detector": "trend_zscore",
  "score": 0.87,
  "probable_cause": "Ensuciamiento progresivo por ceniza o escoria",
  "trigger_variables": [
    "TemperaturaEscape",
    "PresionDiferencial",
    "ConsumoBiomasa"
  ]
}
```

---

## 7. Variables y KPIs críticos

| Variable/KPI | Qué mide | Por qué importa | Cálculo | Anomalía anticipada |
|---|---|---|---|---|
| Temperatura gases escape | Calor perdido por chimenea | Detecta baja transferencia térmica | Sensor + tendencia | Fouling/slagging |
| Presión diferencial | Resistencia al paso de gases | Indica obstrucción o suciedad | Presión entrada - salida | Ensuciamiento |
| Humedad biomasa | Agua en combustible | Reduce poder calorífico | % humedad | Baja eficiencia |
| Consumo biomasa | Ton/h consumidas | Impacta costo y eficiencia | Flujo de biomasa | Mayor consumo sin más potencia |
| Throughput de biomasa | Ton/h procesadas por el sistema | KPI explícito del desafío; mide capacidad productiva y estabilidad de alimentación | `ton biomasa procesada / hora` | Alimentación irregular, cuello de botella o pérdida de continuidad operacional |
| Consumo agua | m³/h usados por proceso | Afecta gasto operacional y disponibilidad de servicios | Medidor de caudal + costo unitario | Fuga, purga excesiva, pérdida de eficiencia |
| Flujo/consumo vapor | Ton/h o kg/h de vapor | Relaciona generación térmica con eficiencia del ciclo | Caudalímetro de vapor / MWh | Pérdida térmica, válvula defectuosa, demanda anómala |
| Potencia generada | MW instantáneos | Resultado operacional inmediato | Medición eléctrica | Pérdida de rendimiento |
| Energía generada | MWh por periodo | KPI explícito del desafío; mide producción eléctrica acumulada | Integral de potencia en el tiempo: `Σ MW × Δt` | Menor producción por baja eficiencia o detenciones |
| Vibración turbina | RMS/espectro mecánico | Detecta desbalance/rodamientos | RMS + FFT | Desbalance, desalineación |
| Vibración bombas | Estado mecánico bombas | Detecta cavitación/falla mecánica | RMS + frecuencia | Cavitación |
| O₂ / CO | Calidad de combustión | Detecta combustión incompleta | Analizador gases | Aire mal regulado, CO alto |
| OEE | Efectividad global | Resume disponibilidad/rendimiento/calidad | Disponibilidad × rendimiento × calidad | Pérdida operacional |
| MTBF | Tiempo medio entre fallas | Mide confiabilidad | Tiempo operativo / fallas | Degradación de activos |
| MTTR | Tiempo medio de reparación | Mide mantenibilidad y rapidez de recuperación | Tiempo total de reparación / número de reparaciones | Reparaciones lentas, falta de repuestos o mala planificación |
| Horas de detención no programada | Tiempo improductivo no planificado | KPI explícito del desafío; conecta fallas con pérdida operacional | Suma de eventos no planificados en horas | Falla crítica, baja confiabilidad o mantenimiento reactivo |
| Energía específica | MWh por tonelada biomasa | Eficiencia energética/económica | MWh / ton biomasa | Ineficiencia térmica |
| Costo biomasa por MWh | Costo de combustible por energía generada | KPI financiero-operacional principal | `(ton biomasa × costo ton) / MWh` | Aumento de gasto sin aumento de producción |
| Agua por MWh | Eficiencia de uso de agua | Detecta gasto operacional anormal | `m³ agua / MWh` | Fuga, purga excesiva o mala operación |
| Vapor por MWh | Eficiencia térmica del ciclo | Evalúa cuánto vapor se requiere para producir energía | `ton vapor / MWh` | Pérdida térmica o bajo rendimiento de turbina |
| Condensado recuperado | Retorno útil al ciclo agua-vapor | Reduce reposición de agua, tratamiento químico y energía térmica requerida | `flujo condensado recuperado / flujo vapor o agua alimentación` | Pérdida de retorno, fuga, venteo o falla de trampa/válvula |
| Costo agua-vapor-condensado | Sobrecosto agregado del circuito térmico | Convierte flujos, presión, temperatura y recuperación de condensado en impacto económico | Agua de reposición + tratamiento + energía térmica asociada - beneficio por retorno de condensado | Gasto operacional oculto por baja recuperación o pérdidas térmicas |
| Costo operacional estimado | Gasto agregado por periodo | Traduce operación a impacto financiero | Biomasa + agua + vapor + energía auxiliar | Desviación presupuestaria operacional |

---

## 8. Gemelo digital simplificado

El gemelo digital debe simular comportamiento termodinámico y mecánico básico.

### Variables lentas

- temperatura de gases;
- presión diferencial;
- humedad de biomasa;
- flujo/consumo de biomasa;
- consumo de agua;
- flujo y presión de vapor;
- potencia generada;
- O₂ / CO.

### Variables rápidas

- vibración turbina;
- vibración bombas;
- ruido mecánico;
- armónicos;
- picos FFT;
- desbalance.

### Escenarios de falla

| Escenario | Efecto simulado |
|---|---|
| `fouling_caldera` | Sube temperatura de escape, sube presión diferencial, cae eficiencia |
| `humedad_biomasa_alta` | Sube consumo, baja potencia, baja energía específica |
| `consumo_agua_anomalo` | Sube m³/h sin justificación productiva, aumenta costo operacional |
| `perdida_vapor` | Sube vapor por MWh, baja eficiencia térmica y aumenta gasto operacional |
| `desbalance_turbina` | Sube vibración RMS, aparece pico 1X/2X |
| `cavitacion_bomba` | Aumenta vibración irregular y ruido de alta frecuencia |
| `combustion_inestable` | CO alto, O₂ inestable, potencia variable |

### Valor para la hackatón

- permite demostrar fallas sin acceso a planta real;
- conecta datos técnicos con impacto operacional;
- muestra una arquitectura completa de punta a punta;
- evita depender de Excel o datos estáticos.

---

## 9. Flujo principal del sistema

```text
Paso 1 -> Sensor real o virtual genera una lectura.
Paso 2 -> El dato se publica en un tópico MQTT.
Paso 3 -> Telegraf consume el mensaje desde el broker.
Paso 4 -> Telegraf transforma y escribe el dato en InfluxDB.
Paso 5 -> El motor de reglas/anomalías consume MQTT o consulta InfluxDB inmediatamente después de persistir.
Paso 6 -> El motor calcula anomalías, KPIs derivados y recomendaciones de mantención.
Paso 7 -> Se publican alertas preventivas y eventos accionables hacia InfluxDB/MQTT/Grafana Alerting.
Paso 8 -> Grafana operacional muestra variables, anomalías y acciones sugeridas.
Paso 9 -> El dashboard ejecutivo traduce rendimiento, consumo y anomalías a impacto operacional o financiero.
```

La lógica predictiva no debe quedar después del dashboard. Si el motor de reglas se ejecuta al final, el sistema solo visualiza y reacciona tarde. Ejecutarlo en el paso 5 permite que los dashboards reciban contexto: riesgo de falla, causa probable, costo asociado y recomendación concreta de mantención.

---

## 10. Dashboards

### Dashboard operacional

| Panel | Tipo | Objetivo |
|---|---|---|
| Estado de caldera | State timeline / gauge | Ver condición actual |
| Temperatura gases escape | Time series | Detectar drift térmico |
| Presión diferencial | Time series + threshold | Detectar obstrucción |
| Humedad biomasa | Gauge + tendencia | Explicar baja eficiencia |
| Consumo biomasa | Time series | Relacionar costo/producción |
| Consumo agua | Time series + umbral | Detectar gasto operacional anormal |
| Flujo de vapor | Time series + eficiencia | Relacionar generación térmica con potencia producida |
| Retorno de condensado | Time series + ratio | Detectar pérdida de recuperación y sobrecosto por reposición de agua/energía |
| Mapa agua-vapor-condensado por TAG | Sankey / node graph / table | Mostrar flujo desde `Desde` hacia `Hasta` usando TAGs reales del XLSX |
| Potencia generada | Time series | Ver impacto productivo |
| Vibración turbina | Time series alta frecuencia | Detectar desbalance |
| FFT vibración | Bar/heatmap | Mostrar componente predictiva |
| Alarmas activas | Table / alert list | Acción operacional |
| Recomendaciones de mantención | Table | Mostrar acción sugerida, prioridad y plazo |
| Timeline de anomalías | State timeline | Ver eventos por equipo |

### Dashboard estratégico

| Panel | Tipo | Objetivo |
|---|---|---|
| OEE | KPI card | Salud operacional global |
| Energía generada | KPI/line | Producción eléctrica acumulada por periodo |
| Throughput de biomasa | KPI/line | Capacidad de alimentación/procesamiento de biomasa |
| MTBF | KPI card | Confiabilidad |
| MTTR | KPI card | Mantenibilidad |
| Horas de detención no programada | KPI/bar | Impacto directo de fallas y eventos no planificados |
| Energía específica | Line/KPI | Eficiencia biomasa → electricidad |
| Costo biomasa por MWh | KPI/line | Gasto de combustible por energía producida |
| Agua por MWh | KPI/line | Eficiencia y gasto hídrico por producción |
| Vapor por MWh | KPI/line | Eficiencia térmica del ciclo |
| Condensado recuperado | KPI/line | Ahorro operacional por retorno al ciclo térmico |
| Costo agua-vapor-condensado | KPI/bar | Sobrecosto de agua, vapor y pérdidas de condensado |
| Costo operacional estimado | KPI/bar | Biomasa + agua + vapor por periodo |
| Pérdidas por baja eficiencia | Waterfall/bar | Impacto económico |
| Riesgo por equipo | Matrix | Priorizar mantenimiento |
| Alertas ejecutivas | Table | Resumen para jefatura |
| Normal vs falla simulada | Comparative chart | Demostrar valor del sistema |

### Consulta integrada operación-finanzas

Además de los dos dashboards, se recomienda una capa de consulta integrada que responda preguntas del tipo: **“la máquina 1 rinde tanto y gasta tanto”**. Esta vista cruza potencia, disponibilidad, biomasa, agua, vapor y alertas para demostrar si un equipo está operando dentro del flujo esperado o si está generando sobrecosto antes de fallar.

Con el XLSX, esa consulta puede bajar a nivel de circuito: por ejemplo, comparar agua industrial captada, agua desmineralizada producida, agua de alimentación hacia economizadores, vapor sobrecalentado generado y condensado retornado. Esa relación permite explicar gastos operacionales de agua/vapor/condensado con evidencia de TAGs y no solo con supuestos del gemelo digital.

### Priorización viable de indicadores para la hackatón

Para la hackatón, la forma más viable de permitir que cada usuario priorice indicadores es usar capacidades nativas de Grafana, no desarrollar un frontend propio. La propuesta es crear un **dashboard maestro** con todos los indicadores disponibles y, desde ahí, preparar vistas por rol:

- **Vista operador:** alarmas activas, riesgo de falla, variables críticas en tiempo real, recomendaciones de mantención.
- **Vista mantención:** MTBF, MTTR, vibración, anomalías por equipo, recomendaciones y plazo sugerido.
- **Vista jefatura/finanzas:** OEE, energía generada, biomasa/MWh, agua/MWh, vapor/MWh, condensado recuperado y costo operacional.

En Grafana, los paneles se pueden mover, redimensionar, duplicar y guardar como copias del dashboard. Eso permite que el operador acomode en pantalla los indicadores más importantes para su turno sin bloquear la demo ni aumentar demasiado el alcance técnico.

Para esta etapa, **no se recomienda construir una aplicación web personalizada de drag-and-drop**. Sería posible en una etapa futura usando la API de Grafana o un frontend propio, pero para tres días conviene priorizar una solución robusta, demostrable y alineada con el stack existente.

---

## 11. Motor de detección de anomalías

### Para la hackatón

Usar métodos interpretables:

| Método | Uso |
|---|---|
| Umbrales | Temperatura, presión, vibración, CO |
| Medias móviles | Suavizar ruido y detectar drift |
| Z-score | Detectar valores fuera de patrón normal |
| Tendencias | Pendientes sostenidas, no solo picos |
| FFT básica | Vibración turbina/bombas |
| Reglas de recomendación | Convertir anomalías en recordatorios o sugerencias de mantención |
| KPIs de costo | Biomasa/MWh, agua/MWh, vapor/MWh y costo operacional estimado |

Ejemplo:

```text
Si TemperaturaEscape sube durante 10 min
Y PresionDiferencial sube
Y PotenciaGenerada cae
=> Riesgo: fouling o pérdida de eficiencia térmica
=> Acción: recomendar limpieza de caldera antes del siguiente turno
=> Impacto: biomasa/MWh sube y aumenta costo operacional
```

Otro ejemplo orientado a gastos operacionales:

```text
Si ConsumoAgua sube sin aumento de PotenciaGenerada
O VaporPorMWh aumenta sobre su banda normal
=> Riesgo: fuga, purga excesiva o pérdida térmica
=> Acción: inspeccionar línea de vapor/agua y revisar válvulas críticas
=> Impacto: sobrecosto operacional por agua y vapor
```

Ejemplo específico del circuito agua-vapor-condensado:

```text
Si FlujoVaporSobrecalentado aumenta
Y CondensadoRecuperado no acompaña la tendencia esperada
Y AguaAlimentacion o AguaDesmineralizada sube
=> Riesgo: pérdida de condensado, venteo, fuga o trampa/válvula defectuosa
=> Acción: inspeccionar retorno de condensado y puntos críticos del circuito
=> Impacto: mayor costo operacional por reposición de agua, tratamiento y energía térmica
```

La salida del motor no debe limitarse a “alerta roja/amarilla”. Debe publicar un evento accionable con: equipo afectado, causa probable, prioridad, recomendación, plazo sugerido y KPI económico impactado. Esa diferencia es clave para pasar de monitoreo reactivo a mantenimiento predictivo defendible.

### Para producción

Evolución:

- Isolation Forest para anomalías multivariables;
- Random Forest/XGBoost si existen fallas etiquetadas;
- Autoencoders si hay mucho histórico normal;
- modelos de degradación por activo;
- MLOps con versionado, drift detection y reentrenamiento.

> En la hackatón no conviene vender “IA mágica”. Conviene vender **detección temprana explicable**. Es más creíble, más demostrable y más defendible ante jurado técnico.

---

## 12. Estructura de carpetas propuesta

```text
energia-predictiva-comasa/
├── docker-compose.yml
├── README.md
├── .env.example
├── mqtt/
│   └── config/
├── telegraf/
│   └── telegraf.conf
├── influxdb/
│   └── init/
├── grafana/
│   ├── dashboards/
│   └── provisioning/
├── simulator/
│   ├── main.py
│   ├── sensors/
│   ├── anomalies/
│   └── requirements.txt
├── analytics/
│   ├── anomaly_detection.py
│   ├── maintenance_recommendations.py
│   └── fft_analysis.py
└── docs/
    ├── architecture.md
    ├── pitch.md
    └── deployment_plan.md
```

Función:

- `mqtt/`: configuración de broker.
- `telegraf/`: puente MQTT → InfluxDB.
- `influxdb/`: inicialización de bucket, token y organización.
- `grafana/`: dashboards versionados.
- `simulator/`: gemelo digital y sensores sintéticos.
- `analytics/`: reglas, anomalías, recomendaciones de mantención, KPIs de costo y FFT.
- `docs/`: arquitectura, pitch y plan de despliegue.

---

## 13. Plan de ejecución hackatón

| Día | Objetivo | Tareas | Entregable | Riesgo | Mitigación |
|---|---|---|---|---|---|
| Día 1 | Entender problema y diseñar arquitectura | Variables críticas, UNS MQTT, modelo de datos, wireframes, narrativa IT/OT | Diagrama + tópicos + modelo | Programar sin entender el proceso | Arquitectura primero, código después |
| Día 2 | Construir demo end-to-end | Docker, Mosquitto, InfluxDB, Telegraf, simulador Python publicando al broker, primera anomalía y primera recomendación | Datos fluyendo MQTT → InfluxDB → motor de reglas → Grafana | Integración lenta | Reducir alcance a 6 variables, 2 anomalías y 1 recomendación de mantención |
| Día 3 | Visualizar, alertar y vender impacto | Dashboard operacional, dashboard financiero, consulta integrada, alertas, KPIs, pitch, demo grabada | Demo funcional + presentación | Falla en vivo | Video backup + capturas + datos precargados |

---

## 14. Riesgos técnicos y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Falla del demo en vivo | Alto | Demo grabada, screenshots, dataset precargado |
| Datos sintéticos poco realistas | Alto | Modelar relaciones causales: humedad ↑ → eficiencia ↓ → consumo ↑ |
| Dashboard sobrecargado | Medio/alto | Separar operacional y ejecutivo |
| Motor de reglas ejecutado demasiado tarde | Alto | Ejecutarlo inmediatamente después de ingesta/persistencia o en paralelo como consumidor MQTT |
| Mala estructura MQTT | Alto | Usar jerarquía Empresa/Sitio/Planta/Área/Equipo/Variable |
| Latencia o pérdida mensajes | Medio | QoS MQTT, timestamps, buffer, health checks |
| No conectar técnica con economía | Alto | Mostrar energía generada, throughput de biomasa, energía por tonelada, OEE, MTBF, MTTR, horas de detención no programada y costo estimado |
| Dificultad explicando IT/OT | Medio | Diagrama simple OT → Edge → MQTT → InfluxDB → Grafana |

---

## 15. Decisiones de diseño principales

1. **Grafana + InfluxDB sobre Power BI para monitoreo operacional**  
   Porque COMASA necesita tiempo real y series temporales, no solo reportes.

2. **MQTT + Unified Namespace como columna vertebral**  
   Porque ataca directamente la fragmentación OT/IT verificada en los PDFs.

3. **Python como gemelo digital de baja fidelidad**  
   Porque permite simular fallas, sensores y anomalías rápido.

4. **Separar dashboard operacional y ejecutivo**  
    Porque operadores y gerencia toman decisiones distintas.

5. **Permitir priorización de indicadores con dashboards Grafana por rol**  
   Porque todos los indicadores deben existir, pero operador, mantención y gerencia no necesitan verlos con la misma jerarquía. Para hackatón es más viable usar dashboard maestro, vistas por rol y copias editables que construir un frontend personalizado.

6. **Ejecutar el motor de reglas antes de la visualización final**  
   Porque el dashboard debe mostrar anomalías, recomendaciones y KPIs derivados ya procesados; si el análisis ocurre después, la solución queda reactiva y pierde valor predictivo.

7. **Incluir una capa de consulta integrada operación-finanzas**  
   Porque el feedback docente pidió mostrar rendimiento y gasto por máquina, conectando funcionamiento técnico con biomasa, agua, vapor y costo operacional.

8. **Diseñar desde el inicio la evolución OPC UA / Edge / Sparkplug B**  
   Porque la demo debe ser hackeable, pero la arquitectura debe ser industrializable.

---

## 16. Recomendación final

Implementar esta arquitectura para el prototipo:

```text
Python Digital Twin
    ↓ MQTT UNS
Mosquitto
    ↓ Telegraf
InfluxDB
    ↓
Motor de reglas/anomalías + KPIs de costo + recomendaciones de mantención
    ↓
Grafana Operacional + Alertas accionables
    ↓
Dashboard Ejecutivo con KPIs e impacto económico
```

Si se requiere menor latencia, el motor de reglas también puede suscribirse directamente al broker MQTT en paralelo a Telegraf y luego persistir sus resultados en InfluxDB. En ambos casos, la condición de diseño es la misma: **el análisis predictivo debe ocurrir antes de la visualización final**.

Y presentarla como una ruta de madurez:

```text
Hackatón:
Simulador Python + MQTT + InfluxDB + Grafana

Producción:
Sensores fieldbus/HART/Ethernet + PLC/SCADA/base de datos/Kepserver + OPC UA + Edge Gateway + Sparkplug B + UNS + Data Lake + ML predictivo
```

Esta arquitectura es la más adecuada para COMASA porque:

- responde al problema real de fragmentación de datos;
- habilita monitoreo continuo;
- permite detectar fallas antes de que generen detenciones;
- conecta variables industriales con KPIs de negocio;
- monitorea gastos operacionales de combustible/biomasa, agua y vapor;
- aprovecha variables existentes exportables desde base de datos, Kepserver o conectores OT en vez de plantear una digitalización desde cero;
- incorpora el circuito agua-vapor-condensado con TAGs reales para explicar costos operacionales y pérdidas de eficiencia;
- transforma anomalías en recordatorios y sugerencias concretas de mantención;
- es viable en 3 días;
- escala hacia una arquitectura industrial seria.

Mensaje central para el pitch:

> “No estamos mostrando gráficos bonitos. Estamos demostrando cómo COMASA puede transformar señales tempranas de falla en decisiones preventivas, reducción de detenciones y mejor eficiencia energética.”
