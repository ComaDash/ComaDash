# Skill: GQM Dashboard Refinement Agent

## Propósito

Refinar dashboards y paneles de Grafana evaluando si cada visualización responde a una necesidad real del proyecto, si permite tomar decisiones operacionales y si está alineada con el modelo GQM: **Goal, Question, Metric**.

Esta skill debe evitar dashboards decorativos o técnicos sin propósito claro. Cada panel debe justificar:

- Qué objetivo apoya.
- Qué pregunta responde.
- Qué métrica muestra.
- Qué decisión habilita.
- Qué acción permite ejecutar.

---

## Cuándo usar esta skill

Usa esta skill cuando el usuario quiera:

- Refinar dashboards existentes.
- Evaluar si un panel de Grafana aporta valor.
- Diseñar nuevas vistas operacionales.
- Convertir dolores del negocio en métricas.
- Detectar paneles redundantes, confusos o innecesarios.
- Mejorar dashboards para pitch, demo o implementación.
- Verificar si las visualizaciones permiten medir innovación o impacto.
- Revisar si un dashboard responde realmente a las necesidades del proyecto.

---

## Entrada esperada

El agente puede recibir uno o más de estos elementos:

- Descripción del proyecto.
- Dolor operacional identificado.
- Capturas o descripción de paneles de Grafana.
- Variables disponibles.
- Métricas actuales.
- Feedback del equipo.
- Objetivos del pitch o demo.
- Datos históricos, energéticos u operacionales.
- Restricciones técnicas.
- Arquitectura de datos disponible.
- Descripción del proceso industrial.
- Hipótesis de valor de la solución.

---

## Marco de análisis obligatorio

Para cada dashboard o panel, el agente debe aplicar esta cadena:

```txt
Dolor → Goal → Question → Metric → Panel → Decisión → Acción
```

Nunca debe evaluar un panel solo por estética, cantidad de gráficos o volumen de datos mostrados.

---

## Principio central

Un panel no es bueno porque tenga muchos datos.

Un panel es bueno si responde:

```txt
¿Qué necesito saber?
¿Por qué importa?
¿Cómo lo mido?
¿Qué decisión habilita?
¿Qué pasa si no lo mido?
```

---

# Proceso de refinamiento

## 1. Identificar el dolor operacional

Primero, el agente debe determinar qué problema intenta abordar el dashboard.

Ejemplos de dolores:

- Pérdida de agua.
- Variabilidad de biomasa.
- Degradación térmica.
- Dependencia del operador.
- Baja integración entre datos históricos, energéticos y operacionales.
- Falta de medición de innovación.
- Dificultad para explicar el proceso en una sola vista.
- Exceso de datos sin interpretación.
- Falta de alertas accionables.
- Desconexión entre variables operacionales y variables de negocio.

Formato de salida:

```md
## Dolor identificado

[Descripción clara del dolor]

## Impacto del dolor

[Consecuencia operacional, económica, energética, estratégica o técnica]
```

---

## 2. Formular el Goal GQM

El agente debe transformar el dolor en un objetivo medible.

Formato recomendado:

```txt
Analizar [objeto/proceso]
con el propósito de [mejorar/reducir/detectar/optimizar]
respecto a [foco de calidad]
desde el punto de vista de [operador/jefe de planta/equipo técnico/gerencia]
en el contexto de [proceso/planta/proyecto].
```

Ejemplo:

```txt
Analizar el comportamiento térmico y energético del proceso
con el propósito de detectar desviaciones operacionales
respecto a eficiencia, estabilidad y consumo energético
desde el punto de vista del equipo operacional y técnico
en el contexto de la operación industrial de COMASA.
```

---

## 3. Derivar preguntas críticas

El agente debe convertir cada Goal en preguntas que el dashboard debe responder.

Buenas preguntas son:

- Operacionales.
- Medibles.
- Accionables.
- Comprensibles para alguien no técnico.
- Directamente conectadas con una decisión.
- Relevantes para el dolor identificado.

Ejemplos:

```md
## Preguntas GQM

1. ¿Dónde se concentra la mayor pérdida de agua?
2. ¿Qué variables anticipan una desviación energética?
3. ¿Cuándo la biomasa empieza a comportarse fuera de lo esperado?
4. ¿Qué diferencias aparecen entre turnos u operadores?
5. ¿Qué proceso consume más tiempo o energía?
6. ¿Qué pasa si esta variable no se mide?
7. ¿Qué variable explica mejor la pérdida de eficiencia?
8. ¿Qué condición operacional se repite antes de una anomalía?
9. ¿Qué indicador permite detectar deterioro antes de que afecte la producción?
10. ¿Qué dato permite justificar el valor de la solución?
```

---

## 4. Asociar métricas

Cada pregunta debe tener una métrica asociada.

Formato obligatorio:

```md
## Pregunta

[Pregunta que el panel debe responder]

## Métrica

[Nombre de la métrica]

## Tipo de métrica

- Resultado
- Proceso
- Diagnóstico
- Predictiva
- Innovación
- Riesgo
- Eficiencia
- Calidad operacional

## Fuente

[Sensor, base de datos, histórico, simulador, cálculo, integración externa, operador, archivo manual, API, etc.]

## Frecuencia

[Tiempo real, cada minuto, por turno, diaria, semanal, mensual]

## Interpretación

[Cómo se debe leer la métrica]

## Acción

[Qué decisión permite tomar]
```

---

# Evaluación de paneles de Grafana

Para cada panel, el agente debe aplicar esta checklist:

```md
# Evaluación del panel: [Nombre del panel]

## 1. Objetivo

¿A qué Goal responde?

## 2. Pregunta

¿Qué pregunta operacional responde?

## 3. Métrica

¿Qué métrica muestra?

## 4. Decisión

¿Qué decisión permite tomar?

## 5. Acción

¿Qué acción concreta habilita?

## 6. Usuario objetivo

¿Quién debería usar este panel?

- Operador
- Jefe de turno
- Equipo técnico
- Gerencia
- Equipo de innovación
- Equipo de mantenimiento
- Equipo de datos

## 7. Nivel de utilidad

- Alto
- Medio
- Bajo

## 8. Problemas detectados

- Métrica poco clara
- Panel sin pregunta
- Exceso de variables
- Falta de contexto
- No hay umbrales
- No permite comparar
- No permite actuar
- Visualización incorrecta
- Falta integración con otras variables
- No muestra tendencia
- No muestra estado esperado vs estado real
- No diferencia condiciones normales y anómalas
- No tiene una acción asociada

## 9. Recomendación

- Mantener
- Refinar
- Fusionar
- Dividir
- Eliminar
- Convertir en alerta
- Convertir en vista ejecutiva
- Convertir en panel diagnóstico
- Convertir en panel predictivo
```

---

# Escala de evaluación

Cada panel debe recibir una nota de 1 a 5:

```md
1 = Panel decorativo o sin utilidad clara.
2 = Muestra datos, pero no responde una pregunta operacional.
3 = Responde parcialmente una pregunta, pero falta contexto o acción.
4 = Responde una pregunta clara y permite interpretar el estado del proceso.
5 = Responde una pregunta crítica, permite decidir y está conectado con una acción o alerta.
```

---

# Criterios de calidad para dashboards

## 1. Claridad

El dashboard debe responder rápidamente:

```txt
¿Qué está pasando?
¿Dónde está pasando?
¿Por qué importa?
¿Qué hago ahora?
```

---

## 2. Trazabilidad GQM

Cada panel debe tener:

```txt
Goal asociado
Pregunta asociada
Métrica asociada
Decisión asociada
Acción asociada
```

Si un panel no puede justificar eso, debe ser refinado o eliminado.

---

## 3. Acción operacional

Un panel útil no solo muestra datos. Debe activar una decisión.

Ejemplo malo:

```txt
Temperatura promedio
```

Ejemplo mejor:

```txt
Temperatura vs rango operacional esperado, con alerta de desviación y posible impacto energético.
```

---

## 4. Contexto

La métrica debe tener referencia:

- Valor actual.
- Valor esperado.
- Umbral.
- Histórico.
- Comparación por turno.
- Comparación por condición operacional.
- Tendencia.
- Estado normal/anómalo.
- Impacto potencial.
- Recomendación de acción.

---

## 5. Relación entre variables

Evitar paneles aislados cuando el dolor depende de múltiples factores.

Ejemplo:

```txt
No mostrar solo humedad de biomasa.
Relacionar humedad + consumo energético + temperatura + rendimiento.
```

---

## 6. Una vista debe responder una pregunta

Cada vista principal debe ser diseñada alrededor de una pregunta fuerte.

Ejemplo:

```txt
¿Dónde se pierde eficiencia operacional?
```

No alrededor de una lista de sensores.

---

# Tipos de paneles recomendados

## Panel 1: Vista ejecutiva de salud operacional

### Pregunta

```txt
¿La operación está dentro de condiciones esperadas?
```

### Métricas

- Estado general del proceso.
- Consumo energético relativo.
- Pérdida estimada de agua.
- Desviaciones críticas.
- Alertas activas.
- Índice de estabilidad operacional.
- Índice de eficiencia operacional.
- Riesgo operacional actual.

### Uso

```txt
Ideal para pitch, gerencia y vista inicial del dashboard.
```

---

## Panel 2: Mapa de proceso

### Pregunta

```txt
¿Qué etapa del proceso concentra mayor tiempo, pérdida o consumo?
```

### Visualización recomendada

- Diagrama de proceso.
- Bloques por etapa.
- Ancho del bloque según duración.
- Color según criticidad.
- Tooltip con métricas clave.
- Indicadores de desviación por etapa.
- Comparación entre estado real y esperado.

### Métricas

- Tiempo por etapa.
- Consumo por etapa.
- Desviación por etapa.
- Pérdida estimada por etapa.
- Eficiencia por etapa.
- Eventos críticos por etapa.

### Uso

```txt
Permite explicar el sistema completo en una sola vista.
```

---

## Panel 3: Variabilidad de biomasa

### Pregunta

```txt
¿Cómo afecta la biomasa al comportamiento operacional?
```

### Métricas

- Humedad.
- Temperatura.
- Poder calorífico estimado.
- Tasa de alimentación.
- Variabilidad por lote.
- Impacto energético asociado.
- Desviación respecto al comportamiento histórico.
- Relación entre tipo de biomasa y estabilidad del proceso.

### Recomendación

```txt
No mostrar biomasa como dato aislado.
Relacionarla con eficiencia, energía, temperatura, rendimiento y estabilidad.
```

---

## Panel 4: Pérdida de agua

### Pregunta

```txt
¿Cuándo y dónde aumenta la pérdida de agua?
```

### Métricas

- Agua ingresada.
- Agua recuperada.
- Agua evaporada estimada.
- Diferencia entre balance esperado y real.
- Eventos de fuga o desviación.
- Tendencia por turno.
- Pérdida acumulada.
- Pérdida por etapa.
- Pérdida relativa respecto a producción.

### Acción habilitada

```txt
Detectar condiciones anómalas y priorizar investigación operacional.
```

---

## Panel 5: Energía y eficiencia

### Pregunta

```txt
¿Qué condiciones operacionales aumentan el consumo energético?
```

### Métricas

- kWh por tonelada.
- Vapor por tonelada.
- Temperatura vs consumo.
- Consumo por etapa.
- Desviación respecto al histórico.
- Eficiencia térmica estimada.
- Consumo específico por régimen operacional.
- Costo energético estimado.
- Energía desperdiciada estimada.

### Acción habilitada

```txt
Identificar configuraciones operacionales ineficientes y priorizar optimización.
```

---

## Panel 6: Dependencia del operador

### Pregunta

```txt
¿Qué decisiones cambian según el operador o turno?
```

### Métricas

- Variabilidad de setpoints.
- Cambios manuales.
- Tiempo fuera de rango.
- Diferencias entre turnos.
- Respuesta ante alertas.
- Número de intervenciones.
- Tiempo hasta corrección.
- Frecuencia de ajustes manuales.
- Desviación operacional por turno.

### Uso

```txt
Este panel debe tratar el problema como dependencia del conocimiento operacional, no como evaluación personal del operador.
```

---

## Panel 7: Integración histórico-operacional-energética

### Pregunta

```txt
¿Qué relaciones aparecen al cruzar datos históricos, operacionales y energéticos?
```

### Métricas

- Correlación entre variables críticas.
- Eventos repetidos.
- Condiciones previas a fallas.
- Patrones por turno.
- Patrones por tipo de biomasa.
- Patrones por régimen operacional.
- Asociación entre consumo energético y condiciones del proceso.
- Asociación entre pérdida de agua y temperatura.
- Asociación entre biomasa y eficiencia.

### Uso

```txt
Sirve para demostrar el valor de integrar datos que antes estaban dispersos.
```

---

## Panel 8: Medición de innovación

### Pregunta

```txt
¿Qué valor nuevo permite generar la solución que antes no se podía medir?
```

### Métricas

- Nuevas variables integradas.
- Nuevas relaciones detectadas.
- Tiempo reducido para diagnosticar problemas.
- Número de decisiones apoyadas por datos.
- Número de alertas accionables.
- Reducción de incertidumbre operacional.
- Capacidad de anticipar desviaciones.
- Nivel de trazabilidad entre variables.

### Uso

```txt
Sirve para demostrar que la propuesta no solo visualiza datos, sino que mejora la capacidad de decisión.
```

---

# Reglas para criticar paneles existentes

El agente debe ser directo, pero constructivo.

Formato recomendado:

```md
Este panel es útil porque [razón].

Sin embargo, actualmente responde más a [dato mostrado] que a [decisión requerida].

Para alinearlo con el proyecto, debería transformarse en [propuesta].
```

Ejemplo:

```md
El panel de temperatura es útil porque muestra una variable crítica del proceso.

Sin embargo, actualmente solo informa el valor histórico, pero no permite saber si la operación está en riesgo.

Para alinearlo con el proyecto, debería incluir rango esperado, umbral de desviación, relación con consumo energético y eventos fuera de rango.
```

---

# Señales de que un panel debe eliminarse o fusionarse

Un panel debe ser eliminado, fusionado o rediseñado si:

- No responde una pregunta clara.
- Solo repite una métrica ya mostrada en otro panel.
- No tiene usuario objetivo.
- No tiene umbral ni interpretación.
- No permite comparar.
- No permite decidir.
- No se conecta con ningún dolor del proyecto.
- No se puede explicar en el pitch.
- Requiere demasiado contexto técnico para entenderlo.
- Muestra datos sin impacto operacional.
- No diferencia entre estado normal y estado problemático.

---

# Señales de que un panel debe convertirse en alerta

Un panel debe convertirse en alerta si:

- Representa una condición crítica.
- Tiene un umbral claro.
- Requiere acción rápida.
- El usuario no necesita mirar constantemente el gráfico.
- El valor solo importa cuando sale de rango.
- La desviación tiene impacto operacional, energético o económico.

Ejemplos:

```txt
Temperatura fuera de rango.
Pérdida de agua sobre umbral.
Consumo energético anómalo.
Variabilidad excesiva de biomasa.
Tiempo prolongado fuera de condición esperada.
```

---

# Señales de que un panel debe convertirse en vista ejecutiva

Un panel debe convertirse en vista ejecutiva si:

- Resume el estado general del proceso.
- Permite explicar valor en menos de 30 segundos.
- Muestra impacto operacional o económico.
- Agrupa varias métricas críticas.
- Sirve para gerencia, pitch o toma de decisiones rápida.

---

# Salida final esperada

El agente debe entregar una tabla como esta:

| Panel | Goal | Pregunta | Métrica | Decisión | Evaluación | Acción recomendada |
|---|---|---|---|---|---|---|
| Temperatura proceso | Detectar desviaciones térmicas | ¿Está el proceso fuera de rango? | Temperatura vs umbral | Ajustar operación | 3/5 | Agregar rangos, alertas y relación con energía |
| Humedad biomasa | Controlar variabilidad | ¿La biomasa afecta el rendimiento? | Humedad + consumo energético | Ajustar alimentación | 4/5 | Cruzar con energía y rendimiento |
| Consumo energético | Mejorar eficiencia | ¿Qué consume más energía? | kWh/ton | Optimizar operación | 4/5 | Separar por etapa y turno |

---

# Diagnóstico final obligatorio

Después de evaluar los paneles, el agente debe cerrar con:

```md
## Diagnóstico general

El dashboard actualmente está en nivel:
[Exploratorio / Operacional / Analítico / Predictivo / Ejecutivo]

## Fortalezas

- [Fortaleza 1]
- [Fortaleza 2]
- [Fortaleza 3]

## Debilidades

- [Debilidad 1]
- [Debilidad 2]
- [Debilidad 3]

## Brechas GQM

- [Objetivos sin métricas]
- [Preguntas sin panel]
- [Métricas sin decisión]
- [Paneles sin acción]
- [Dolores no representados]
- [Variables sin integración]

## Prioridad de mejora

1. [Mejora más importante]
2. [Segunda mejora]
3. [Tercera mejora]

## Conclusión

[Resumen claro sobre si el dashboard cumple o no con lo que necesita el proyecto]
```

---

# Formato de respuesta recomendado

Cuando el agente refine un dashboard, debe responder con esta estructura:

```md
# Refinamiento GQM del dashboard

## 1. Resumen del objetivo del dashboard

[Explicación breve]

## 2. Dolores operacionales cubiertos

- [Dolor 1]
- [Dolor 2]
- [Dolor 3]

## 3. Dolores no cubiertos

- [Dolor no cubierto 1]
- [Dolor no cubierto 2]

## 4. Evaluación por panel

| Panel | Pregunta que responde | Métrica principal | Problema detectado | Nota | Recomendación |
|---|---|---|---|---|---|

## 5. Brechas GQM

| Goal | Pregunta faltante | Métrica faltante | Panel sugerido |
|---|---|---|---|

## 6. Paneles recomendados

- [Panel recomendado 1]
- [Panel recomendado 2]
- [Panel recomendado 3]

## 7. Acciones concretas para Grafana

- [Acción 1]
- [Acción 2]
- [Acción 3]

## 8. Diagnóstico final

[Conclusión]
```

---

# Aplicación específica al proyecto COMASA

Cuando el contexto sea COMASA, el agente debe considerar los siguientes dolores como base posible:

## Dolor 1: Pérdida de agua

Posibles preguntas:

- ¿Dónde se concentra la pérdida de agua?
- ¿Cuándo aumenta la pérdida?
- ¿Qué condiciones operacionales se asocian a pérdida anómala?
- ¿La pérdida parece asociarse a fuga, evaporación o balance operacional?

Posibles métricas:

- Agua ingresada.
- Agua recuperada.
- Agua evaporada estimada.
- Diferencia entre balance esperado y real.
- Pérdida acumulada.
- Pérdida por turno.
- Pérdida por etapa.

---

## Dolor 2: Variabilidad de biomasa

Posibles preguntas:

- ¿La biomasa se comporta de manera estable?
- ¿Qué propiedades de la biomasa explican variaciones operacionales?
- ¿Cómo cambia el consumo energético según la biomasa?
- ¿Qué lotes generan mayor inestabilidad?

Posibles métricas:

- Humedad.
- Granulometría, si existe.
- Poder calorífico estimado.
- Tasa de alimentación.
- Variabilidad por lote.
- Impacto energético.
- Temperatura asociada.
- Rendimiento asociado.

---

## Dolor 3: Posibles degradaciones térmicas

Posibles preguntas:

- ¿Hay señales de pérdida de eficiencia térmica?
- ¿Qué condiciones anteceden una degradación?
- ¿La calidad del agua de pozo se relaciona con problemas térmicos?
- ¿Qué variables indican incrustación, pérdida de transferencia o deterioro?

Posibles métricas:

- Temperatura de entrada y salida.
- Diferencial térmico.
- Conductividad del agua, si existe.
- Caída de eficiencia.
- Consumo energético adicional.
- Eventos fuera de rango.
- Tendencia de rendimiento térmico.

---

## Dolor 4: Dependencia del conocimiento operacional

Posibles preguntas:

- ¿Qué decisiones dependen más del operador de turno?
- ¿Qué diferencias existen entre turnos?
- ¿Qué acciones manuales se repiten antes de estabilizar el proceso?
- ¿Qué conocimiento tácito puede transformarse en regla, alerta o recomendación?

Posibles métricas:

- Cambios manuales.
- Variabilidad de setpoints.
- Tiempo fuera de rango.
- Tiempo hasta corrección.
- Diferencia entre turnos.
- Frecuencia de intervención.
- Eventos corregidos manualmente.

---

## Dolor 5: Baja integración de datos históricos, energéticos y operacionales

Posibles preguntas:

- ¿Qué relaciones aparecen al cruzar datos antes separados?
- ¿Qué variables explican el consumo energético?
- ¿Qué patrones históricos anticipan problemas?
- ¿Qué variables deberían visualizarse juntas?

Posibles métricas:

- Correlación entre variables.
- Consumo energético por condición operacional.
- Eventos repetidos.
- Patrones por turno.
- Patrones por biomasa.
- Patrones por etapa.
- Variables críticas integradas.

---

## Dolor 6: Enfoque reactivo ante fallas y paradas no programadas

Posibles preguntas:

- ¿Cuándo ocurrirá la próxima parada crítica si mantenemos las condiciones actuales?
- ¿Qué tan probable es que el ensuciamiento de la caldera (fouling) afecte la potencia en el próximo turno?
- ¿Cómo impactará la variabilidad de la biomasa actual en la generación de vapor de las próximas horas?
- ¿Qué señales de vibración o temperatura anticipan una falla mecánica en turbinas o bombas?
- ¿Cuál es la causa probable de una desviación térmica detectada antes de que genere una alarma de seguridad?
- ¿Qué acciones de mantenimiento preventivo evitarían una detención no programada esta semana?

Posibles métricas:

- MTBF (Mean Time Between Failures): Tiempo medio entre fallas para medir confiabilidad.
- MTTR (Mean Time To Repair): Tiempo medio de reparación para medir mantenibilidad.
- Score de Anomalía: Índice (z-score o similar) que detecta desviaciones del comportamiento histórico normal.
- Horas de detención no programada: Tiempo improductivo que la predicción busca reducir.
- Probabilidad de falla por activo: Porcentaje de riesgo estimado para equipos críticos (caldera, turbina, bombas).
- Costo de mantenimiento evitado: Impacto económico ahorrado al intervenir de forma predictiva vs. correctiva.
- Eficiencia predictiva: Ratio de detecciones tempranas confirmadas frente a fallas reales.
- Recomendaciones de mantenimiento activas: Sugerencias automáticas generadas por el motor de reglas (ej: "programar limpieza de caldera por drift térmico").

---

# Checklist final de validación

Antes de aprobar un dashboard, el agente debe verificar:

```md
## Checklist GQM

- [ ] Cada panel tiene un Goal explícito.
- [ ] Cada panel responde una pregunta operacional.
- [ ] Cada panel tiene una métrica principal.
- [ ] Cada métrica tiene una fuente de datos clara.
- [ ] Cada métrica tiene interpretación.
- [ ] Cada panel permite tomar una decisión.
- [ ] Cada panel tiene usuario objetivo.
- [ ] Existen umbrales o rangos esperados.
- [ ] Se diferencia estado normal de estado anómalo.
- [ ] Se cruzan variables cuando el dolor lo requiere.
- [ ] Hay al menos una vista ejecutiva.
- [ ] Hay al menos una vista operacional.
- [ ] Hay al menos una vista diagnóstica.
- [ ] El dashboard permite explicar valor en el pitch.
- [ ] El dashboard permite medir impacto o innovación.
```

---

# Instrucción final para el agente

Cuando uses esta skill, no te limites a describir los paneles.

Debes juzgar si cumplen o no cumplen con el proyecto.

La evaluación debe ser crítica, accionable y orientada a mejorar el dashboard.

Siempre debes cerrar con:

```txt
¿El dashboard permite tomar mejores decisiones que antes?
¿Permite medir el valor de la propuesta?
¿Hace visible un dolor operacional real?
¿Qué panel falta para que el proyecto sea más convincente?
```
