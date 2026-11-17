# Guía de examen — Conecta 4 (Minimax + Árbol de Decisión)

## 0. Datos del proyecto que conviene saber de memoria

- Tablero: **4 filas × 5 columnas** (`ROWS = 4`, `COLS = 5`), se conectan **4**.
- IA = `'O'` (Amarillo). Humano = `'X'` (Rojo).
- Dificultad = profundidad de búsqueda: **fácil 2, medio 4, difícil 6**.
- Minimax usa **poda alfa-beta + límite de profundidad + heurística**.
- El Árbol de Decisión recibe **20 entradas** (4×5) y devuelve **una columna 0..4**.
- Codificación del tablero para el árbol: **1 = ficha propia, −1 = ficha rival, 0 = vacío**, siempre desde la perspectiva de quien va a mover.

---

## 1. Chuleta de valores (lo que más le interesa al ingeniero)

| Situación | Valor | Significado |
|---|---:|---|
| Gana la IA | **+10000 − profundidad** | Victoria segura. Cuanto antes se encuentra, mayor puntaje. |
| Gana el humano | **−10000 + profundidad** | Derrota. Cuanto más tarde ocurre, menos negativa. |
| Empate o tablero lleno | **0** | Neutro. |
| Ventana de 4 con **3 fichas de la IA** | **+5** | Casi victoria. |
| Ventana de 4 con **2 fichas de la IA** | **+2** | Amenaza. |
| Ventana de 4 con **3 fichas del humano** | **−5** | Peligro alto. |
| Ventana de 4 con **2 fichas del humano** | **−2** | Peligro leve. |
| Ventana mezclada (IA y humano) | **0** | Ya nadie puede ganar por ahí. |
| Ventana con 1 o 0 fichas | **0** | Sin valor. |

### Regla de signos

- **Positivo = bueno para la IA** (jugador MAX).
- **Negativo = bueno para el humano** (jugador MIN).
- La IA elige la jugada con el **puntaje más alto**.
- El humano, dentro del algoritmo, elige la jugada con el **puntaje más bajo**.

### ¿Por qué 10000 y no 100?

Porque una victoria/derrota debe valer **más que cualquier suma de la heurística**.
En este tablero hay como máximo **17 ventanas de 4**; la heurística máxima posible es
`17 × 5 = 85`. Al usar `10000`, un estado terminal siempre domina a cualquier estado no terminal.

### ¿Por qué `10000 − profundidad`?

`profundidad` es el nivel en el que se encontró la jugada.
- Victoria en profundidad 1 → `9999`.
- Victoria en profundidad 5 → `9995`.

Así la IA prefiere **ganar rápido**.

### ¿Por qué `−10000 + profundidad`?

- Derrota en profundidad 1 → `−9999`.
- Derrota en profundidad 5 → `−9995`.

Así la IA prefiere **perder lo más tarde posible**.

---

## 2. Pseudocódigo del modelo (lo que Minimax necesita)

```text
FUNCIÓN ColumnasDisponibles():
    DEVOLVER [c PARA c = 0..COLUMNAS-1 SI altura[c] < FILAS]

FUNCIÓN Poner(col, jugador):
    SI col no está disponible: DEVOLVER falso
    fila ← FILAS - 1 - altura[col]
    tablero[fila][col] ← jugador
    altura[col] ← altura[col] + 1
    DEVOLVER verdadero

FUNCIÓN Quitar(col):                 # BACKTRACKING
    altura[col] ← altura[col] - 1
    fila ← FILAS - 1 - altura[col]
    tablero[fila][col] ← VACÍO

FUNCIÓN Gana(jugador):
    PARA CADA celda (f, c):
        PARA CADA dirección (0,1), (1,0), (1,1), (1,-1):
            SI las 4 celdas seguidas existen y son del jugador:
                DEVOLVER verdadero
    DEVOLVER falso
```

La clave es `Poner` → explorar → `Quitar`. No se copia el tablero: se modifica y se deshace.
Eso es **backtracking** y ahorra memoria.

---

## 3. Pseudocódigo de Minimax (versión corta para examen)

```text
FUNCIÓN MejorJugada(tablero):
    mejorPuntaje ← -∞
    mejorColumna ← nula
    alfa ← -∞ ; beta ← +∞

    PARA CADA col EN tablero.ColumnasDisponibles():
        tablero.Poner(col, IA)
        puntaje ← Minimax(tablero, 1, alfa, beta, MIN)
        tablero.Quitar(col)

        SI puntaje > mejorPuntaje:
            mejorPuntaje ← puntaje
            mejorColumna ← col

        alfa ← max(alfa, mejorPuntaje)

    DEVOLVER mejorColumna, mejorPuntaje
```

> Detalle de examen: si dos jugadas empatan en puntaje, se queda con la **primera**,
> porque la comparación es `>` estricta. Como se recorre de izquierda a derecha,
> gana la columna más a la izquierda.

```text
FUNCIÓN Minimax(tablero, prof, alfa, beta, turno):

    # --- PARADAS (lo único que necesitas de casos base) ---
    SI tablero.Gana(IA):        DEVOLVER  10000 - prof
    SI tablero.Gana(HUMANO):    DEVOLVER -10000 + prof
    SI no hay columnas:         DEVOLVER  0
    SI prof ≥ PROFUNDIDAD_MAX:  DEVOLVER  Heuristica(tablero)

    # --- TURNO MAX (IA) ---
    SI turno = MAX:
        mejor ← -∞
        PARA CADA col EN columnas disponibles:
            tablero.Poner(col, IA)
            valor ← Minimax(tablero, prof+1, alfa, beta, MIN)
            tablero.Quitar(col)

            mejor ← max(mejor, valor)
            alfa  ← max(alfa, mejor)

            SI beta ≤ alfa: ROMPER        # PODA ALFA-BETA

        DEVOLVER mejor

    # --- TURNO MIN (HUMANO) ---
    SINO:
        mejor ← +∞
        PARA CADA col EN columnas disponibles:
            tablero.Poner(col, HUMANO)
            valor ← Minimax(tablero, prof+1, alfa, beta, MAX)
            tablero.Quitar(col)

            mejor ← min(mejor, valor)
            beta  ← min(beta, mejor)

            SI beta ≤ alfa: ROMPER        # PODA ALFA-BETA

        DEVOLVER mejor
```

### Idea central

La IA **no elige la jugada con mejor heurística inmediata**.
Elige la jugada cuyo **peor futuro** (después de la mejor respuesta del rival) sea el mejor.
Eso es Minimax: MAX elige el máximo, MIN elige el mínimo, y los valores suben y bajan por el árbol.

---

## 4. Pseudocódigo de la heurística

```text
FUNCIÓN Heuristica(tablero):
    total ← 0
    PARA CADA celda (f, c):
        PARA CADA dirección (0,1), (1,0), (1,1), (1,-1):
            v ← VentanaDe4(f, c, dirección)
            SI v existe:
                total ← total + PuntuarVentana(v)
    DEVOLVER total

FUNCIÓN PuntuarVentana(v):
    mios  ← contar(IA, v)
    rival ← contar(HUMANO, v)

    SI mios > 0 Y rival > 0: DEVOLVER  0
    SI mios = 3:             DEVOLVER +5
    SI mios = 2:             DEVOLVER +2
    SI rival = 3:            DEVOLVER -5
    SI rival = 2:            DEVOLVER -2
    DEVOLVER 0
```

### ¿Qué hace exactamente?

Recorre **todas las ventanas de 4 casillas en línea**:
horizontal, vertical, diagonal derecha y diagonal izquierda.
Cada ventana se puntúa según cuántas fichas propias o rivales tiene, **solo si no está mezclada**.

### Detalles que pueden preguntar

- Una ventana con **4 fichas** no se puntúa con 5: se detecta antes como **victoria terminal**.
- Una ventana con **1 ficha** vale 0: no es una amenaza todavía.
- Una ventana **mezclada** vale 0: está bloqueada para ambos.
- No se distingue si el espacio libre es jugable por gravedad; es una **simplificación**.
- Tampoco se da más peso al centro ni se distingue una tripleta abierta de una cerrada.

---

## 5. Ejemplo numérico (para entender cómo se propaga el valor)

Supón que la IA debe mover y solo hay dos columnas candidatas: **A** y **B**.
`PROFUNDIDAD_MAX = 2`.

```text
                 IA (MAX)
                /        \
          jugar A        jugar B
             |              |
       HUMANO (MIN)    HUMANO (MIN)
        /       \        /       \
      +4        -6      +3       +1
```

- Si la IA juega **A**, el humano elige el mínimo: `min(+4, −6) = −6`.
- Si la IA juega **B**, el humano elige el mínimo: `min(+3, +1) = +1`.
- La IA elige el máximo: `max(−6, +1) = +1`.

**Resultado: juega B.**

Aunque A tenía una rama con +4, el rival no va a regalar esa rama: elegirá −6.
Por eso el algoritmo mira el **peor caso**, no el mejor.

### Ejemplo con victoria y bloqueo

- Si la IA puede ganar en su jugada actual: `10000 − 1 = 9999`.
- Si el humano puede ganar en la siguiente: `−10000 + 2 = −9998`.

Como `9999` es altísimo y `−9998` es bajísimo, la IA:
1. **Gana si puede**.
2. **Bloquea si el rival puede ganar**, porque cualquier otra jugada vale como mucho ±85.

---

## 6. Poda alfa-beta (explicación corta)

- `alfa` = el mejor valor que MAX ya tiene asegurado.
- `beta` = el mejor valor que MIN ya tiene asegurado.
- Si en algún momento **`beta ≤ alfa`**, se corta la búsqueda: esa rama ya no puede cambiar la decisión.

### Ejemplo

```text
En la raíz, la jugada A obtuvo 5  →  alfa = 5.
Ahora se evalúa la jugada B:
  el humano responde y su primera opción vale 3  →  beta = 3.
  Como beta (3) ≤ alfa (5), se podan las demás respuestas de B.
```

¿Por qué? Porque el humano, siendo MIN, elegiría **como máximo 3** en esa rama;
la IA ya tiene un 5 con A; entonces B no puede superar a A. No vale la pena seguir.

### Complejidad

| Versión | Tiempo | Memoria |
|---|---|---|
| Minimax puro | `O(b^d)` | `O(b · d)` |
| Alfa-beta (mejor caso) | `O(b^(d/2))` | `O(b · d)` |
| Alfa-beta (peor caso) | `O(b^d)` | `O(b · d)` |

`b` = factor de ramificación (columnas disponibles, máximo 5).
`d` = profundidad (2, 4 o 6 en el juego).

---

## 7. Pseudocódigo del Árbol de Decisión

### 7.1 Entrenamiento (`scripts/train_tree.py`)

```text
FUNCIÓN Entrenar():
    datos ← leer CSV "data/minimax_games.csv"
    X ← las 20 columnas del tablero (c0 ... c19)
    y ← la columna elegida por Minimax ("move")

    X_entreno, X_prueba, y_entreno, y_prueba ← dividir(X, y, 80% / 20%)

    árbol ← DecisionTreeClassifier(profundidad_max = 15)
    árbol.Entrenar(X_entreno, y_entreno)

    precisión ← árbol.Puntuar(X_prueba, y_prueba)
    MOSTRAR precisión

    guardar árbol en "model/tree_model.joblib"
```

### 7.2 Jugar (`model/decision_tree_agent.py`)

```text
FUNCIÓN MejorJugada(tablero):
    estado ← Codificar(tablero, IA)     # 1 = mía, -1 = rival, 0 = vacío
    col ← árbol.Predecir(estado)

    SI col no está disponible:
        col ← columna disponible más cercana a la predicha

    DEVOLVER col
```

### 7.3 Camino de decisión (lo que se muestra en pantalla)

```text
FUNCIÓN CaminoDeDecisión(tablero):
    estado ← Codificar(tablero, IA)
    hoja ← árbol.Apply(estado)
    nodos ← árbol.DecisionPath(estado)
    pasos ← []

    PARA CADA nodo EN nodos:
        SI nodo = hoja: CONTINUAR       # la hoja no es una pregunta

        característica ← árbol.feature[nodo]
        umbral ← árbol.threshold[nodo]

        paso.fila      ← característica DIV COLUMNAS
        paso.columna   ← característica MOD COLUMNAS
        paso.vaIzquierda ← estado[característica] ≤ umbral

        agregar paso a pasos

    DEVOLVER pasos
```

### 7.4 Cómo decide internamente el árbol

Cada nodo interno hace una pregunta del tipo:

```text
¿fila 3, columna 2  ≤  0.5 ?
        /              \
      SÍ                NO
```

- Si el valor es `≤ umbral`, va a la izquierda; si no, a la derecha.
- Las hojas contienen la **columna más frecuente** de los ejemplos que llegaron ahí.
- Para elegir la pregunta, `DecisionTreeClassifier` usa por defecto **impureza de Gini**:

```text
Gini(nodo) = 1 - Σ (proporción de cada clase)²
```

Elige la característica y el umbral que **más reduzcan la impureza**.
`max_depth = 15` limita el árbol para no memorizar demasiado (overfitting).

---

## 8. Teoría clave (resumen para responder)

### Minimax

- Algoritmo para juegos **de suma cero, deterministas, por turnos y con información perfecta**.
- Construye un **árbol de juego**: nodos = estados, aristas = jugadas.
- **MAX** (IA) maximiza; **MIN** (humano) minimiza.
- Supone que el rival juega **óptimamente**.
- El valor de un nodo es el mejor resultado que puede asegurar quien mueve en ese nodo.
- Es una forma de **búsqueda exhaustiva con backtracking**.
- Sin límite de profundidad, el árbol es demasiado grande: por eso se corta con `max_depth` y se usa una **heurística**.

### Árbol de decisión (machine learning)

- Modelo de **aprendizaje supervisado** para clasificación.
- Aprende un mapa **tablero → columna** a partir de ejemplos.
- No busca jugadas en tiempo real: solo **predice**.
- Se entrena con partidas **Minimax vs jugador aleatorio**.
- La etiqueta es la columna que eligió Minimax (profundidad 6).
- Precisión ≈ **80%**: mide cuánto **imita** a Minimax, no cuánto gana.
- Responde en **milisegundos** (una predicción), mientras Minimax explora miles de nodos.
- El "camino de decisión" que se muestra es el camino **real** del árbol entrenado.

### Diferencia importante

| | Árbol de juego (Minimax) | Árbol de decisión (ML) |
|---|---|---|
| Qué es | Búsqueda en el árbol de jugadas | Modelo entrenado |
| Cuándo trabaja | En cada jugada, en tiempo real | Antes, en el entrenamiento |
| Costo | Alto (`O(b^d)`) | Bajo (`O(profundidad)`) |
| Resultado | Jugada calculada | Jugada predicha |
| Nodos evaluados | Miles | 0 |

---

## 9. Preguntas probables del examen (con respuesta corta)

1. **¿Qué es Minimax?**
   Algoritmo de búsqueda para juegos por turnos que asume que el rival juega óptimo; MAX maximiza y MIN minimiza.

2. **¿Por qué se limita la profundidad?**
   Porque el árbol crece de forma exponencial (`O(b^d)`) y explorarlo completo tarda demasiado.

3. **¿Qué hace la función heurística?**
   Estima el valor de un estado no terminal sumando puntos por ventanas de 4 casillas.

4. **¿Qué significan +5, +2, −5, −2?**
   +5 tripleta propia, +2 pareja propia, −5 tripleta rival, −2 pareja rival.

5. **¿Por qué +10000 y −10000?**
   Para que una victoria o derrota siempre valga más que cualquier suma heurística.

6. **¿Por qué se resta/suma la profundidad?**
   Para preferir ganar rápido (`10000 − prof`) y perder lo más tarde posible (`−10000 + prof`).

7. **¿Qué es alfa y qué es beta?**
   Alfa es la mejor opción de MAX encontrada; beta la mejor de MIN. Si `beta ≤ alfa`, se poda.

8. **¿Qué es backtracking aquí?**
   Poner una ficha, explorar, y quitarla (`undo`) para reutilizar el mismo tablero.

9. **¿Qué pasa si hay empate de puntajes?**
   Se queda con la primera jugada encontrada, es decir, la columna más a la izquierda.

10. **¿Cómo se codifica el tablero para el árbol?**
    20 valores: 1 ficha propia, −1 rival, 0 vacío, desde la perspectiva de quien mueve.

11. **¿Qué mide la precisión del árbol?**
    El porcentaje de posiciones donde elige la misma columna que Minimax; no mide victorias.

12. **¿Por qué el árbol es más rápido?**
    Porque no explora: solo recorre unas pocas preguntas hasta una hoja.

13. **¿Qué diferencia hay entre el árbol de juego y el árbol de decisión?**
    El de juego se explora con Minimax en cada jugada; el de decisión se entrena antes y solo predice.

14. **¿Qué es la impureza de Gini?**
    Una medida de mezcla de clases en un nodo; el árbol elige la división que más la reduce.

---

## 10. Limitaciones que puedes mencionar (puntos extra)

- La heurística no distingue una tripleta **abierta** de una **bloqueada**.
- No da más valor a la **columna central**, que suele ser estratégica.
- No comprueba si el hueco libre de una ventana es **alcanzable** por gravedad.
- La evaluación se repite para cada ventana, sin tablas de posiciones.
- El árbol de decisión puede fallar en posiciones poco parecidas a las del entrenamiento.
- El árbol **imita** a Minimax; si Minimax se equivoca, el árbol aprende ese error.

---

## 11. Orden recomendado para estudiar

1. Tabla de valores de la sección 1 (lo más importante).
2. Pseudocódigo de Minimax y de la heurística (secciones 3 y 4).
3. Ejemplo numérico de la sección 5.
4. Poda alfa-beta (sección 6).
5. Árbol de decisión: entrenamiento y predicción (sección 7).
6. Teoría y preguntas (secciones 8 y 9).

Si en el examen te piden "escribe el código", con las secciones 3, 4 y 7 tienes las tres piezas:
**búsqueda (Minimax), evaluación (heurística) y aprendizaje (árbol de decisión).**

---

# PARTE II — Árbol de decisión SIN dataset de Minimax

## 12. El problema: el árbol necesita etiquetas

Un árbol de decisión es **aprendizaje supervisado**. Necesita ejemplos de la forma:

```text
(estado del tablero)  →  (columna que se debería jugar)
```

Si esa "columna correcta" la produce Minimax, el árbol solo aprende a **imitarlo**.
Para que no sea una copia, la etiqueta debe venir de otra fuente. Hay tres opciones válidas:

| Fuente de las etiquetas | Cómo se obtiene | Ventaja | Desventaja |
|---|---|---|---|
| **Partidas humanas** | Se graba cada jugada de una persona | Es lo más defendible: aprende de humanos | Se necesitan muchas partidas |
| **Autoaprendizaje con política simple** | La IA juega contra sí misma con reglas simples | Se genera solo y rápido | Aprende de una política sencilla, no óptima |
| **Monte Carlo** | Para cada jugada se simulan partidas aleatorias | No usa Minimax ni heurística fuerte | Es más lento de generar |

**Importante:** en las tres, el árbol sigue siendo supervisado. Lo que cambia es **quién pone la etiqueta**.
Ya no se compara contra Minimax; se compara contra el humano o contra la política que generó los datos.

---

## 13. Opción recomendada: autoaprendizaje con política simple

La política simple **no es Minimax**: solo mira la jugada actual, no simula la respuesta del rival.

```text
FUNCIÓN ElegirJugadaPolitica(tablero, jugador):
    rival ← Rival(jugador)

    # 1. Si puede ganar ahora, gana.
    PARA CADA col EN columnas disponibles:
        Poner(col, jugador)
        SI Gana(jugador):
            Quitar(col)
            DEVOLVER col
        Quitar(col)

    # 2. Si el rival puede ganar ahora, bloquea.
    PARA CADA col EN columnas disponibles:
        Poner(col, rival)
        SI Gana(rival):
            Quitar(col)
            DEVOLVER col
        Quitar(col)

    # 3. Si no, elige la jugada con mejor evaluación INMEDIATA.
    #    Ojo: evalúa el tablero tal como queda, sin mirar el futuro.
    mejorValor ← -∞
    mejorCol ← primera columna disponible
    PARA CADA col EN columnas disponibles:
        Poner(col, jugador)
        valor ← EvaluarEstatico(tablero, jugador)
        Quitar(col)
        SI valor > mejorValor:
            mejorValor ← valor
            mejorCol ← col

    DEVOLVER mejorCol
```

`EvaluarEstatico` puede ser la misma suma de ventanas de 4 (sección 4), pero **sin recursión**.
Eso es lo que la diferencia de Minimax: aquí no se explora el árbol de jugadas.

### 13.1 Generar el dataset con partidas

```text
FUNCIÓN GenerarDataset(N):
    muestras ← []

    PARA partida EN 1..N:
        tablero ← TableroVacio()
        jugador ← X si partida es par, si no O
        historial ← []

        MIENTRAS verdadero:
            # 15% de jugadas al azar para que las partidas no sean repetidas.
            SI aleatorio() < 0.15:
                col ← columna disponible al azar
            SINO:
                col ← ElegirJugadaPolitica(tablero, jugador)

            estado ← Codificar(tablero, jugador)   # 1 mía, -1 rival, 0 vacío
            agregar (estado, col, jugador) a historial

            Poner(col, jugador)

            SI Gana(jugador):
                ganador ← jugador
                ROMPER
            SI TableroLleno():
                ganador ← nulo
                ROMPER

            jugador ← Rival(jugador)

        # Solo se aprende de las jugadas del ganador.
        # Si fue empate, se conservan las jugadas de ambos.
        PARA CADA (estado, col, jug) EN historial:
            SI ganador = nulo O jug = ganador:
                agregar (estado, col) a muestras

    DEVOLVER muestras
```

**Por qué filtrar por el ganador:** así el árbol aprende patrones de quien ganó, no de quien perdió.
Es una forma sencilla de aprendizaje por experiencia, sin Minimax.

### 13.2 Entrenar el árbol

```text
FUNCIÓN Entrenar():
    muestras ← GenerarDataset(2000)

    X ← [estado de cada muestra]     # 20 valores por muestra
    y ← [columna de cada muestra]    # clase: 0, 1, 2, 3 o 4

    # Dividir por PARTIDA, no por posición.
    # Si se divide por posición, posiciones casi iguales quedan en
    # entrenamiento y prueba, y la precisión sale artificialmente alta.
    X_entreno, X_prueba, y_entreno, y_prueba ← DividirPorPartida(muestras, 80% / 20%)

    árbol ← DecisionTreeClassifier(
        profundidad_max = 10,
        min_muestras_hoja = 10,
        random_state = 42
    )
    árbol.Entrenar(X_entreno, y_entreno)

    precisión ← árbol.Puntuar(X_prueba, y_prueba)
    MOSTRAR precisión

    guardar árbol en "model/tree_model.joblib"
```

### 13.3 Evaluar de verdad (no solo precisión)

La precisión solo dice **cuánto imita las etiquetas**. Para saber si juega bien, hay que jugar partidas:

```text
FUNCIÓN MedirFuerza(árbol, N):
    victorias ← 0
    PARA i EN 1..N:
        resultado ← JugarPartida(árbol vs PoliticaSimple)
        SI resultado = árbol:
            victorias ← victorias + 1
    DEVOLVER victorias / N     # porcentaje de victorias
```

Puedes medir tres cosas:
1. **Precisión:** coincidencia con la etiqueta (humano o política).
2. **Tasa de victoria:** contra aleatorio, contra la política simple, contra un humano.
3. **Latencia:** milisegundos por jugada.

---

## 14. Opción con partidas humanas (la más defendible)

Si el profesor quiere que aprenda de personas:

```text
FUNCIÓN GrabarPartidaHumana():
    tablero ← TableroVacio()
    jugador ← X
    historial ← []

    MIENTRAS no termine:
        col ← esperar clic del humano
        estado ← Codificar(tablero, jugador)
        agregar (estado, col, jugador) a historial
        Poner(col, jugador)

        SI Gana(jugador) O TableroLleno():
            ROMPER
        jugador ← Rival(jugador)

    DEVOLVER historial, ganador
```

Luego se guardan solo las jugadas del ganador (o todas, si se quiere aprender también de los errores).
El CSV tendría las mismas 20 columnas `c0..c19` y una columna `move`.

**Ventaja:** el árbol aprende de humanos reales.
**Desventaja:** necesitas juntar muchas partidas para que no memorice pocas posiciones.

---

## 15. Opción Monte Carlo (sin Minimax y sin heurística)

Para cada jugada posible, se simulan partidas aleatorias y se elige la que más gana:

```text
FUNCIÓN EtiquetarConMonteCarlo(tablero, jugador, simulaciones):
    PARA CADA col EN columnas disponibles:
        victorias ← 0

        PARA i EN 1..simulaciones:
            Poner(col, jugador)
            resultado ← JugarPartidaAleatoria(tablero, Rival(jugador))
            Quitar(col)

            SI resultado = jugador:
                victorias ← victorias + 1

        valor[col] ← victorias / simulaciones

    DEVOLVER col con mayor valor[col]
```

Es más lento, pero no copia ni a Minimax ni a una heurística.
Se usa para generar las etiquetas y después se entrena el árbol normalmente.

---

## 16. Qué cambiaría en tu proyecto

No hay que tocar `DecisionTreeAgent`: sigue prediciendo igual.
Solo cambia el **generador del dataset** y el **archivo CSV**:

| Antes (copia de Minimax) | Ahora (entrenamiento propio) |
|---|---|
| `model/ml_agent.py` usa `MinimaxAgent` | Usa `ElegirJugadaPolitica` o partidas humanas |
| `data/minimax_games.csv` | `data/selfplay_games.csv` |
| Etiqueta = jugada de Minimax | Etiqueta = jugada del ganador / humano |
| Precisión = imita a Minimax | Precisión = imita la política o al humano |
| Comparación contra Minimax | Comparación contra aleatorio, política y humanos |

Y en la defensa puedes decir:

> “El árbol no copia a Minimax. Se entrenó con partidas generadas por una política propia
> (o por humanos) y conserva solo las jugadas de los ganadores. Minimax se usa como
> agente rival para medir la fuerza, no como fuente de las etiquetas.”

---

# PARTE III — Recorridos de árboles y balanceo

## 17. Recorridos de un árbol

Árbol de ejemplo:

```text
          A
        /   \
       B     C
      / \   / \
     D   E F   G
```

| Recorrido | Orden | Resultado |
|---|---|---|
| **Preorden** | raíz → izquierda → derecha | `A B D E C F G` |
| **Inorden** | izquierda → raíz → derecha | `D B E A F C G` |
| **Postorden** | izquierda → derecha → raíz | `D E B F G C A` |
| **Por niveles (BFS)** | nivel 0, luego nivel 1, etc. | `A B C D E F G` |

### Pseudocódigo

```text
FUNCIÓN Preorden(n):
    SI n = nulo: REGRESAR
    VISITAR(n)
    Preorden(n.izquierda)
    Preorden(n.derecha)

FUNCIÓN Inorden(n):
    SI n = nulo: REGRESAR
    Inorden(n.izquierda)
    VISITAR(n)
    Inorden(n.derecha)

FUNCIÓN Postorden(n):
    SI n = nulo: REGRESAR
    Postorden(n.izquierda)
    Postorden(n.derecha)
    VISITAR(n)

FUNCIÓN PorNiveles(raíz):
    cola ← [raíz]
    MIENTRAS cola no esté vacía:
        n ← cola.sacar()
        VISITAR(n)
        SI n.izquierda ≠ nulo: cola.meter(n.izquierda)
        SI n.derecha   ≠ nulo: cola.meter(n.derecha)
```

### ¿Para qué sirve cada uno?

- **Preorden:** copiar o serializar un árbol; en un árbol de juego, expandir un nodo antes de sus hijos.
- **Inorden:** en un **BST** devuelve las claves **ordenadas**. En un árbol de juego no tiene sentido, porque no hay orden por clave.
- **Postorden:** liberar memoria, evaluar expresiones y **Minimax**: primero se evalúan los hijos y al final se calcula el valor del padre.
- **Por niveles (BFS):** búsqueda por anchura; sirve para encontrar el camino más corto en número de jugadas.
- **DFS (profundidad):** usa pila o recursión; es el recorrido natural de Minimax y del backtracking.

### Relación con Minimax

Minimax hace un **DFS en postorden**:

```text
Para cada jugada:
    bajar (Poner)
    calcular el valor del hijo
    subir (Quitar)
Después de recorrer todos los hijos, calcular max o min del padre.
```

La **poda alfa-beta no cambia el recorrido**: sigue siendo DFS en postorden, solo que se salta ramas que ya no pueden cambiar la decisión.

### Relación con el árbol de decisión

- **Predecir** no recorre todo el árbol: sigue **un solo camino** desde la raíz hasta una hoja, preguntando `valor ≤ umbral` en cada nodo. Es `O(profundidad)`.
- **Entrenar** construye el árbol de arriba hacia abajo (preorden): elige la mejor pregunta para la raíz, divide los datos y repite en cada hijo.

---

## 18. Árbol binario de búsqueda (BST)

Un **BST** cumple:

```text
todo lo de la izquierda < nodo < todo lo de la derecha
```

- Búsqueda, inserción y eliminación: `O(h)`, donde `h` es la altura.
- Si el árbol está **balanceado**, `h ≈ log₂(n)` y las operaciones son `O(log n)`.
- Si está **degenerado** (por ejemplo, insertar 1, 2, 3, 4, 5 en orden), `h = n` y las operaciones son `O(n)`.

```text
FUNCIÓN Buscar(n, clave):
    SI n = nulo: DEVOLVER nulo
    SI clave = n.clave: DEVOLVER n
    SI clave < n.clave: DEVOLVER Buscar(n.izquierda, clave)
    DEVOLVER Buscar(n.derecha, clave)
```

El **inorden** de un BST devuelve las claves ordenadas. Eso no pasa en un árbol de juego ni en un árbol de decisión.

---

## 19. Balanceo: árboles AVL

Un árbol **AVL** es un BST que se mantiene balanceado.
Para cada nodo se define el **factor de balance**:

```text
FB(n) = altura(izquierda) - altura(derecha)
```

En un AVL válido: `FB ∈ {-1, 0, +1}`.
Si `|FB| > 1`, hay que hacer **rotaciones**.

### Las cuatro rotaciones

| Caso | Situación | Solución |
|---|---|---|
| **LL** | izquierda pesada, el hijo izquierdo también | rotación simple a la derecha |
| **RR** | derecha pesada, el hijo derecho también | rotación simple a la izquierda |
| **LR** | izquierda pesada, el hijo izquierdo pesa a la derecha | rotación izquierda al hijo, luego derecha al nodo |
| **RL** | derecha pesada, el hijo derecho pesa a la izquierda | rotación derecha al hijo, luego izquierda al nodo |

### Pseudocódigo

```text
FUNCIÓN Altura(n):
    SI n = nulo: DEVOLVER 0
    DEVOLVER n.altura

FUNCIÓN ActualizarAltura(n):
    n.altura ← 1 + max(Altura(n.izquierda), Altura(n.derecha))

FUNCIÓN FactorBalance(n):
    DEVOLVER Altura(n.izquierda) - Altura(n.derecha)

FUNCIÓN RotarDerecha(y):
    x ← y.izquierda
    T2 ← x.derecha

    x.derecha ← y
    y.izquierda ← T2

    ActualizarAltura(y)
    ActualizarAltura(x)
    DEVOLVER x

FUNCIÓN RotarIzquierda(x):
    y ← x.derecha
    T2 ← y.izquierda

    y.izquierda ← x
    x.derecha ← T2

    ActualizarAltura(x)
    ActualizarAltura(y)
    DEVOLVER y

FUNCIÓN Rebalancear(n):
    ActualizarAltura(n)
    fb ← FactorBalance(n)

    SI fb > 1:                                  # izquierda pesada
        SI FactorBalance(n.izquierda) < 0:      # caso LR
            n.izquierda ← RotarIzquierda(n.izquierda)
        DEVOLVER RotarDerecha(n)                # caso LL

    SI fb < -1:                                 # derecha pesada
        SI FactorBalance(n.derecha) > 0:        # caso RL
            n.derecha ← RotarDerecha(n.derecha)
        DEVOLVER RotarIzquierda(n)              # caso RR

    DEVOLVER n

FUNCIÓN Insertar(n, clave):
    SI n = nulo: DEVOLVER Nodo(clave)

    SI clave < n.clave:
        n.izquierda ← Insertar(n.izquierda, clave)
    SINO SI clave > n.clave:
        n.derecha ← Insertar(n.derecha, clave)
    SINO:
        DEVOLVER n        # no se permiten duplicados

    DEVOLVER Rebalancear(n)
```

### Árboles rojo-negro (mención)

- También son BST balanceados, pero con reglas de color en vez de factor de balance.
- Garantizan altura `O(log n)` con menos rotaciones que un AVL.
- Se usan en bibliotecas estándar (por ejemplo, mapas y conjuntos ordenados).

---

## 20. Ojo: no confundir los tres tipos de árbol

| Tipo | Qué guarda | Orden | Recorrido típico | ¿Se balancea? |
|---|---|---|---|---|
| **BST / AVL** | Claves ordenadas | Sí, por clave | Inorden → ordenado | Sí: rotaciones |
| **Árbol de juego** | Estados de la partida | No | DFS postorden (Minimax) | No: se limita la profundidad |
| **Árbol de decisión** | Preguntas y clases | No | Camino raíz → hoja | No: se limita `max_depth` |

Entonces:

- **Al árbol de juego no se le aplican rotaciones AVL.** Su "control" es `max_depth`, la heurística y la poda alfa-beta.
- **Al árbol de decisión tampoco.** Su control es `max_depth`, `min_samples_leaf` y la poda por impureza (el propio algoritmo corta ramas que no aportan).
- **El balanceo AVL es para BST**, donde sí existe un orden por clave y se quiere garantizar `O(log n)`.

Si te preguntan “¿el árbol de Minimax está balanceado?”, la respuesta correcta es:
**no se balancea; es un árbol de estados que se corta por profundidad, no un BST.**

---

## 21. Preguntas nuevas probables

1. **¿Cuál es la diferencia entre preorden, inorden y postorden?**
   Cambia el momento en que se visita la raíz: antes, en medio o después de los hijos.

2. **¿Qué recorrido usa Minimax y por qué?**
   Postorden con DFS: primero necesita el valor de los hijos para poder calcular el máximo o mínimo del padre.

3. **¿La poda alfa-beta cambia el recorrido?**
   No, sigue siendo DFS en postorden; solo evita explorar ramas que no pueden cambiar el resultado.

4. **¿Para qué sirve el inorden?**
   En un BST devuelve las claves ordenadas. En un árbol de juego o de decisión no aporta.

5. **¿Qué es el factor de balance?**
   `altura(izquierda) - altura(derecha)`. En un AVL debe ser -1, 0 o +1.

6. **¿Cuándo se aplica una rotación simple y cuándo una doble?**
   Simple en LL o RR; doble en LR o RL.

7. **¿Por qué importa balancear un BST?**
   Porque sin balanceo puede degenerar en una lista y pasar de `O(log n)` a `O(n)`.

8. **¿Se balancea el árbol de decisión?**
   No con rotaciones. Se controla con `max_depth` y `min_samples_leaf` para evitar sobreajuste.

9. **¿Cómo se entrena el árbol sin Minimax?**
   Con partidas humanas o de autoaprendizaje con una política simple; la etiqueta es la jugada del ganador o del humano, no la de Minimax.

10. **¿Qué mide la precisión en ese caso?**
    Cuánto imita al humano o a la política que generó los datos. Para medir fuerza hay que jugar partidas y calcular la tasa de victoria.
