# Prompt para agente en modo plan — Mejora de dashboards COMASA

Actúa como arquitecto de datos, diseñador de dashboards industriales y desarrollador Python/Grafana para el proyecto **COMASA Energía Predictiva**.

Trabaja **SOLO en modo PLAN**. No escribas código todavía. Primero analiza el estado actual del proyecto, los dashboards existentes, los datos disponibles, el agente de analítica y el archivo de agua/vapor/condensado. Luego propón un plan de mejora claro, ordenado y ejecutable.

---

## Contexto del proyecto

Estamos desarrollando un prototipo para COMASA basado en:

- Simulador Python / gemelo digital.
- Mosquitto MQTT.
- Telegraf.
- InfluxDB.
- Agente de analítica en Python.
- Grafana.
- Datos de referencia del archivo `Agua, Vapor y Condensado Planta COMASA.xlsx`.
- Libro base: `Estadística para ingenieros y científicos`.
- Documentación interna: `Agent.md`.

El objetivo **NO** es hacer dashboards bonitos sin sentido. El objetivo es que los dashboards ayuden a tomar decisiones reales:

- detectar anomalías;
- explicar causas probables;
- recomendar acciones de mantenimiento;
- mostrar impacto operacional/económico;
- conectar variables técnicas con KPIs entendibles para operación, mantenimiento y gerencia.

---

## Agente actual

El agente actual:

- consume MQTT desde `COMASA/#`;
- valida payloads JSON con `value` y `variable`;
- mantiene una ventana reciente de datos;
- calcula KPIs;
- evalúa reglas de anomalía;
- genera recomendaciones de mantenimiento;
- escribe en InfluxDB measurements como:
  - `telemetry_raw`;
  - `kpi`;
  - `anomaly_event`;
  - `maintenance_recommendation`.

---

## KPIs actuales o esperados

- `energia_generada_mwh_h`
- `throughput_biomasa_ton_h`
- `energia_por_ton_biomasa`
- `oee`
- `mtbf_horas_demo`
- `mttr_horas_demo`
- `horas_detencion_no_programada`
- `costo_biomasa_por_mwh`
- `agua_por_mwh`
- `vapor_por_mwh`
- `condensado_recuperado`
- `costo_agua_vapor_condensado`
- `costo_operacional_estimado`

---

## Variables relevantes

- `TemperaturaEscape`
- `PresionDiferencial`
- `PotenciaMW`
- `HumedadBiomasa`
- `ConsumoBiomasa`
- `VibracionRMS`
- `VibracionFFT1X`
- `AguaIndustrial`
- Flujo vapor / `FT_5101-1`
- Flujo condensado / `FT_3001`
- Agua Alimentación
- Agua Desmineralizada
- Vapor Sobrecalentado
- Vapor Saturado
- Condensado

---

## Escenarios de falla

- `fouling_caldera`
- `humedad_biomasa_alta`
- `perdida_vapor_condensado`
- `desbalance_turbina`
- `cavitacion_bomba`
- `combustion_inestable`

---

## Objetivo de la tarea

Quiero que propongas una mejora completa de visualización en Grafana, manteniendo lo que ya existe, pero reorganizándolo de forma más clara.

---

## Criterios de diseño

1. Cada dashboard debe responder una pregunta de decisión, no solo mostrar datos.
2. Los gráficos deben estar agrupados por causa/decisión:
   - salud general;
   - caldera/biomasa;
   - agua-vapor-condensado;
   - vibración/mantenimiento;
   - KPIs ejecutivos/costos.
3. Priorizar visualizaciones entendibles en una demo de hackatón.
4. Evitar dashboards sobrecargados.
5. Separar vista operacional, vista mantenimiento y vista gerencia.
6. Usar paneles nativos de Grafana cuando sea suficiente.
7. Usar Business Charts / Apache ECharts solo si aporta valor real.
8. Usar Python/matplotlib solo para generar gráficos estadísticos auxiliares si Grafana no lo resuelve bien.
9. No proponer una app web externa salvo que sea estrictamente necesario.
10. Mantener trazabilidad con TAGs reales del Excel cuando se trabaje agua, vapor y condensado.

---

## Recomendaciones estadísticas a aplicar desde el libro

- Usar histogramas para ver distribución de variables y detectar sesgo.
- Usar diagramas de caja/boxplot para comparar escenarios normal vs falla y detectar atípicos.
- Usar medias móviles para suavizar ruido.
- Usar z-score para detectar valores fuera de patrón normal.
- Usar gráficos de control tipo Shewhart para distinguir variación normal vs causa especial.
- Usar CUSUM si sirve para detectar cambios graduales.
- Usar scatter/XY para relacionar variables:
  - humedad biomasa vs potencia;
  - presión diferencial vs temperatura de escape;
  - vapor por MWh vs potencia;
  - condensado recuperado vs costo operacional;
  - vibración RMS vs score FFT.

---

# Estructura de respuesta solicitada

Entrega el plan con esta estructura:

---

## 1. Diagnóstico del estado actual

Incluye:

- Qué está bien.
- Qué falta.
- Qué puede confundir al jurado o al usuario.
- Qué datos ya están disponibles desde el agente.
- Qué datos faltan o convendría derivar.

---

## 2. Propuesta de dashboards

Define mínimo 5 dashboards.

---

### A. Dashboard: Vista Operacional

Debe responder:

- ¿La planta está operando normal?
- ¿Hay alertas activas?
- ¿Qué variable se salió de rango?
- ¿Qué equipo requiere atención?

Debe incluir:

- Estado general de planta.
- Potencia generada.
- Temperatura escape.
- Presión diferencial.
- Humedad biomasa.
- Consumo biomasa.
- Flujo de vapor.
- Retorno de condensado.
- Alarmas activas.
- Recomendaciones abiertas.

---

### B. Dashboard: Caldera y Biomasa

Debe responder:

- ¿La caldera está perdiendo eficiencia?
- ¿La biomasa está afectando el rendimiento?
- ¿Hay señales de fouling o humedad alta?

Debe incluir:

- `TemperaturaEscape` + `PresionDiferencial` en gráfico agrupado.
- `PotenciaMW` vs `ConsumoBiomasa`.
- `HumedadBiomasa` vs `EnergiaPorTonBiomasa`.
- `CostoBiomasaPorMWh`.
- Eventos `fouling_caldera` y `humedad_biomasa_alta`.
- Recomendación asociada.

---

### C. Dashboard: Agua, Vapor y Condensado

Debe responder:

- ¿El circuito térmico está operando eficientemente?
- ¿Se está perdiendo vapor o condensado?
- ¿Cuánto impacto tiene en costo?

Debe incluir:

- `AguaPorMWh`.
- `VaporPorMWh`.
- `CondensadoRecuperado`.
- `CostoAguaVaporCondensado`.
- Flujo vapor TAG `FT_5101-1`.
- Flujo condensado TAG `FT_3001`.
- Tabla por TAG con:
  - Desde;
  - Hasta;
  - Variable;
  - Medición;
  - Unidad;
  - Valor.
- Visualización tipo Node graph, Sankey, Canvas o Business Charts si es viable.
- Evento `perdida_vapor_condensado`.
- Recomendación asociada.

---

### D. Dashboard: Mantenimiento Predictivo

Debe responder:

- ¿Qué equipo está en mayor riesgo?
- ¿Qué recomendación debe atenderse primero?
- ¿Qué anomalía se detectó y por qué?

Debe incluir:

- Riesgo por equipo.
- Timeline de anomalías.
- Tabla de recomendaciones.
- Severidad.
- Causa probable.
- Acción sugerida.
- Plazo.
- KPI impactado.
- MTBF.
- MTTR.
- Horas de detención no programada.
- `VibracionRMS` + `VibracionFFT1X`.

---

### E. Dashboard: Vista Ejecutiva

Debe responder:

- ¿Cómo afecta la operación al negocio?
- ¿Dónde están las pérdidas?
- ¿Qué decisión debe tomar gerencia?

Debe incluir:

- OEE.
- Energía generada.
- Throughput de biomasa.
- Energía por tonelada de biomasa.
- Costo operacional estimado.
- Costo biomasa/MWh.
- Agua/MWh.
- Vapor/MWh.
- Condensado recuperado.
- Horas de detención no programada.
- Comparación normal vs falla simulada.
- Pérdidas estimadas por baja eficiencia.

---

## 3. Matriz de visualizaciones

Para cada KPI o variable, indicar:

- Nombre.
- Fuente:
  - `telemetry_raw`;
  - `kpi`;
  - `anomaly_event`;
  - `maintenance_recommendation`.
- Tipo de gráfico recomendado.
- Panel Grafana recomendado.
- Alternativa con Business Charts/ECharts.
- Alternativa con Python/matplotlib.
- Objetivo de decisión.

La matriz debe priorizar decisiones, no estética.

---

## 4. Reglas de diseño visual

Define lineamientos concretos:

- Máximo de paneles por dashboard.
- Orden visual recomendado.
- Colores por severidad.
- Uso de thresholds.
- Uso de unidades.
- Cuándo usar gauge y cuándo no.
- Cuándo usar tabla.
- Cuándo usar time series.
- Cuándo usar histogramas.
- Cuándo usar boxplots.
- Cuándo usar control charts.
- Cómo evitar que el dashboard se vea saturado.
- Cómo agrupar paneles por pregunta de decisión.

---

## 5. Mejoras recomendadas al agente

Sin programar todavía, indica qué sería útil agregar al agente para mejorar visualizaciones:

- score de riesgo por equipo;
- `ack_status` real de recomendaciones;
- `scenario` visible en KPIs;
- estado normal/warning/critical por equipo;
- costo por anomalía;
- duración de anomalía;
- lifecycle de evento:
  - open;
  - acknowledged;
  - resolved;
- cooldown por `(type, equipment, severity)`;
- variables derivadas para control chart o CUSUM;
- agregados por ventana:
  - promedio;
  - mediana;
  - desviación estándar;
  - percentiles.

---

## 6. Plan de implementación por prioridad

Divide el plan en:

### Prioridad alta

Debe implementarse para la demo.

### Prioridad media

Implementar si queda tiempo.

### Prioridad baja

Mejora futura.

Para cada tarea indicar:

- Qué se debe hacer.
- Por qué importa.
- Archivo o dashboard probable a modificar.
- Resultado esperado.

---

## 7. Archivos probables a revisar o modificar

Identifica posibles archivos:

- `grafana/dashboards/*.json`
- `grafana/provisioning/*`
- `analytics/kpis.py`
- `analytics/rules.py`
- `analytics/recommendations.py`
- `analytics/influx_writer.py`
- `simulator/catalog.py`
- `simulator/scenarios.py`
- `docker-compose.yml`
- `README.md`

---

## 8. Entregable final esperado

El resultado del plan debe ser una lista clara de tareas para implementar, **sin código todavía**.

Debe incluir:

- dashboards propuestos;
- paneles por dashboard;
- tipo de gráfico recomendado;
- fuente de datos;
- mejoras al agente;
- prioridades;
- riesgos;
- acciones concretas.

---

## Restricciones

- No inventes datos oficiales no presentes.
- No cambies la arquitectura base.
- No elimines los dashboards actuales; propón reorganizarlos o mejorarlos.
- No propongas IA compleja si no es necesaria.
- No uses “IA mágica”; mantener detección temprana explicable.
- Mantén el enfoque en decisiones operacionales y económicas.
- Entrega el plan en español, con lenguaje claro, directo y accionable.
- No escribas código en esta fase.
