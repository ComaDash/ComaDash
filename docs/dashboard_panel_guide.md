# Guía de paneles Grafana — COMASA

## Propósito y uso

Esta guía explica qué aporta cada panel de los dashboards Grafana ubicados en `grafana/dashboards/*.json`. Está escrita para que desarrollo, producto y pitch entiendan el concepto detrás de cada widget: **qué pregunta operacional o ejecutiva responde, qué decisión habilita y si conviene mostrarlo en una demo de 5 minutos**.

Usala así:

- Para preparar el pitch: seguí la ruta sugerida y mostrás solo paneles `SHOW`.
- Para desarrollo: mantené estables las mediciones, tags, campos y preguntas asociadas a cada panel.
- Para refactorizar dashboards: no muevas paneles solo por estética; primero verificá qué pregunta responden y qué decisión habilitan.
- Para discutir alcance: los paneles `SUPPORT` y `MERGE` sirven como respaldo, pero no deberían consumir tiempo central del pitch.

## Leyenda de decisiones

- `SHOW`: mostrar en el pitch/demo de 5 minutos.
- `SUPPORT`: mantener como respaldo o vista de detalle.
- `MERGE`: conservar conceptualmente, pero unirlo con otro dashboard/panel durante el pitch.
- `CUT`: no mostrar en el pitch.

## Resumen ejecutivo

### Dashboards para el pitch

| Dashboard | Decisión | Motivo |
|---|---|---|
| `problem_first_operations.json` | KEEP | Es el mejor punto de entrada: parte por problemas, no por gráficos. Responde rápido dónde mirar, qué costo tiene y qué acción tomar. |
| `water_steam_condensate.json` | KEEP | Demuestra la propuesta refinada: ciclo agua-vapor-condensado, TAGs reales, trazabilidad y costo del circuito térmico. |
| `boiler_biomass.json` | MERGE | Es clave para explicar biomasa, fouling y combustión, pero conviene mostrarlo como drill-down desde la ruta principal. |
| `master.json` | MERGE | Sirve como centro de decisión, pero repite paneles de riesgo, potencia, condensado, costos y eventos. Usarlo como respaldo o cierre. |
| `operator.json` | SUPPORT | Buena vista de turno, útil si preguntan por operación diaria. Para pitch es menos diferenciadora que la vista por problema. |
| `maintenance.json` | SUPPORT | Fuerte para la dimensión predictiva. Mostrar solo si el jurado pregunta por mantenimiento o confiabilidad. |
| `finance.json` | SUPPORT | Necesario para impacto y viabilidad, pero debe entrar como síntesis económica, no como dashboard principal completo. |

### Ruta demo recomendada

Ruta compacta preferida para GQM: abrir `GQM - COMASA Decision Narrative` (`grafana/dashboards/gqm_comasa_decision_narrative.json`, UID `gqm-decision-narrative`) y recorrer `Tramo crítico ahora`, `Ranking GQM de tramos: causa, calidad y acción`, `Eficiencia agua-vapor-condensado`, `Biomasa húmeda: consumo y MW`, `Acciones recomendadas por impacto`, `OEE` y `Costo operacional estimado`.

Ruta histórica de drill-down si hace falta más detalle:

1. Abrir `problem_first_operations.json` o su duplicado `gqm_problem_first_operations.json` y mostrar `Ranking de tramos con razón, calidad y acción`.
2. Pasar a `¿La eficiencia del circuito confirma la pérdida?` y `¿Cuánto duele en costo agua/vapor?` para conectar operación con costo.
3. Mostrar `Humedad -> consumo -> MW` y `Acción sobre biomasa` para explicar variabilidad de biomasa y recomendación accionable.
4. Abrir `water_steam_condensate.json` y mostrar `Vapor FT_5101-1 vs condensado FT_3001`, `Tabla operacional por TAG: área, equipo, medición, unidad y valor` y `Acción recomendada del circuito`.
5. Cerrar con 1 o 2 KPIs de `finance.json`: `Costo operacional estimado`, `OEE` o `Recomendaciones por impacto económico`.

Esta ruta calza con la rúbrica: prototipo funcional y demo en vivo, impacto operativo-económico, innovación por representación de tramos y presentación clara en 5 minutos.

### Dashboards GQM disponibles

| Archivo | UID | Título | Uso recomendado |
|---|---|---|---|
| `gqm_comasa_decision_narrative.json` | `gqm-decision-narrative` | `GQM - COMASA Decision Narrative` | Demo compacta principal de 5 minutos. |
| `gqm_problem_first_operations.json` | `gqm-problem-first-ops` | `GQM - COMASA Problem-First Operations` | Drill-down por tramo, razón, calidad y acción. |
| `gqm_water_steam_condensate.json` | `gqm-water-steam-cond` | `GQM - COMASA Water Steam Condensate Decisions` | Evidencia TAG y circuito agua-vapor-condensado. |
| `gqm_boiler_biomass.json` | `gqm-boiler-biomass` | `GQM - COMASA Biomass Boiler Efficiency` | Causa raíz biomasa/caldera/combustión. |
| `gqm_maintenance.json` | `gqm-maintenance-risk` | `GQM - COMASA Predictive Maintenance Risk` | Riesgo, acciones preventivas y backlog. |
| `gqm_finance.json` | `gqm-finance-impact` | `GQM - COMASA Executive Financial Impact` | Cierre de OEE, costo e impacto ejecutivo. |

Ver detalle de implementación, mapeo de títulos planificados vs reales, mitigaciones y métricas futuras en `docs/gqm_dashboard_implementation.md`.

## `problem_first_operations.json` — COMASA - Revision integrada por problema

Decisión general: `KEEP`. Es el dashboard más alineado con `info/refinamiento_dashboard_COMASA.md` porque organiza la lectura por preguntas críticas, tramos, calidad de datos, acción e impacto. Para el pitch, ESTE es el tablero principal.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `Pregunta 1: ¿Qué tramo agua-vapor-condensado necesita atención primero?` | row | Separador narrativo de la primera pregunta operacional. | Sin consulta. | ¿Dónde empieza el diagnóstico? | Enfocar la demo en el tramo más crítico. | Existe para evitar un dashboard decorativo. Refuerza la unidad de análisis `tramo operacional` definida en el refinamiento y el contrato `segment_status` de arquitectura. | SHOW |
| `Tramo crítico en 10 segundos` | stat | Mayor `risk_score` reciente para tramos impactados por `excessive_water_loss`. | `segment_status`, campo `risk_score`, tags `segment_id`, `from_node`, `to_node`, `status`, filtro `impacted_problem = excessive_water_loss`. | ¿Qué tramo necesita atención primero? | Priorizar inspección sin revisar tablas ni series una por una. | Responde la pregunta central del refinamiento: identificar rápido el tramo comprometido. Aporta calidad de prototipo e innovación porque convierte datos fragmentados en decisión inmediata. | SHOW |
| `Ranking de tramos con razón, calidad y acción` | table | Lista de tramos ordenados por riesgo, con estado, origen, destino, fluido, TAG, valor, calidad, razón, acción e impacto. | `segment_status`; campos `risk_score`, `value`, `reason`, `recommendation_link`, `cost_efficiency_impact`; tags de tramo, fluido, TAG, unidad, calidad y problema. | ¿Qué reviso primero y por qué? | Ordenar acciones de operación o mantención según riesgo y evidencia. | Es el panel más importante para demostrar trazabilidad y reportabilidad. Conecta arquitectura, refinamiento y rubric de impacto: muestra causa, evidencia y acción. | SHOW |
| `¿La eficiencia del circuito confirma la pérdida?` | timeseries | Tendencia de `condensado_recuperado`, `agua_por_mwh` y `vapor_por_mwh`. | `kpi`, campo `value`, KPIs `condensado_recuperado`, `agua_por_mwh`, `vapor_por_mwh`. | ¿El problema del tramo se ve también en eficiencia del circuito? | Validar si una alerta local tiene impacto sistémico. | Evita mirar una variable aislada. Justifica la integración agua-vapor-condensado con energía, un punto central del refinamiento y del desafío. | SHOW |
| `¿Cuánto duele en costo agua/vapor?` | stat | Costo actual estimado del circuito agua-vapor-condensado. | `kpi`, `costo_agua_vapor_condensado`. | ¿Cuál es el impacto económico inmediato? | Comunicar prioridad económica a jefatura. | Une operación con viabilidad, clave para el 25% de impacto y viabilidad de la rúbrica. | SHOW |
| `Pregunta 2: ¿La variabilidad de biomasa está golpeando potencia y costo?` | row | Separador narrativo para biomasa y potencia. | Sin consulta. | ¿La biomasa explica parte del rendimiento? | Cambiar de diagnóstico hídrico/térmico a combustible. | El refinamiento y la arquitectura piden integrar biomasa con vapor, energía y costo, no tratarla como dato externo. | SHOW |
| `Humedad -> consumo -> MW` | timeseries | Relación temporal entre `HumedadBiomasa`, `ConsumoBiomasa` y `PotenciaMW`. | `telemetry_raw`, variables `HumedadBiomasa`, `ConsumoBiomasa`, `PotenciaMW`. | ¿La humedad de biomasa aumenta consumo y reduce generación? | Ajustar mezcla/calidad de biomasa o anticipar baja eficiencia. | Es una historia causal fácil para pitch: combustible peor, más consumo, menos MW. Apoya analítica avanzada explicable sin vender IA mágica. | SHOW |
| `Acción sobre biomasa` | table | Recomendaciones asociadas al `SistemaBiomasa`. | `maintenance_recommendation`, filtro `equipment = SistemaBiomasa`, campos `severity`, `probable_cause`, `suggested_action`, `expected_impact`. | ¿Qué acción concreta tomar ante variabilidad de biomasa? | Pasar de observación a acción preventiva. | Refuerza que el motor publica recomendaciones, como exige la arquitectura: Grafana debe consumir eventos procesados, no solo señales crudas. | SHOW |
| `Pregunta 3: ¿Hay señal de degradación térmica asociada al agua?` | row | Separador narrativo para degradación térmica asociada al agua. | Sin consulta. | ¿El agua puede estar afectando desempeño térmico? | Abrir análisis de degradación de proceso. | Está directamente alineado con el refinamiento: posible degradación térmica por agua de pozo y calidad/trazabilidad de datos. | SUPPORT |
| `Señal térmica y confianza de datos` | table | Tramos con problema `well_water_thermal_degradation`, riesgo, calidad, confianza, razón y causa recomendada. | `segment_status`, filtro `impacted_problem = well_water_thermal_degradation`, campos `risk_score`, `value`, `confidence`, `reason`, `recommendation_cause`. | ¿Hay evidencia confiable de degradación térmica asociada al agua? | Decidir si investigar calidad de agua, tratamiento o tramo térmico. | Muy valioso como respaldo técnico. En 5 minutos puede ser demasiado específico salvo que el pitch enfatice calidad de agua. | SUPPORT |
| `Pregunta 4: ¿Qué conocimiento operacional debe quedar sistematizado?` | row | Separador para convertir experiencia de turno en conocimiento reutilizable. | Sin consulta. | ¿Qué conocimiento tácito debe quedar visible? | Enfocar recomendaciones como base de aprendizaje operacional. | Alineado con el refinamiento: reducir dependencia del operador sin culparlo. | SUPPORT |
| `Causa -> acción -> impacto: base mínima de conocimiento del turno` | table | Recomendaciones recientes con equipo, severidad, causa probable, acción, impacto, plazo y estado. | `maintenance_recommendation`, campos `equipment`, `severity`, `probable_cause`, `suggested_action`, `expected_impact`, `due_minutes`, `ack_status`. | ¿Qué patrón operacional ya fue convertido en acción sistemática? | Documentar conocimiento y priorizar acciones de turno. | Excelente respaldo para innovación y escalabilidad organizacional. Para pitch, mostrar solo si hay tiempo. | SUPPORT |
| `Pregunta 5: ¿Operación histórica y energía cuentan la misma historia?` | row | Separador para cerrar con energía, costo y riesgo. | Sin consulta. | ¿Los KPIs confirman el diagnóstico operacional? | Conectar operación histórica con resultado económico. | Sostiene la integración OT/IT y la reportabilidad en tiempo real exigidas por el desafío. | SHOW |
| `Energía, costo y eficiencia operacional` | timeseries | Tendencia de energía generada, costo operacional y energía por tonelada de biomasa. | `kpi`, KPIs `energia_generada_mwh_h`, `costo_operacional_estimado`, `energia_por_ton_biomasa`. | ¿La planta produce más, cuesta menos y usa mejor la biomasa? | Explicar impacto de eficiencia a nivel negocio. | Buen panel de cierre porque conecta producción, costo y eficiencia específica, tres conceptos defendibles ante jurado. | SHOW |
| `Top riesgos que explican el costo` | bargauge | Ranking de activos por `risk_score` que pueden explicar costo. | `asset_risk`, campo `risk_score`, tags `equipment`, `status`. | ¿Qué activos están detrás del costo o pérdida de eficiencia? | Priorizar equipos que impactan el negocio. | Une mantenimiento predictivo con impacto económico. Es fuerte para cierre si no se abre `maintenance.json`. | SHOW |

## `water_steam_condensate.json` — COMASA - Agua, vapor y condensado

Decisión general: `KEEP`. Es el dashboard de evidencia de proceso. Demuestra que la solución no parte de widgets genéricos, sino de TAGs y circuitos reales del XLSX: `FT_5101-1`, `FT_3001`, `FT_5001`, `FT_2101-1`, `FT_5002`.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `¿El circuito agua-vapor-condensado está perdiendo eficiencia?` | row | Separador del bloque de salud del circuito térmico. | Sin consulta. | ¿El circuito está operando eficientemente? | Abrir diagnóstico de agua, vapor y condensado. | Alinea la vista con la pregunta clave del refinamiento: dónde, cuándo y bajo qué condiciones se pierde eficiencia. | SHOW |
| `Riesgo circuito térmico` | stat | Riesgo del equipo lógico `CircuitoAguaVaporCondensado`. | `asset_risk`, `equipment = CircuitoAguaVaporCondensado`, campo `risk_score`. | ¿Cuál es el nivel de riesgo global del circuito? | Decidir si el circuito requiere atención inmediata. | Resume analítica predictiva en un indicador simple; útil para demo rápida. | SHOW |
| `Agua por MWh` | stat | Consumo específico de agua por energía generada. | `kpi`, `agua_por_mwh`. | ¿Cuánta agua cuesta producir energía? | Detectar sobreconsumo hídrico. | Directamente recomendado por arquitectura y refinamiento como métrica de eficiencia integrada. | SHOW |
| `Vapor por MWh` | stat | Vapor requerido por energía generada. | `kpi`, `vapor_por_mwh`. | ¿Cuánto vapor necesita la planta para producir MWh? | Detectar pérdida térmica o baja eficiencia. | Conecta proceso térmico con generación, clave para reportabilidad operacional. | SHOW |
| `Condensado recuperado` | stat | Porcentaje de condensado recuperado. | `kpi`, `condensado_recuperado`. | ¿El ciclo está recuperando suficiente condensado? | Priorizar revisión de retorno, fugas o pérdidas. | Es uno de los indicadores más claros para explicar pérdida de eficiencia y costo oculto. | SHOW |
| `Balance operativo del circuito` | row | Separador para balance entre vapor, condensado, eficiencia y costo. | Sin consulta. | ¿El balance operacional confirma la hipótesis? | Pasar de indicadores a comportamiento de proceso. | Refuerza que el proceso es la entidad, no una variable aislada. | SHOW |
| `Vapor FT_5101-1 vs condensado FT_3001` | timeseries | Comparación de flujo de vapor sobrecalentado y retorno de condensado. | `telemetry_raw`, tags `FT_5101-1`, `FT_3001`, variable `Flujo`. | ¿El condensado retorna acorde al vapor generado/enviado? | Investigar pérdida de condensado, venteo, fuga o trampa/válvula defectuosa. | Excelente para demo porque usa TAGs reales y muestra trazabilidad industrial. | SHOW |
| `Eficiencia agua, vapor y condensado` | timeseries | Tendencia de `agua_por_mwh`, `vapor_por_mwh` y `condensado_recuperado`. | `kpi`, esos tres KPIs. | ¿La eficiencia del circuito mejora o empeora en el tiempo? | Confirmar tendencia antes de decidir intervención. | Buen respaldo al panel problem-first; puede fusionarse en la narrativa para no repetir. | MERGE |
| `Costo agua/vapor/condensado` | stat | Costo estimado del circuito térmico. | `kpi`, `costo_agua_vapor_condensado`. | ¿Cuánto cuesta la ineficiencia del circuito? | Traducir la pérdida técnica a impacto económico. | Importante para la rúbrica de impacto y viabilidad. Ya aparece en el dashboard por problema, por eso puede fusionarse. | MERGE |
| `Valores actuales por TAG crítico` | barchart | Valores recientes de TAGs críticos del circuito. | `telemetry_raw`, tags `FT_5101-1`, `FT_3001`, `FT_5001`, `FT_2101-1`, `FT_5002`. | ¿Qué TAGs críticos están altos o bajos ahora? | Revisar mediciones base antes de interpretar KPIs. | Útil para mostrar compatibilidad con datos industriales reales. Para pitch, mostrar breve si se quiere evidenciar trazabilidad. | SUPPORT |
| `Trazabilidad por TAG` | row | Separador de detalle instrumental. | Sin consulta. | ¿De dónde viene cada dato? | Validar confianza y origen de mediciones. | La arquitectura insiste en conservar TAG y contexto; este bloque lo hace visible. | SUPPORT |
| `Tabla operacional por TAG: área, equipo, medición, unidad y valor` | table | Tabla por área, equipo, TAG, variable, unidad, calidad, valor y tiempo. | `telemetry_raw`, áreas `AguaIndustrial`, `AguaAlimentacion`, `AguaDesmineralizada`, `VaporSobrecalentado`, `Condensado`. | ¿Qué mide cada TAG y con qué calidad? | Auditar trazabilidad antes de tomar decisiones. | Es respaldo fuerte contra la crítica de “datos inventados”: muestra estructura industrial y calidad. | SHOW |
| `Pérdida de vapor/condensado y acción` | row | Separador para eventos y acciones del circuito. | Sin consulta. | ¿La pérdida ya generó evento y recomendación? | Pasar de diagnóstico a acción. | Alineado con la arquitectura: eventos y recomendaciones ya procesados antes de visualizar. | SHOW |
| `Evento pérdida vapor/condensado` | table | Eventos de anomalía de tipo `perdida_vapor_condensado`. | `anomaly_event`, filtro `type = perdida_vapor_condensado`, campos `equipment`, `severity`, `score`, `message`, `probable_cause`, `impacted_kpis`. | ¿Qué evento explica la pérdida? | Confirmar causa probable e impacto en KPIs. | Buen panel de demo si hay un evento sintético cargado. Muestra predicción/falla y reportabilidad. | SHOW |
| `Acción recomendada del circuito` | table | Recomendaciones para `CircuitoAguaVaporCondensado`. | `maintenance_recommendation`, campos `suggested_action`, `due_minutes`, `expected_impact`, `ack_status`. | ¿Qué debe hacer el equipo ahora? | Ejecutar acción preventiva con plazo e impacto esperado. | Es la pieza accionable; sin esto el dashboard se queda en monitoreo. | SHOW |

## `boiler_biomass.json` — COMASA - Caldera y biomasa

Decisión general: `MERGE`. Es buen drill-down de causa raíz para fouling, biomasa y combustión. En el pitch debe aparecer como explicación secundaria después de la ruta por problema.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `¿La caldera o la biomasa están bajando el rendimiento?` | row | Separador del diagnóstico caldera/biomasa. | Sin consulta. | ¿La pérdida viene de caldera, biomasa o combustión? | Abrir análisis de causa raíz energética. | Conecta variables de biomasa, combustión y eficiencia, requeridas por arquitectura. | MERGE |
| `Riesgo fouling caldera` | stat | Riesgo de `CalderaBiomasa01`. | `asset_risk`, `equipment = CalderaBiomasa01`, `risk_score`. | ¿Hay riesgo de ensuciamiento/fouling? | Programar limpieza o inspección. | Muestra predicción de falla explicable, útil para calidad del prototipo. | MERGE |
| `Riesgo calidad biomasa` | stat | Riesgo asociado al `SistemaBiomasa`. | `asset_risk`, `equipment = SistemaBiomasa`, `risk_score`. | ¿La biomasa está afectando rendimiento? | Ajustar mezcla, suministro o control de humedad. | Apoya el problema de variabilidad de biomasa descrito en refinamiento. | SHOW |
| `Riesgo combustión` | stat | Riesgo de `CombustionCaldera`. | `asset_risk`, `equipment = CombustionCaldera`, `risk_score`. | ¿La combustión está inestable? | Revisar aire, O2/CO o control de combustión. | Conecta señales de combustión con riesgo operacional. | SUPPORT |
| `Costo biomasa por MWh` | stat | Costo de biomasa por energía producida. | `kpi`, `costo_biomasa_por_mwh`. | ¿La biomasa está encareciendo el MWh? | Priorizar acciones por costo de combustible. | Muy útil para impacto, pero ya aparece en finanzas. | MERGE |
| `Evidencia técnica` | row | Separador para las señales que explican el riesgo. | Sin consulta. | ¿Qué señales sostienen el diagnóstico? | Presentar evidencia antes de recomendar. | Evita vender “alertas mágicas”; muestra fundamentos. | SUPPORT |
| `Fouling: temperatura escape + presión diferencial` | timeseries | Tendencia de `TemperaturaEscape` y `PresionDiferencial`. | `telemetry_raw`, variables `TemperaturaEscape`, `PresionDiferencial`. | ¿Hay patrón compatible con fouling? | Revisar superficies de intercambio y caída de presión. | Es el ejemplo técnico más claro de detección temprana explicable. | SHOW |
| `Potencia generada vs consumo de biomasa` | timeseries | Relación entre `PotenciaMW` y `ConsumoBiomasa`. | `telemetry_raw`, variables `PotenciaMW`, `ConsumoBiomasa`. | ¿Se consume más biomasa sin producir más MW? | Detectar ineficiencia de combustible. | Conecta operación y economía, útil para la rúbrica de impacto. | SHOW |
| `Humedad biomasa vs energía por tonelada` | timeseries | Humedad de biomasa frente a `energia_por_ton_biomasa`. | `telemetry_raw` `HumedadBiomasa` + `kpi` `energia_por_ton_biomasa`. | ¿La humedad reduce energía específica? | Evaluar calidad de biomasa antes de culpar equipos. | Buena historia causal para pitch, pero puede repetirse con `Humedad -> consumo -> MW`. | MERGE |
| `Combustión: CO y O2` | timeseries | Señales de CO y O2. | `telemetry_raw`, variables `CO`, `O2`. | ¿La combustión está completa y estable? | Ajustar aire/combustión o investigar inestabilidad. | Técnicamente relevante, pero menos directo para un pitch corto. | SUPPORT |
| `Eventos y decisión` | row | Separador para eventos y recomendaciones. | Sin consulta. | ¿Qué eventos y acciones salen del diagnóstico? | Cerrar la causa raíz con acción. | Refuerza analítica previa al dashboard. | SUPPORT |
| `Eventos caldera/biomasa` | table | Eventos `fouling_caldera`, `humedad_biomasa_alta` y `combustion_inestable`. | `anomaly_event`, campos de equipo, severidad, tipo, score, mensaje y causa probable. | ¿Qué anomalía fue detectada? | Validar severidad y causa probable. | Respaldo importante para demo predictiva. | SUPPORT |
| `Recomendación asociada` | table | Recomendaciones para caldera, biomasa y combustión. | `maintenance_recommendation`, equipos `CalderaBiomasa01`, `SistemaBiomasa`, `CombustionCaldera`. | ¿Qué acción se debe ejecutar? | Programar intervención preventiva. | Muestra conversión de anomalía a acción; usar si no se muestra la recomendación del dashboard principal. | MERGE |

## `master.json` — COMASA - Centro de decisión operacional

Decisión general: `MERGE`. Es un centro de mando útil, pero repite conceptos. Para pitch conviene usarlo como respaldo o como cierre si se quiere mostrar visión integral.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `Resumen ejecutivo-operacional` | row | Separador del bloque de salud general. | Sin consulta. | ¿Cómo está la planta ahora? | Dar contexto inicial o cierre ejecutivo. | Alinea operación y gerencia, pedido explícito en arquitectura. | MERGE |
| `Riesgo planta` | stat | Máximo riesgo entre activos. | `asset_risk`, `risk_score`, máximo por equipo. | ¿Cuál es el peor riesgo actual? | Decidir si hay condición crítica general. | Útil, pero menos específico que el tramo crítico. | MERGE |
| `Potencia actual` | stat | Último valor de `PotenciaMW`. | `telemetry_raw`, variable `PotenciaMW`. | ¿Cuánto está generando la planta ahora? | Ver impacto productivo inmediato. | KPI operacional básico; mostrar solo como contexto. | SUPPORT |
| `OEE actual` | gauge | OEE actual. | `kpi`, `oee`. | ¿Qué tan efectiva está la operación? | Comunicar salud operacional global. | KPI explícito del desafío y de arquitectura. | SHOW |
| `Condensado recuperado` | stat | Porcentaje de condensado recuperado. | `kpi`, `condensado_recuperado`. | ¿Se recupera suficiente condensado? | Detectar pérdida de eficiencia térmica. | Repetido en otros dashboards; fusionar. | MERGE |
| `Top activos en riesgo` | bargauge | Ranking de equipos por riesgo. | `asset_risk`, `risk_score`, top 6 por `equipment`. | ¿Dónde está concentrado el riesgo? | Priorizar equipos para revisión. | Útil para visión integral, pero `problem_first` lo expresa mejor por costo y problema. | MERGE |
| `Acciones recomendadas ahora` | table | Top 5 recomendaciones recientes. | `maintenance_recommendation`, campos de acción, plazo, impacto y estado. | ¿Qué hacemos ahora? | Convertir diagnóstico en tareas. | Panel fuerte para demo si se usa `master` como pantalla inicial. | SHOW |
| `Tendencias críticas` | row | Separador de variables críticas. | Sin consulta. | ¿Qué señales explican el estado actual? | Entrar a evidencia temporal. | Respalda el enfoque de series temporales de Grafana + InfluxDB. | SUPPORT |
| `Producción eléctrica` | timeseries | Tendencia de `PotenciaMW`. | `telemetry_raw`, `PotenciaMW`. | ¿Cómo evoluciona la generación? | Detectar caída productiva. | Básico y necesario, pero no diferenciador. | SUPPORT |
| `Pérdida térmica: temperatura escape` | timeseries | Tendencia de `TemperaturaEscape`. | `telemetry_raw`, `TemperaturaEscape`. | ¿Se está perdiendo calor por escape? | Investigar fouling o baja transferencia térmica. | Muy buen respaldo técnico; ya aparece en caldera/mantenimiento. | MERGE |
| `Riesgo mecánico: vibración` | timeseries | Vibración RMS de turbina y bomba. | `telemetry_raw`, `VibracionRMS`, `VibracionBombaRMS`. | ¿Hay señal mecánica anómala? | Revisar riesgo de desbalance/cavitación. | Apoya predicción de falla, pero mejor en `maintenance.json`. | SUPPORT |
| `Servicios y costos` | row | Separador de agua, vapor, condensado y costo. | Sin consulta. | ¿Cómo se conectan servicios industriales con costo? | Abrir lectura operación-finanzas. | Alineado con separar visualización operacional y financiera, pero conectarlas. | SHOW |
| `Agua: flujos por circuito` | timeseries | Flujos de áreas de agua industrial, alimentación y desmineralizada. | `telemetry_raw`, áreas `AguaIndustrial`, `AguaAlimentacion`, `AguaDesmineralizada`, variable `Flujo`. | ¿Cómo se mueven los flujos de agua? | Detectar sobreconsumo o desviaciones por área. | Relevante, pero `water_steam_condensate` tiene trazabilidad por TAG más fuerte. | MERGE |
| `Vapor vs retorno de condensado` | timeseries | Flujo de vapor sobrecalentado frente a condensado. | `telemetry_raw`, áreas `VaporSobrecalentado`, `Condensado`, variable `Flujo`. | ¿El retorno acompaña al vapor? | Detectar pérdida del ciclo térmico. | Repite el panel con TAGs reales; usar el de `water_steam_condensate`. | MERGE |
| `Impacto económico en tiempo real` | timeseries | Tendencia de costos de biomasa, circuito térmico y operación. | `kpi`, `costo_biomasa_por_mwh`, `costo_agua_vapor_condensado`, `costo_operacional_estimado`. | ¿Cómo se mueve el costo ahora? | Relacionar anomalías con gasto. | Muy útil para cierre ejecutivo; también está en `finance`. | SHOW |
| `Detalle de eventos` | row | Separador de anomalías. | Sin consulta. | ¿Qué eventos explican el estado? | Auditar eventos detectados. | Respalda el motor de anomalías de la arquitectura. | SUPPORT |
| `Anomalías detectadas` | table | Eventos recientes con equipo, severidad, tipo, score, mensaje y causa probable. | `anomaly_event`. | ¿Qué detectó el sistema? | Revisar causa probable y severidad. | Fuerte para demostrar analítica, pero no abrir si ya se mostró recomendación. | SUPPORT |
| `Historial de anomalías por equipo` | state-timeline | Evolución temporal de anomalías por equipo y tipo. | `anomaly_event`, campos `equipment`, `severity`, `type`, `score`. | ¿Cuándo ocurrió cada anomalía? | Ver recurrencia y secuencia. | Buen respaldo, pero consume tiempo en pitch. | SUPPORT |

## `operator.json` — COMASA - Vista operador de turno

Decisión general: `SUPPORT`. Es una vista práctica para turno, con valores inmediatos y acciones. En pitch conviene mencionarla como evidencia de adopción por rol, no recorrerla completa.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `Estado inmediato de operación` | row | Separador del bloque de atención del operador. | Sin consulta. | ¿Qué debe mirar el turno ahora? | Enfocar operación inmediata. | Alineado con vistas por rol recomendadas en arquitectura. | SUPPORT |
| `Riesgo operacional` | stat | Máximo riesgo entre equipos. | `asset_risk`, `risk_score`. | ¿El turno está en condición normal, atención o crítica? | Escalar o mantener monitoreo. | Simple y útil, pero genérico frente a `Tramo crítico en 10 segundos`. | SUPPORT |
| `Potencia actual` | stat | Última potencia en MW. | `telemetry_raw`, `PotenciaMW`. | ¿La generación está dentro de lo esperado? | Detectar pérdida productiva inmediata. | KPI operacional básico. | SUPPORT |
| `Temperatura escape` | stat | Última temperatura de escape. | `telemetry_raw`, `TemperaturaEscape`. | ¿Hay señal de pérdida térmica? | Revisar caldera si supera umbrales. | Indicador temprano de fouling. | MERGE |
| `Presión diferencial` | stat | Última presión diferencial. | `telemetry_raw`, `PresionDiferencial`. | ¿Hay restricción u obstrucción? | Revisar limpieza o condición de flujo. | Indicador temprano de ensuciamiento. | MERGE |
| `Alarmas activas y explicación` | table | Últimas anomalías con equipo, severidad, tipo, mensaje y score. | `anomaly_event`. | ¿Qué alarma explica el estado actual? | Atender alarma priorizada. | Convierte analítica en lectura de turno. | SUPPORT |
| `Acción recomendada para turno` | table | Recomendaciones con acción, plazo, impacto y estado. | `maintenance_recommendation`. | ¿Qué acción debe ejecutar o registrar el operador? | Tomar acción preventiva. | Muy alineado con reducir dependencia del conocimiento individual. | SUPPORT |
| `Variables de proceso` | row | Separador de tendencias operativas. | Sin consulta. | ¿Qué variables explican el estado? | Ir desde alerta a evidencia. | Correcto para operación, pero secundario en pitch. | SUPPORT |
| `Producción MW` | timeseries | Tendencia de `PotenciaMW`. | `telemetry_raw`, `PotenciaMW`. | ¿La generación cae o se recupera? | Ajustar operación o investigar causa. | Repite producción de `master`. | CUT |
| `Temperatura gases` | timeseries | Tendencia de `TemperaturaEscape`. | `telemetry_raw`, `TemperaturaEscape`. | ¿La temperatura muestra deriva térmica? | Confirmar fouling o pérdida de eficiencia. | Mejor mostrar en caldera si hace falta. | MERGE |
| `Presión diferencial` | timeseries | Tendencia de `PresionDiferencial`. | `telemetry_raw`, `PresionDiferencial`. | ¿La presión diferencial empeora? | Confirmar obstrucción progresiva. | Repetido; útil como respaldo. | SUPPORT |
| `Combustión: humedad biomasa y O2` | timeseries | Humedad de biomasa y O2. | `telemetry_raw`, `HumedadBiomasa`, `O2`. | ¿La combustión tiene relación con biomasa húmeda? | Ajustar combustión o revisar combustible. | Panel útil, pero la historia causal es mejor en `problem_first` y `boiler_biomass`. | MERGE |
| `Vibración crítica` | timeseries | Vibración de turbina y bomba. | `telemetry_raw`, `VibracionRMS`, `VibracionBombaRMS`. | ¿Hay riesgo mecánico inmediato? | Avisar a mantenimiento. | Apoya predicción de falla, mejor desarrollado en `maintenance`. | SUPPORT |
| `Servicios: vapor y retorno` | timeseries | Flujos de vapor sobrecalentado y condensado. | `telemetry_raw`, áreas `VaporSobrecalentado`, `Condensado`, variable `Flujo`. | ¿El vapor y el retorno están balanceados? | Detectar pérdida del circuito. | Repetido con más trazabilidad en `water_steam_condensate`. | MERGE |

## `maintenance.json` — COMASA - Mantenimiento predictivo y riesgo de falla

Decisión general: `SUPPORT`. Es el mejor respaldo para defender predicción de fallas, MTBF, MTTR, FFT y backlog preventivo. Para pitch, mostrar solo si hay pregunta técnica o si se necesita reforzar el 40% de calidad del prototipo.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `Prioridad de mantenimiento` | row | Separador del bloque de priorización. | Sin consulta. | ¿Qué activo se atiende primero? | Enfocar al equipo de mantenimiento. | Alineado con mantenimiento predictivo pedido por el desafío. | SUPPORT |
| `Riesgo máximo activo` | stat | Máximo `risk_score` entre activos. | `asset_risk`. | ¿Qué tan crítica es la peor condición actual? | Escalar mantenimiento. | Indicador sintético; útil como respaldo. | SUPPORT |
| `Ranking visual de equipos cerca de falla` | bargauge | Ranking de equipos por riesgo. | `asset_risk`, `risk_score` por `equipment`. | ¿Qué equipos están más cerca de falla? | Ordenar inspección. | Directo para predicción de fallas, pero menos explicativo que la tabla. | SUPPORT |
| `Equipos cerca de fallar: orden de atención` | table | Equipos con área, estado, anomalía probable, riesgo, señal dominante, acción, plazo e impacto. | `asset_risk`, campos `probable_anomaly`, `risk_score`, `dominant_signal`, `suggested_action`, `due_minutes`, `expected_impact`. | ¿Qué equipo atiendo, por qué y con qué acción? | Planificar mantenimiento preventivo. | Panel fuerte: une riesgo, causa, señal y acción. Si se muestra mantenimiento, mostrar este. | SHOW |
| `Eventos y acciones` | row | Separador para anomalías y backlog. | Sin consulta. | ¿Qué ocurrió y qué acciones quedan? | Revisar trazabilidad de eventos. | Alineado con motor de anomalías y recomendaciones. | SUPPORT |
| `Timeline de anomalías por equipo` | state-timeline | Eventos por equipo a lo largo del tiempo. | `anomaly_event`, campos `equipment`, `severity`, `type`, `score`. | ¿Cuándo y dónde aparecieron anomalías? | Ver recurrencia o patrón temporal. | Útil para diagnóstico, no para demo corta. | SUPPORT |
| `Backlog preventivo recomendado` | table | Lista de recomendaciones ordenadas por plazo. | `maintenance_recommendation`, orden `due_minutes`. | ¿Qué tarea preventiva vence primero? | Planificar backlog de mantenimiento. | Muy defendible para impacto operacional; mostrar si preguntan por adopción. | SUPPORT |
| `Salud mecánica y confiabilidad` | row | Separador para vibración, FFT y confiabilidad. | Sin consulta. | ¿La salud mecánica respalda el riesgo? | Entrar a evidencia técnica. | Alineado con variables rápidas y FFT de arquitectura. | SUPPORT |
| `Vibración RMS turbina y bomba` | timeseries | Vibración RMS de turbina y bomba. | `telemetry_raw`, `VibracionRMS`, `VibracionBombaRMS`. | ¿Hay vibración anormal? | Detectar desbalance o cavitación. | Ejemplo claro de mantenimiento predictivo. | SUPPORT |
| `Componentes FFT dominantes` | barchart | Componentes FFT 1X y alta frecuencia de bomba. | `telemetry_raw`, `VibracionFFT1X`, `VibracionBombaFFTAlta`. | ¿Qué frecuencia domina la vibración? | Diferenciar desbalance/cavitación de ruido general. | Aporta innovación técnica, pero requiere explicación; cuidado con el tiempo. | SUPPORT |
| `Confiabilidad actual` | barchart | MTBF, MTTR y horas de detención no programada. | `kpi`, `mtbf_horas_demo`, `mttr_horas_demo`, `horas_detencion_no_programada`. | ¿Cómo está la confiabilidad operacional? | Comunicar mantenibilidad y downtime. | KPIs explícitos del desafío. Mejor mostrar en finanzas si se necesita síntesis ejecutiva. | MERGE |
| `Indicadores tempranos` | row | Separador de temperatura y presión como señales tempranas. | Sin consulta. | ¿Qué señales anticipan falla? | Mirar precursores antes del evento. | Refuerza detección temprana explicable. | SUPPORT |
| `Indicador temprano: temperatura de escape` | timeseries | Tendencia de `TemperaturaEscape`. | `telemetry_raw`, `TemperaturaEscape`. | ¿La temperatura anticipa fouling? | Programar revisión de caldera. | Repetido en caldera; usar como respaldo. | MERGE |
| `Indicador temprano: presión diferencial` | timeseries | Tendencia de `PresionDiferencial`. | `telemetry_raw`, `PresionDiferencial`. | ¿La presión anticipa obstrucción? | Programar limpieza/inspección. | Repetido en caldera; usar como respaldo. | MERGE |

## `finance.json` — COMASA - Vista ejecutiva y finanzas

Decisión general: `SUPPORT`. Es necesario para el relato de impacto, pero no debe reemplazar la historia operacional. En pitch usar solo 2 o 3 paneles para cerrar valor.

| Panel | Tipo | Qué muestra | Base de datos/consulta | Pregunta que responde | Decisión que habilita | Motivo y justificación | Pitch |
|---|---|---|---|---|---|---|---|
| `Impacto del negocio` | row | Separador de KPIs ejecutivos. | Sin consulta. | ¿Qué valor de negocio está en juego? | Enfocar a gerencia. | Alineado con separar vista operacional y financiera. | SHOW |
| `Energía generada` | stat | Energía generada reciente. | `kpi`, `energia_generada_mwh_h`. | ¿Cuánta energía se está generando? | Medir producción acumulada. | KPI explícito del desafío. | SHOW |
| `Throughput biomasa` | stat | Toneladas por hora de biomasa. | `kpi`, `throughput_biomasa_ton_h`. | ¿Cuánta biomasa procesa el sistema? | Evaluar capacidad y estabilidad de alimentación. | KPI explícito del desafío. | SUPPORT |
| `OEE` | gauge | Efectividad global del equipo/proceso. | `kpi`, `oee`. | ¿Qué tan efectiva es la operación? | Comunicar salud operacional global. | KPI explícito y muy entendible para jurado. | SHOW |
| `Costo operacional estimado` | stat | Costo operacional agregado. | `kpi`, `costo_operacional_estimado`. | ¿Cuánto cuesta operar en la condición actual? | Cerrar el caso de negocio. | Panel clave para impacto y viabilidad. | SHOW |
| `Dónde se pierde valor` | row | Separador de costos y recuperación. | Sin consulta. | ¿Qué componente explica la pérdida? | Pasar de KPI agregado a causa. | Refuerza que el valor económico viene de variables operacionales. | SHOW |
| `Costo biomasa por MWh` | stat | Costo de biomasa por energía. | `kpi`, `costo_biomasa_por_mwh`. | ¿Cuánto pesa la biomasa en el MWh? | Optimizar combustible o mezcla. | Fuerte para negocio; puede fusionarse con caldera/biomasa. | MERGE |
| `Costo circuito térmico` | stat | Costo asociado a agua, vapor y condensado. | `kpi`, `costo_agua_vapor_condensado`. | ¿Cuánto cuesta la ineficiencia térmica? | Justificar intervención en circuito. | Conecta el refinamiento de agua-vapor-condensado con finanzas. | SHOW |
| `Condensado recuperado` | stat | Recuperación de condensado. | `kpi`, `condensado_recuperado`. | ¿La recuperación reduce costos? | Priorizar retorno de condensado. | Repetido en `water_steam_condensate`; usar como puente ejecutivo. | MERGE |
| `Tendencia de costos` | timeseries | Evolución de costos de biomasa, circuito térmico y operación total. | `kpi`, `costo_biomasa_por_mwh`, `costo_agua_vapor_condensado`, `costo_operacional_estimado`. | ¿El costo está subiendo o bajando? | Evaluar impacto temporal de anomalías. | Buen panel de cierre si se quiere mostrar tiempo real financiero. | SUPPORT |
| `Composición de costos actual` | barchart | Comparación actual de costo biomasa y circuito térmico. | `kpi`, `costo_biomasa_por_mwh`, `costo_agua_vapor_condensado`. | ¿Qué componente pesa más ahora? | Priorizar biomasa o circuito térmico. | Útil para gerencia, pero simplificado. | SUPPORT |
| `Decisiones para jefatura` | row | Separador de recomendaciones y riesgo de negocio. | Sin consulta. | ¿Qué debe decidir jefatura? | Convertir técnica en decisión ejecutiva. | Alineado con impacto y presentación. | SHOW |
| `Recomendaciones por impacto económico` | table | Recomendaciones con impacto e KPIs afectados. | `maintenance_recommendation`, campos `expected_impact`, `impacted_kpis`, `suggested_action`. | ¿Qué acción tiene mayor impacto económico? | Priorizar inversión o intervención. | Panel excelente para cierre: decisión, acción e impacto. | SHOW |
| `Riesgo que puede impactar el negocio` | bargauge | Ranking de riesgo por equipo. | `asset_risk`, `risk_score`. | ¿Qué riesgo técnico amenaza el negocio? | Priorizar activos críticos. | Redundante con master/mantenimiento, pero útil como resumen ejecutivo. | SUPPORT |
| `Confiabilidad` | row | Separador de KPIs MTBF, MTTR y detención. | Sin consulta. | ¿La solución mejora confiabilidad? | Defender reducción de fallas/downtime. | Conecta con KPIs explícitos del desafío. | SUPPORT |
| `MTBF, MTTR y detención no programada` | barchart | Confiabilidad y mantenibilidad en horas. | `kpi`, `mtbf_horas_demo`, `mttr_horas_demo`, `horas_detencion_no_programada`. | ¿Cuánto falla, cuánto tarda en repararse y cuánto detiene? | Medir mejora de mantenimiento. | Muy relevante para rúbrica y desafío; mostrar si hay tiempo. | SUPPORT |
| `Eficiencia global y recuperación` | timeseries | OEE y recuperación de condensado en el tiempo. | `kpi`, `oee`, `condensado_recuperado`. | ¿Eficiencia global y recuperación van juntas? | Ver si recuperación impacta desempeño. | Buen vínculo operación-finanzas, pero no esencial en 5 minutos. | SUPPORT |

## Síntesis final

### Paneles núcleo para la narrativa

Estos son los paneles que sostienen la demo principal sin dispersarse:

- `Tramo crítico en 10 segundos`
- `Ranking de tramos con razón, calidad y acción`
- `¿La eficiencia del circuito confirma la pérdida?`
- `¿Cuánto duele en costo agua/vapor?`
- `Humedad -> consumo -> MW`
- `Acción sobre biomasa`
- `Vapor FT_5101-1 vs condensado FT_3001`
- `Tabla operacional por TAG: área, equipo, medición, unidad y valor`
- `Evento pérdida vapor/condensado`
- `Acción recomendada del circuito`
- `OEE`
- `Costo operacional estimado`
- `Recomendaciones por impacto económico`

### Paneles redundantes

Hay redundancia útil, pero no hay que mostrarla toda:

- `Condensado recuperado` aparece en `water_steam_condensate.json`, `master.json` y `finance.json`.
- `Potencia actual` y tendencias de potencia aparecen en `master.json`, `operator.json`, `boiler_biomass.json` y `problem_first_operations.json`.
- `TemperaturaEscape` y `PresionDiferencial` aparecen en `boiler_biomass.json`, `operator.json`, `maintenance.json` y `master.json`.
- `asset_risk` por equipo aparece en casi todos los dashboards; para pitch conviene mostrarlo como tramo o como top riesgos que explican costo, no como ranking repetido.
- `maintenance_recommendation` aparece en vistas de problema, operador, mantenimiento, caldera y finanzas; elegí una tabla de recomendación según el momento de la historia.

### Paneles faltantes que fortalecerían el pitch

- Un panel explícito de **antes/después normal vs falla simulada** para mostrar impacto de la detección temprana durante la demo.
- Un panel de **calidad de datos global** con `% completitud`, `% variables con TAG` y `% variables integradas con energía`, pedido por el refinamiento.
- Un panel tipo **mapa operacional visual del ciclo** que represente `Desde -> Hasta` como proceso, no solo tabla. Si Grafana nativo limita esto, una tabla enriquecida o state timeline por tramo puede ser fallback.
- Un panel de **tiempo de respuesta del diagnóstico**: cuánto tarda el usuario en identificar el tramo crítico. Esto defendería mejor innovación y presentación.
- Un panel de **turno/operador/intervenciones** si se quiere probar reducción de dependencia del conocimiento individual. Hoy hay recomendaciones, pero no variables de turno u operador.

### Guía práctica para desarrollo

- No rompan el contrato de `segment_status`: es la base del enfoque por tramo y de los paneles más innovadores.
- Mantengan `from_node`, `to_node`, `fluid`, `tag`, `quality`, `status`, `impacted_problem`, `risk_score`, `reason`, `recommendation_link` y `cost_efficiency_impact` cuando refactoricen consultas.
- No eliminen TAGs reales como `FT_5101-1`, `FT_3001`, `FT_5001`, `FT_2101-1` y `FT_5002`; son evidencia de trazabilidad industrial.
- No conviertan recomendaciones en texto decorativo. `maintenance_recommendation` debe conservar causa, acción, plazo, impacto y estado.
- No mezclen demasiadas unidades en un solo panel salvo que la comparación sea explícita. Si se comparan `%`, `MW`, `t/h`, `m3/MWh` o costo, el título debe explicar la relación.
- No diseñen desde el widget. Primero definan la pregunta operacional, luego la métrica, después el panel.
- No muestren todos los dashboards en el pitch. En 5 minutos, más pantallas no significan más valor; significan menos claridad.

Mensaje central para el equipo: **cada panel debe existir porque permite tomar una decisión, no porque Grafana permita dibujarlo**.
