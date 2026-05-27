# Refinamiento de Propuesta Dashboard Operacional COMASA

## 1. Propósito del documento

Este documento consolida el refinamiento conceptual y técnico de la propuesta de dashboard operacional para Planta COMASA, con foco en el ciclo **agua – vapor – condensado** y su relación con variables energéticas, biomasa, operación y calidad de datos.

El objetivo es que este archivo sirva como referencia dentro del repositorio de GitHub para orientar la implementación actual en Grafana y evitar que el desarrollo derive en un dashboard meramente visual, sin una unidad de análisis clara ni capacidad real de responder preguntas operacionales.

La propuesta parte de una base existente: actualmente ya existe una implementación en **Grafana con datos funcionando**. Sin embargo, se requiere refinar el enfoque para transformar esos datos en una representación operacional útil, escalable y orientada a decisiones.

---

## 2. Idea central de la propuesta

La propuesta no consiste solamente en mostrar variables en gráficos.

La propuesta consiste en transformar mediciones dispersas del ciclo agua–vapor–condensado en una **representación visual del proceso**, donde cada tramo operacional sea una entidad de primera categoría.

> Nuestra propuesta transforma mediciones dispersas del ciclo agua–vapor–condensado en una representación visual del proceso, donde cada tramo operacional es una entidad de primera categoría. Esto permite detectar pérdidas de agua, variabilidad térmica/energética, dependencia operacional y baja integración de datos en una sola vista escalable.

---

## 3. Problema actual

A partir del análisis del proceso y del feedback recibido, los principales problemas identificados son:

1. **Demasiada pérdida de agua**
   - Asociada posiblemente a fugas, evaporación, purgas, baja recuperación de condensado o desbalances no visibles.

2. **Variabilidad en el comportamiento de la biomasa**
   - La biomasa utilizada no siempre se comporta de la misma manera.
   - Esto puede impactar la generación de vapor, estabilidad térmica, presión y producción energética.

3. **Posibles degradaciones térmicas asociadas al agua de pozo**
   - El origen y calidad del agua puede influir en el rendimiento térmico, incrustaciones, transferencia de calor o eficiencia del tratamiento.

4. **Dependencia del conocimiento operacional de los operadores**
   - Parte importante del diagnóstico depende del operador de turno.
   - El conocimiento existe, pero no está suficientemente sistematizado ni representado en datos.

5. **Baja integración entre variables operacionales históricas y energéticas**
   - Existen múltiples fuentes de datos.
   - Las variables de agua, vapor, condensado, biomasa, energía, turnos y operación no están integradas de forma suficiente.
   - Actualmente parte de esta agrupación depende de terceros o de análisis manuales.

---

## 4. Consecuencia de no resolver el problema

Si no existe una representación integrada del proceso, la planta no puede responder rápidamente preguntas críticas sobre su operación.

La consecuencia de no contar con esta representación es:

- No saber con claridad dónde se pierde agua.
- No distinguir entre variabilidad normal y anomalía operacional.
- No relacionar de forma directa biomasa con vapor y generación eléctrica.
- No saber qué variables impactan realmente la eficiencia energética.
- Mantener dependencia excesiva del criterio del operador de turno.
- Seguir revisando múltiples planillas, dashboards o fuentes sin una lectura operacional unificada.
- No poder medir si la propuesta mejora realmente la toma de decisiones.

> No medir la propuesta implica no poder distinguir entre un dashboard decorativo y una herramienta real de diagnóstico operacional.

---

## 5. Pregunta clave de la propuesta

La pregunta general que debe guiar el desarrollo es:

> ¿Dónde, cuándo y bajo qué condiciones se pierde eficiencia en el ciclo agua–vapor–condensado de COMASA?

Esta pregunta se divide en preguntas operacionales más específicas:

1. ¿Dónde se está perdiendo agua?
2. ¿Qué tramo del proceso presenta mayor desviación?
3. ¿Qué variables térmicas cambian cuando cambia la biomasa?
4. ¿Qué comportamiento depende demasiado del operador?
5. ¿Qué variables operacionales no están integradas con energía?
6. ¿Qué sensores o TAG tienen datos faltantes, inconsistentes o poco trazables?
7. ¿Qué tramo debería revisar primero el usuario al abrir el dashboard?

---

## 6. Unidad de análisis: tramo operacional

El feedback recibido destaca la importancia de representar la entidad principal del problema como un **first class citizen**.

En este caso, la entidad principal no debe ser una variable aislada, como flujo, presión o temperatura.

La unidad de análisis propuesta es:

# Tramo operacional del proceso

Un tramo operacional se define como:

```text
Desde → Hasta + Fluido + Unidad Generadora + Condición de carga + Variable medida + TAG + Medición
```

Ejemplo:

```text
Estanque Agua Alimentación → ECO I
Fluido: Agua de alimentación
Unidad: UG_1
Condición: MT
Variable: Flujo
Medición: 49,7 ton/h
TAG: FT_2101-1
```

La fila del dataset deja de ser solamente un dato tabular y pasa a ser una entidad consultable:

> El tramo Estanque Agua Alimentación → ECO I, para Agua de Alimentación, en UG_1_MT, tiene un flujo de 49,7 ton/h medido por FT_2101-1.

Esto permite formular preguntas como:

> ¿Este tramo está transportando suficiente agua para la carga actual de generación?

---

## 7. Modelo de dominio propuesto

Para implementar correctamente el dashboard, se recomienda construir un modelo de dominio base.

### 7.1 Entidades principales

| Entidad | Descripción |
|---|---|
| Planta | Contexto general de COMASA. |
| Unidad generadora | UG_1, UG_2 u otras unidades futuras. |
| Bloque o condición operacional | MT, BL1, BL2 u otros estados/cargas. |
| Tramo operacional | Conexión desde un punto del proceso hacia otro. |
| Equipo | Pozo, estanque, osmosis, desaireador, economizador, domo, sobrecalentador, turbina, condensador, torre, etc. |
| Fluido | Agua industrial, agua desmineralizada, agua de alimentación, vapor saturado, vapor sobrecalentado, condensado, agua de refrigeración. |
| Variable | Flujo, presión, temperatura, nivel, carga, conductividad, pH, humedad, energía. |
| Instrumento / TAG | Sensor o identificador de medición. |
| Medición | Valor medido en un instante o período. |
| Biomasa | Tipo, lote, humedad, consumo, poder calorífico. |
| Operación | Turno, operador, setpoint, intervención, alarma. |
| Energía | MW, MWh, carga, eficiencia, consumo específico. |

### 7.2 Relaciones principales

```text
Planta
 └── Unidad Generadora
      └── Condición Operacional
           └── Tramo Operacional
                ├── Desde Equipo
                ├── Hasta Equipo
                ├── Fluido
                ├── Variable
                ├── TAG
                ├── Medición
                ├── Estado operacional
                └── Impacto energético
```

La implementación en Grafana debería intentar respetar esta estructura lógica aunque las tablas internas o consultas estén distribuidas.

---

## 8. Representación visual principal

La primera vista del dashboard debe responder inmediatamente:

> ¿Qué tramo del proceso está más comprometido ahora?

Para eso, se propone una vista tipo **mapa operacional del ciclo agua–vapor–condensado**.

### 8.1 Representación recomendada

Cada tramo se representa como un bloque o conexión:

```text
Pozo → Captación → Tratamiento/Osmosis → Agua Permeada → Desaireador → Economizador → Domo → Sobrecalentador → Turbina → Condensador → Retorno
```

Cada bloque o tramo debe tener información visual:

| Elemento visual | Significado |
|---|---|
| Color | Estado operacional: normal, atención, crítico. |
| Ancho | Tiempo de proceso, magnitud del flujo o criticidad. |
| Tamaño | Volumen, flujo o impacto relativo. |
| Borde punteado | Dato faltante, poco confiable o sin TAG. |
| Ícono de sensor | Existe TAG asociado. |
| Opacidad baja | Variable no integrada al histórico. |
| Tooltip | Detalle: valor, unidad, TAG, timestamp, estado, fuente. |

### 8.2 Tres colores base

| Color | Estado | Criterio sugerido |
|---|---|---|
| Verde | Normal | Dentro del rango esperado. |
| Amarillo | Atención | Desviación moderada, dato incompleto o comportamiento inestable. |
| Rojo | Crítico | Desviación alta, pérdida probable, dato clave ausente o anomalía severa. |

Ejemplo de regla:

```text
Si el valor actual se desvía más de 15% del promedio histórico para esa condición de carga → amarillo.
Si se desvía más de 30% → rojo.
Si el dato falta y es una variable crítica → amarillo o rojo según criticidad.
```

---

## 9. Vistas principales del dashboard

El dashboard no debe tener muchas vistas desconectadas. Debe tener pocas vistas, pero orientadas a responder preguntas críticas.

---

### Vista 1: Mapa operacional del ciclo

**Pregunta que responde:**

> ¿Dónde está el problema ahora?

**Debe mostrar:**

- Tramos Desde → Hasta.
- Fluido por tramo.
- Estado operacional por color.
- Flujo, presión, temperatura o nivel principal.
- TAG asociado.
- Condición de carga.
- Unidad generadora.

**Resultado esperado:**

El usuario puede identificar visualmente qué tramo requiere atención sin revisar tabla por tabla.

---

### Vista 2: Balance agua–vapor–condensado

**Pregunta que responde:**

> ¿Cuánta agua entra, cuánta se convierte en vapor y cuánta retorna como condensado?

**Debe mostrar:**

- Entrada de agua desde pozos.
- Agua tratada / permeada.
- Agua de alimentación a caldera.
- Vapor generado.
- Vapor enviado a turbina.
- Condensado recuperado.
- Pérdida estimada.

**Métricas sugeridas:**

```text
Pérdida aparente de agua = Agua de entrada - Condensado recuperado - Agua útil enviada al proceso
```

```text
% recuperación de condensado = Condensado recuperado / Vapor enviado a turbina
```

```text
Consumo específico de agua = m3 de agua / MWh generado
```

---

### Vista 3: Ranking de tramos críticos

**Pregunta que responde:**

> ¿Qué debo revisar primero?

**Debe ordenar tramos por:**

1. Mayor pérdida estimada.
2. Mayor desviación de temperatura.
3. Mayor caída de presión.
4. Mayor variabilidad entre bloques.
5. Mayor cantidad de datos faltantes.
6. Mayor impacto energético.

**Tabla sugerida:**

| Ranking | Tramo | Problema | Severidad | Dato que lo sustenta |
|---|---|---|---|---|
| 1 | Condensador → Desaireador | Baja recuperación de condensado | Alta | Flujo condensado vs vapor a turbina |
| 2 | Osmosis → Agua permeada | Datos incompletos de nivel | Media | Valores faltantes |
| 3 | Pozo → Captación | Variabilidad de flujo | Media | Flujo por bloque |
| 4 | Domo → Sobrecalentador | Riesgo térmico | Alta | Temperatura/presión |
| 5 | Torre de enfriamiento | Pérdida térmica | Media | Temperatura entrada/salida |

---

### Vista 4: Biomasa vs comportamiento operacional

**Pregunta que responde:**

> ¿Qué biomasa produce mayor inestabilidad o menor eficiencia?

**Debe mostrar:**

- Tipo de biomasa.
- Humedad.
- Consumo.
- Ton/h de vapor producido.
- MW generados.
- Temperatura de vapor.
- Presión de vapor.
- Variabilidad térmica.

**Métricas sugeridas:**

```text
Eficiencia vapor/biomasa = ton/h de vapor producido / ton/h de biomasa consumida
```

```text
Eficiencia eléctrica = MW generados / ton/h de biomasa consumida
```

```text
Variabilidad térmica = desviación estándar de temperatura de vapor por tipo de biomasa
```

---

### Vista 5: Calidad de datos e integración

**Pregunta que responde:**

> ¿Qué tan confiable es el análisis?

**Debe mostrar:**

- TAG faltantes.
- Valores faltantes o inválidos.
- Variables sin unidad clara.
- Variables sin histórico.
- Sensores duplicados.
- Mediciones sin integración energética.
- Fuentes de datos no conectadas.

**Métricas sugeridas:**

```text
% completitud de datos = datos válidos / datos esperados
```

```text
% variables con TAG = variables con TAG / total de variables
```

```text
% variables integradas con energía = variables relacionadas con MW o MWh / total de variables críticas
```

---

### Vista 6: Operación, turno y dependencia operacional

**Pregunta que responde:**

> ¿Qué parte del comportamiento depende demasiado del operador o del turno?

**Debe mostrar:**

- Turno.
- Operador.
- Intervenciones manuales.
- Alarmas.
- Cambios de setpoint.
- Tiempo hasta estabilización.
- Variables antes/después de intervención.

**Métricas sugeridas:**

```text
Variabilidad por operador = diferencia de comportamiento del proceso entre operadores bajo condiciones similares
```

```text
Intervenciones por turno = número de ajustes manuales por período
```

```text
Tiempo hasta corrección = tiempo entre anomalía y estabilización
```

La idea no es culpar operadores, sino convertir conocimiento tácito en información operacional visible y reutilizable.

> El dashboard reduce la dependencia del conocimiento individual porque transforma patrones operacionales en información visible, comparable y reutilizable por cualquier turno.

---

## 10. Medición de innovación

La innovación de la propuesta no debe medirse por la existencia del dashboard, sino por su capacidad de mejorar el análisis operacional.

> La innovación de la propuesta no está únicamente en visualizar datos, sino en representar el proceso como una entidad operacional consultable. Esto permite pasar de una revisión manual de variables aisladas a una lectura integrada, trazable y escalable del comportamiento de la planta.

### 10.1 Indicadores de innovación

| Dimensión | Cómo medirla | Ejemplo |
|---|---|---|
| Tiempo de respuesta | Tiempo necesario para responder una pregunta crítica | Antes: revisar varias hojas. Después: una vista única. |
| Integración de datos | Cantidad de fuentes conectadas | Agua, vapor, condensado, biomasa, energía, turno, operador. |
| Representación del proceso | Si el proceso aparece como entidad visual principal | Tramos Desde → Hasta como bloques/conexiones. |
| Escalabilidad | Capacidad de agregar nuevas variables sin rehacer todo | Nuevos TAG, nuevos sensores, nuevas unidades. |
| Calidad de decisión | Preguntas que el dashboard logra responder | Pérdidas, fugas, variabilidad, degradación térmica. |
| Reducción de dependencia operacional | Menor necesidad de interpretación manual | Alertas, reglas y métricas calculadas automáticamente. |
| Trazabilidad | Capacidad de saber de dónde viene cada dato | TAG, unidad, hoja, sensor, fecha, fuente. |
| Adopción | Uso real por parte de usuarios | Frecuencia de consulta, vistas usadas, decisiones tomadas. |

### 10.2 Preguntas para medir innovación

1. ¿Cuánto tarda un usuario en identificar el tramo más crítico antes y después del dashboard?
2. ¿Cuántas fuentes de datos antes estaban separadas y ahora están integradas?
3. ¿Cuántas preguntas operacionales se pueden responder desde una sola vista?
4. ¿Cuántas variables críticas tienen TAG, unidad, estado y trazabilidad?
5. ¿Cuántas decisiones siguen dependiendo exclusivamente del operador?
6. ¿Cuántas anomalías se detectan antes de convertirse en pérdidas o ineficiencias?

---

## 11. Preguntas operacionales y datos necesarios

### 11.1 Pérdida de agua

**Pregunta:**

> ¿En qué tramo del ciclo se está perdiendo agua y cuánto se pierde?

**Datos necesarios:**

| Dato | Uso |
|---|---|
| Flujo de agua industrial | Entrada al sistema. |
| Flujo de agua desmineralizada | Agua tratada disponible. |
| Flujo de agua de alimentación | Agua enviada a caldera. |
| Flujo de vapor | Conversión a vapor. |
| Flujo de condensado | Recuperación. |
| Niveles de estanques | Acumulación o pérdida. |
| Presiones | Posibles fugas o restricciones. |
| Temperaturas | Posible evaporación o pérdida térmica. |

---

### 11.2 Variabilidad de biomasa

**Pregunta:**

> ¿Cómo cambia el comportamiento del vapor y la generación eléctrica según la biomasa utilizada?

**Datos necesarios:**

| Dato | Uso |
|---|---|
| Tipo de biomasa | Clasificar comportamiento. |
| Humedad | Explicar menor poder calorífico. |
| Granulometría | Explicar combustión irregular. |
| Poder calorífico | Relacionar energía disponible. |
| Consumo de biomasa | Relación biomasa/vapor. |
| Ton/h de vapor | Resultado térmico. |
| MW generados | Resultado energético. |
| Temperatura de vapor | Estabilidad térmica. |
| Presión de vapor | Estabilidad operacional. |

---

### 11.3 Degradación térmica asociada al agua de pozo

**Pregunta:**

> ¿El agua proveniente de ciertos pozos está asociada a peor comportamiento térmico o mayor exigencia del sistema?

**Datos necesarios:**

| Dato | Uso |
|---|---|
| Pozo 1 / Pozo 2 | Origen del agua. |
| Flujo por pozo | Cantidad aportada. |
| Presión por pozo | Estado hidráulico. |
| Conductividad, pH, dureza, sílice | Calidad de agua. |
| Flujo osmosis | Eficiencia del tratamiento. |
| Nivel de estanques | Disponibilidad. |
| Temperatura en economizador, domo y sobrecalentador | Efecto térmico aguas abajo. |

**Métrica sugerida:**

```text
ΔT por tramo = Temperatura salida - Temperatura entrada
```

---

### 11.4 Dependencia operacional

**Pregunta:**

> ¿Qué decisiones o interpretaciones dependen del operador y no están sistematizadas en datos?

**Datos necesarios:**

| Dato | Uso |
|---|---|
| Operador de turno | Comparar comportamientos. |
| Turno | Diferenciar día/noche u otros bloques. |
| Ajustes manuales | Identificar intervenciones. |
| Alarmas | Asociar eventos a desviaciones. |
| Cambios de setpoint | Entender decisiones operacionales. |
| Variables antes/después | Medir efecto de intervención. |
| Observaciones manuales | Capturar contexto. |

---

### 11.5 Integración operacional-energética

**Pregunta:**

> ¿Cómo se relacionan las variables de agua, vapor y condensado con la generación eléctrica?

**Datos necesarios:**

| Categoría | Datos |
|---|---|
| Proceso hídrico | Flujos, niveles, presiones. |
| Proceso térmico | Temperaturas, vapor, condensado. |
| Energía | MW, MWh, carga de unidad. |
| Combustible | Biomasa, humedad, consumo. |
| Tiempo | Fecha, hora, turno. |
| Operación | Operador, setpoints, alarmas. |
| Instrumentación | TAG, calidad de medición, fuente. |

**Métricas sugeridas:**

```text
Consumo específico de agua = m3 de agua / MWh generado
```

```text
Vapor específico = ton/h de vapor / MW generado
```

```text
Condensado recuperado por MWh = m3/h de condensado / MW generado
```

```text
Eficiencia integrada = energía generada / agua + biomasa consumida
```

---

## 12. Datos faltantes para una implementación robusta

El Excel actual permite modelar estructura de proceso y variables principales. Sin embargo, para implementar un dashboard realmente útil se requiere integrar información adicional.

| Dato faltante | Por qué importa |
|---|---|
| Fecha y hora | Permite análisis histórico y series temporales. |
| Turno | Permite comparar operación por bloques humanos. |
| Operador | Permite estudiar dependencia operacional. |
| MW generados exactos | Conecta proceso con energía. |
| Biomasa usada | Explica variabilidad operacional. |
| Humedad de biomasa | Factor crítico de combustión. |
| Consumo de biomasa | Permite calcular eficiencia. |
| Calidad del agua | Permite evaluar degradación térmica o tratamiento. |
| Setpoints | Permite distinguir operación normal/anormal. |
| Alarmas/eventos | Permite explicar desviaciones. |
| Tiempo de proceso | Permite usar el ancho de bloque como duración real. |
| Fuente del dato | Permite trazabilidad y auditoría. |

> El archivo actual permite modelar la estructura del proceso y sus variables principales, pero para medir pérdidas, eficiencia e innovación de manera robusta se requiere incorporar temporalidad, energía, biomasa, turno, operador y calidad del agua.

---

## 13. Recomendaciones para implementación en Grafana

### 13.1 Principio de diseño

El dashboard debe partir desde el proceso, no desde los gráficos.

Orden recomendado:

```text
Modelo de dominio → Preguntas operacionales → Métricas → Visualizaciones → Alertas → Validación con usuarios
```

No se recomienda partir directamente desde paneles gráficos sin definir primero qué entidad se está representando.

---

### 13.2 Estructura sugerida de paneles

1. **Estado general del ciclo**
   - Semáforo general por unidad generadora.
   - Estado de agua, vapor, condensado, energía y datos.

2. **Mapa de proceso**
   - Tramos operacionales representados visualmente.
   - Color por estado.
   - Tooltip con TAG, valor, unidad, timestamp y fuente.

3. **Balance de masa simplificado**
   - Entrada de agua.
   - Vapor generado.
   - Condensado recuperado.
   - Pérdida estimada.

4. **Ranking de criticidad**
   - Tramos ordenados de mayor a menor impacto.

5. **Biomasa y energía**
   - Relación biomasa → vapor → MW.

6. **Calidad de datos**
   - Variables faltantes, TAG faltantes, datos no confiables.

7. **Histórico y comparación**
   - Comparación por unidad, carga, turno, operador y biomasa.

---

### 13.3 Recomendaciones visuales

- Usar colores solo si responden a reglas de negocio.
- No saturar el dashboard con demasiados paneles.
- Priorizar una vista inicial que responda una pregunta en menos de 10 segundos.
- Usar tooltips para no sobrecargar la vista principal.
- Permitir filtros por:
  - Unidad generadora.
  - Condición de carga.
  - Fluido.
  - Variable.
  - TAG.
  - Fecha/hora.
  - Biomasa.
  - Turno.
- Separar claramente:
  - Estado operacional.
  - Calidad de datos.
  - Eficiencia energética.
  - Variabilidad.

---

## 14. Roadmap de implementación

### Fase 1: Normalizar modelo de datos

Objetivo:

> Convertir las mediciones actuales en entidades tipo tramo operacional.

Tareas:

- Crear tabla o estructura para tramos.
- Definir campos mínimos:
  - unidad_generadora
  - condicion_operacional
  - desde
  - hasta
  - fluido
  - variable
  - valor
  - unidad
  - tag
  - timestamp
  - fuente
- Identificar datos faltantes.
- Homologar nombres de fluidos y equipos.
- Homologar unidades de medida.

---

### Fase 2: Definir métricas operacionales

Objetivo:

> Pasar de datos individuales a indicadores de proceso.

Tareas:

- Definir pérdida aparente de agua.
- Definir recuperación de condensado.
- Definir consumo específico de agua.
- Definir vapor específico.
- Definir eficiencia vapor/biomasa.
- Definir estado de calidad de datos.
- Definir reglas verde/amarillo/rojo.

---

### Fase 3: Construir vistas en Grafana

Objetivo:

> Representar el proceso como entidad visual de primera categoría.

Tareas:

- Crear vista de mapa operacional.
- Crear vista de balance agua–vapor–condensado.
- Crear ranking de tramos críticos.
- Crear vista de calidad de datos.
- Crear filtros globales.
- Crear tooltips por tramo.

---

### Fase 4: Integrar biomasa, energía y operación

Objetivo:

> Relacionar comportamiento del proceso con sus causas operacionales y energéticas.

Tareas:

- Integrar tipo de biomasa.
- Integrar humedad de biomasa.
- Integrar consumo de biomasa.
- Integrar MW/MWh.
- Integrar turno y operador, si está disponible.
- Integrar alarmas o eventos relevantes.

---

### Fase 5: Validar innovación

Objetivo:

> Demostrar que la propuesta mejora el análisis operacional.

Tareas:

- Medir tiempo de respuesta antes/después.
- Medir cantidad de fuentes integradas.
- Medir cantidad de preguntas respondidas por vista.
- Medir completitud de datos.
- Validar con usuarios operacionales.
- Documentar decisiones tomadas gracias al dashboard.

---

## 15. Criterios para saber si el dashboard está funcionando

El dashboard puede considerarse útil si cumple lo siguiente:

- Permite identificar el tramo más crítico rápidamente.
- Representa el proceso, no solo gráficos aislados.
- Permite ver pérdidas de agua o baja recuperación de condensado.
- Relaciona agua/vapor/condensado con energía.
- Integra variables de biomasa.
- Expone datos faltantes o poco confiables.
- Reduce dependencia del conocimiento individual del operador.
- Permite comparar comportamiento por unidad, carga, turno o biomasa.
- Entrega trazabilidad: valor, TAG, unidad, fuente y tiempo.
- Permite medir si el análisis mejora frente al método anterior.

---

## 16. Riesgos a evitar

### 16.1 Dashboard decorativo

Riesgo:

> Crear muchas gráficas sin que respondan preguntas operacionales.

Mitigación:

- Toda visualización debe tener una pregunta asociada.
- Todo panel debe justificar qué decisión permite tomar.

---

### 16.2 Variable como unidad principal

Riesgo:

> Analizar flujo, presión o temperatura de forma aislada.

Mitigación:

- Representar siempre las variables dentro de un tramo operacional.

---

### 16.3 Falta de trazabilidad

Riesgo:

> Mostrar un valor sin saber de dónde viene.

Mitigación:

- Todo dato debe tener TAG, unidad, timestamp, fuente y contexto.

---

### 16.4 No medir impacto

Riesgo:

> No poder demostrar si el dashboard mejora algo.

Mitigación:

- Definir indicadores de innovación desde el inicio.

---

### 16.5 Sobrecarga visual

Riesgo:

> Intentar mostrar todo en una sola pantalla sin jerarquía.

Mitigación:

- Vista principal simple.
- Detalle progresivo por tooltips, drill-down o paneles secundarios.

---

## 17. Frases guía para el equipo

> Un dashboard útil no es el que muestra más gráficos, sino el que representa correctamente la unidad de análisis del problema.

> En este caso, la unidad de análisis no es una variable aislada, sino cada tramo del proceso agua–vapor–condensado y su relación con energía, biomasa, operador y condición de carga.

> La innovación no está solo en visualizar datos, sino en reducir el tiempo necesario para responder preguntas críticas de operación.

> Si el usuario no puede responder qué tramo debe revisar primero, el dashboard todavía no está suficientemente refinado.

> Toda vista debe responder una pregunta operacional clara.

> Todo dato debe tener contexto: dónde ocurre, qué mide, con qué instrumento, en qué condición y con qué impacto.

---

## 18. Definición resumida de la propuesta

Se propone desarrollar y refinar un dashboard operacional basado en un modelo de dominio del ciclo agua–vapor–condensado de Planta COMASA.

La unidad de análisis será el **tramo operacional**, definido por origen, destino, fluido, variable, medición, TAG, unidad generadora y condición de carga.

Esta representación permitirá visualizar en una sola vista el comportamiento del proceso, detectar pérdidas de agua, variabilidad térmica, efectos asociados a biomasa y dependencia operacional.

La innovación se medirá mediante la reducción del tiempo de análisis, el aumento de integración de datos, la trazabilidad de variables críticas y la capacidad de responder preguntas operacionales sin depender exclusivamente del conocimiento del operador.

---

## 19. Próximo paso recomendado

El próximo paso técnico recomendado es revisar la implementación actual en Grafana y mapear cada panel existente contra esta estructura:

| Panel actual | Pregunta que responde | Entidad representada | Métrica usada | Datos requeridos | Brecha |
|---|---|---|---|---|---|
| Panel 1 | ¿Qué responde? | ¿Variable o tramo? | ¿Qué indicador usa? | ¿Qué datos consume? | ¿Qué falta? |
| Panel 2 | ¿Qué responde? | ¿Variable o tramo? | ¿Qué indicador usa? | ¿Qué datos consume? | ¿Qué falta? |
| Panel 3 | ¿Qué responde? | ¿Variable o tramo? | ¿Qué indicador usa? | ¿Qué datos consume? | ¿Qué falta? |

Esto permitirá distinguir qué ya está funcionando, qué debe reorganizarse y qué falta implementar para alcanzar un nivel de refinamiento adecuado.
