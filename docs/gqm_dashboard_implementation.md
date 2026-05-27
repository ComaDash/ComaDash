# Implementación GQM de dashboards COMASA

## Alcance implementado

El refinamiento GQM fue aplicado de forma aditiva: se crearon dashboards nuevos bajo `grafana/dashboards/` sin borrar, renombrar ni reducir los dashboards originales.

| Uso | Archivo | UID | Título | Tags clave |
|---|---|---|---|---|
| Entrada por problema operacional | `grafana/dashboards/gqm_problem_first_operations.json` | `gqm-problem-first-ops` | `GQM - COMASA Problem-First Operations` | `COMASA`, `GQM`, `problemas`, `segmentos`, `decision` |
| Evidencia agua-vapor-condensado | `grafana/dashboards/gqm_water_steam_condensate.json` | `gqm-water-steam-cond` | `GQM - COMASA Water Steam Condensate Decisions` | `COMASA`, `GQM`, `agua`, `vapor`, `condensado` |
| Causa raíz biomasa/caldera | `grafana/dashboards/gqm_boiler_biomass.json` | `gqm-boiler-biomass` | `GQM - COMASA Biomass Boiler Efficiency` | `COMASA`, `GQM`, `caldera`, `biomasa`, `eficiencia` |
| Riesgo y mantenimiento predictivo | `grafana/dashboards/gqm_maintenance.json` | `gqm-maintenance-risk` | `GQM - COMASA Predictive Maintenance Risk` | `COMASA`, `GQM`, `mantencion`, `riesgo` |
| Cierre ejecutivo-financiero | `grafana/dashboards/gqm_finance.json` | `gqm-finance-impact` | `GQM - COMASA Executive Financial Impact` | `COMASA`, `GQM`, `finanzas`, `impacto` |
| Demo compacta de 5 minutos | `grafana/dashboards/gqm_comasa_decision_narrative.json` | `gqm-decision-narrative` | `GQM - COMASA Decision Narrative` | `COMASA`, `GQM`, `narrativa`, `pitch`, `decision` |

## Ruta demo recomendada

Para pitch o revisión ejecutiva, abrir directamente **`GQM - COMASA Decision Narrative`** en Grafana. La ruta compacta evita recorrer dashboards grandes y cuenta la historia completa:

1. `Tramo crítico ahora`: decide qué tramo revisar primero.
2. `Ranking GQM de tramos: causa, calidad y acción`: muestra causa, calidad, TAG, unidad y acción recomendada.
3. `Eficiencia agua-vapor-condensado` y `Costo del circuito térmico`: valida si la pérdida técnica tiene impacto económico.
4. `Biomasa húmeda: consumo y MW`: explica la relación causal entre combustible, consumo y generación.
5. `Acciones recomendadas por impacto`: convierte evidencia en intervención preventiva.
6. `Energía generada`, `OEE` y `Costo operacional estimado`: cierra con impacto ejecutivo.

Si una pregunta requiere detalle, usar los otros dashboards `GQM - ...` como drill-down, no como recorrido principal.

## Mapeo planned vs actual de títulos de panel

Durante la implementación se detectaron títulos planificados que no existían literalmente en los dashboards fuente. No se crearon ni renombraron paneles para forzar el plan; se preservaron paneles existentes y se documentó la equivalencia.

| Título planificado | Estado real | Cobertura actual |
|---|---|---|
| `Tramo crítico en 10 segundos` | Existía en la guía histórica, pero no como panel literal en los duplicados GQM actuales. | Cubierto por `Ranking de tramos con razón, calidad y acción` en `gqm_problem_first_operations.json` y por `Tramo crítico ahora` en `gqm_comasa_decision_narrative.json`. |
| `Energía, costo y eficiencia operacional` | No existe como panel único. | Separado en `Energía generada`, `Eficiencia energética` y `Costo operacional estimado` en `gqm_problem_first_operations.json`; el dashboard compacto cierra con `Energía generada`, `OEE` y `Costo operacional estimado`. |
| `Top riesgos que explican el costo` | No existe con ese título literal. | Cubierto por `Riesgo que puede impactar el negocio` en `gqm_finance.json`. |
| `Valores actuales por TAG crítico` | No existe como barchart literal. | Cubierto por `Tabla operacional por TAG: área, equipo, medición, unidad y valor` en `gqm_water_steam_condensate.json`. |

## Mitigaciones aplicadas

- **No destructivo**: los originales `problem_first_operations.json`, `water_steam_condensate.json`, `boiler_biomass.json`, `maintenance.json` y `finance.json` siguen existiendo.
- **Identidad GQM clara**: todos los nuevos dashboards tienen título `GQM - ...` y/o tag `GQM`; los duplicados tienen UID propio e `id: null`.
- **Sin plugins extra**: el dashboard compacto usa solo tipos nativos observados en Grafana: `row`, `stat`, `table`, `timeseries` y `gauge`.
- **Descripciones accionables**: los paneles no-row del compacto tienen `Goal`, `Question`, `Metric`, `Decision` y `Action` en `description`.
- **Unidades mixtas explícitas**: paneles causales como `Eficiencia agua-vapor-condensado` y `Biomasa húmeda: consumo y MW` declaran que son relación causal, no comparación homogénea de magnitudes.
- **Demo/prototipo responsable**: costos demo o métricas derivadas se presentan desde las mediciones existentes (`kpi`, `segment_status`, `telemetry_raw`, `maintenance_recommendation`) sin afirmar ML productivo no evidenciado.

## Métricas futuras / Batch E opcional

- `diagnosis_time_demo`: tiempo desde abrir el dashboard hasta identificar tramo, causa y acción.
- `data_quality`: completitud por TAG crítico, porcentaje de variables con unidad y porcentaje de puntos con calidad/confianza suficiente.
- `scenario_comparison`: comparación normal vs falla con fuente real antes de quitar etiquetas demo/simulado.
- `decision_support_count`: cantidad de recomendaciones generadas, reconocidas y cerradas.
- Variables de turno, setpoint e intervención ejecutada para medir reducción de dependencia del conocimiento individual.
- Métricas reales de backlog preventivo y efectividad posterior a la acción antes de convertir la narrativa en KPI productivo.

## Rollback seguro

Como el cambio es aditivo, el rollback consiste en retirar únicamente los archivos `grafana/dashboards/gqm_*.json` y esta documentación GQM. No se debe tocar ni eliminar ningún dashboard original.
