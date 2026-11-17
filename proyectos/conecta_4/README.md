# Conecta 4

Juego de **Conecta 4** en escritorio, escrito en Python con una arquitectura **MVC**
(Modelo–Vista–Controlador). Es una versión reducida del clásico: un tablero de
**4 filas × 5 columnas** donde gana quien consiga **4 fichas seguidas**.

![Python](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-1e4fa3?style=flat-square)
![Arquitectura](https://img.shields.io/badge/arquitectura-MVC-green?style=flat-square)

---

## ✨ Características

- Tablero compacto de **4 × 5** (fácil de probar y depurar).
- Detección de victoria en las **4 direcciones**: horizontal, vertical y las dos diagonales.
- Detección de **empate** cuando el tablero se llena.
- Fichas que **caen por gravedad** al fondo de la columna.
- Columna llena → el movimiento se rechaza con un aviso en pantalla.
- Botón **Reiniciar** para empezar una partida nueva.
- La vista no contiene lógica de juego: solo dibuja y reporta clics.

---

## 🚀 Requisitos

- **Python 3.10 o superior**
- **Tkinter** — incluido en la instalación estándar de Python en Windows y macOS.
  En Linux puede hacer falta instalarlo:

  ```bash
  # Debian / Ubuntu
  sudo apt install python3-tk
  ```

- **ttkbootstrap** — tema moderno para Tkinter. Se instala con:

  ```bash
  pip install ttkbootstrap
  ```

- **scikit-learn** y **joblib** — solo necesarios si quieres volver a entrenar
  el árbol de decisión (`scripts/train_tree.py`) o visualizarlo
  (`scripts/visualize_tree.py`). Para jugar no hacen falta.

El juego en sí usa la biblioteca estándar más `ttkbootstrap` para la interfaz.

También puedes instalar todas las dependencias de una vez:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecutar

Desde la raíz del proyecto:

```bash
python main.py
```

> Es importante ejecutarlo desde la raíz, porque los módulos se importan como
> `model.game_model`, `view.gui_view` y `controller.game_controller`.

---

## 🕹️ Cómo jugar

1. Haz clic en una **columna** para soltar tu ficha.
2. Las fichas caen hasta el fondo o hasta la pila de la columna.
3. Cambia de turno automáticamente: empieza **X** (rojo), luego **O** (amarillo).
4. Gana quien consiga **4 fichas en línea** (horizontal, vertical o diagonal).
5. Si el tablero se llena sin ganador, hay **empate**.
6. Pulsa **Reiniciar** para jugar otra vez.

La barra superior muestra el estado: de quién es el turno, la victoria, el empate
o el aviso de columna llena.

---

## 📁 Estructura del proyecto

```
conecta_4/
├── main.py                     # Punto de entrada: crea la app y el bucle principal
├── trace_backtracking.py       # Script educativo: traza de recursión y backtracking
├── README.md
├── .flake8                     # Configuración de flake8 (max-line-length = 79)
├── .gitignore
│
├── controller/
│   ├── __init__.py
│   └── game_controller.py      # Coordina modelo, vista y agentes de IA
│
├── model/
│   ├── __init__.py
│   ├── game_model.py           # Estado del tablero, reglas, victoria/empate, undo
│   ├── minimax_agent.py        # IA con Minimax + poda alfa-beta y heurística
│   ├── decision_tree_agent.py  # IA con árbol de decisión entrenado (scikit-learn)
│   ├── ml_agent.py             # Generador de dataset (Minimax vs jugador aleatorio)
│   └── tree_model.joblib       # Modelo entrenado del árbol de decisión
│
├── view/
│   ├── __init__.py
│   ├── app.py                  # Pantallas: Inicio → Modo → Dificultad → Juego
│   ├── gui_view.py             # Dibujo del tablero, clics, métricas, camino de decisión
│   └── menu_view.py            # Pantallas de menú (inicio, modo, dificultad)
│
├── data/
│   └── minimax_games.csv       # Dataset usado para entrenar el árbol de decisión
│
├── scripts/
│   ├── compare_agents.py       # Compara Minimax vs Árbol (precisión y latencia)
│   ├── train_tree.py           # Entrena el árbol y guarda tree_model.joblib
│   └── visualize_tree.py       # Visualiza los primeros 3 niveles del árbol
│
└── tests/
    ├── __init__.py
    ├── test_game_model.py      # Tests del modelo (victorias, empate, undo…)
    ├── test_game_controller_ai.py  # Tests del controlador con IA (FakeView)
    ├── test_minimax_agent.py   # Tests del agente Minimax
    └── test_ml_agent.py        # (reservado, actualmente vacío)
```

Cada paquete incluye su `__init__.py` para ser importado como módulo.

---

## 🧱 Arquitectura MVC

El proyecto separa las tres responsabilidades. La comunicación siempre pasa por
el controlador: la vista nunca toca el modelo directamente.

```
        ┌───────────────────────────────┐
        │            Vista              │
        │  view/gui_view.py             │
        │  dibuja el tablero            │
        │  emite clics de columna       │
        └───────────┬───────────────────┘
                    │  handler(col) / reiniciar
                    ▼
        ┌───────────────────────────────┐
        │         Controlador           │
        │  controller/game_controller.py│
        │  decide qué hacer con cada    │
        │  evento y qué mensaje mostrar │
        └───────────┬───────────────────┘
             ▲      │ make_move / check_winner
             │      ▼
        ┌───────────────────────────────┐
        │           Modelo              │
        │  model/game_model.py          │
        │  tablero, reglas, turnos      │
        └───────────────────────────────┘
```

### Flujo de un clic

1. El usuario hace clic → `GameView._on_click` valida que el clic caiga dentro
   del tablero y calcula la columna.
2. Llama al handler registrado → `GameController.on_column_click(col)`.
3. El controlador pide al modelo `make_move(col, player)`.
   - Si devuelve `False`, la columna está llena y solo se avisa.
4. Comprueba `check_winner` → `is_draw` → si no hay fin, `switch_player`.
5. El controlador llama `_update_view(mensaje)`, que redibuja el tablero y
   actualiza la barra de estado.

---

## 🗃️ Estructura de datos principal

El modelo se apoya en dos estructuras clave:

| Estructura | Definición | Para qué sirve |
|---|---|---|
| `board` | Lista de listas `board[ fila ][ columna ]` con `' '`, `'X'` u `'O'` | Representación del tablero para dibujarlo y leer líneas |
| `heights` | Lista de `cols` enteros: `heights[c]` = fichas apiladas en la columna `c` | Calcular dónde cae la siguiente ficha **en O(1)** sin recorrer la columna |

### Constantes

```python
ROWS = 4        # filas
COLS = 5        # columnas
CONNECT = 4     # fichas seguidas para ganar
EMPTY = ' '     # casilla vacía
```

Son parámetros por defecto del constructor, así que se puede jugar con otros
tamaños:

```python
model = GameModel(rows=6, cols=7, connect=4)   # Conecta 4 clásico
```

---

## 🔍 Detección de ganador

Para cada casilla del tablero se prueban **4 direcciones**:

```python
directions = ((0, 1),    # →  horizontal
              (1, 0),    # ↓  vertical
              (1, 1),    # ↘  diagonal descendente
              (1, -1))   # ↙  diagonal ascendente
```

`_line_matches` avanza `connect` pasos en esa dirección y comprueba que:

- todas las casillas quedan **dentro del tablero** (si se sale, descarta),
- todas contienen la **ficha del jugador**.

Si alguna dirección coincide, hay victoria. Coste: **O(filas × columnas × 4 × connect)**,
despreciable para tableros pequeños.

---

## 🧪 Tests

```bash
python -m pytest tests -v
```

> `pytest` está instalado en el `venv` del proyecto. Si no lo tienes:
> `pip install pytest`

**27 tests, todos pasando**, distribuidos en cuatro archivos:

| Archivo | Tests | Qué verifica |
|---------|-------|--------------|
| `tests/test_game_model.py` | 8 | Victorias (vertical, horizontal, diagonales), columna llena, empate, `undo` |
| `tests/test_game_controller_ai.py` | 9 | Controlador con IA (modos, turnos automáticos, clics ignorados, métricas, reinicio) |
| `tests/test_minimax_agent.py` | 8 | Victoria inmediata, bloqueo del oponente, backtracking sin modificar tablero, conteo de nodos, heurística |
| `tests/test_ml_agent.py` | 2 | Generación de dataset (`encode_board`) |

Son de **integración** y usan una **vista falsa** (`FakeView`) para probar
modelo + controlador juntos **sin abrir ventanas**. Gracias a eso los tests
corren rápido y funcionan sin pantalla (incluso en CI).

### El patrón `FakeView`

```python
class FakeView:
    """Vista falsa que registra lo que el controlador le pide."""
    def set_column_click_handler(self, handler): ...
    def set_restart_handler(self, handler): ...
    def set_mode_handler(self, handler): ...
    def set_status(self, text): ...
    def draw_board(self, board): ...
    def schedule_delayed(self, delay_ms, callback): ...
    def set_metrics(self, nodes, elapsed_seconds): ...
    def clear_metrics(self): ...
    def show_decision_path(self, steps, move): ...
    def clear_decision_path(self): ...
```

Implementa la misma interfaz que `GameView`, pero en lugar de dibujar **guarda
lo que le llega**. Así se puede escribir:

```python
view, _ = make_game()
view.column_handler(0)              # como si el usuario hiciera clic
assert view.status == 'Turno de Amarillo'  # comprobar el resultado
```

Es **pruebas de doble (*test double*)**: se testea la lógica sin depender de
la GUI.

---

## 🔧 Código de estilo

El proyecto sigue **PEP 8** con `max-line-length = 79`, configurado en `.flake8`:

```bash
python -m flake8 .
```

> `flake8` está en el `venv`. Excluye `venv`, `__pycache__` y `.git`.

**Estado actual: limpio**, sin avisos de `flake8` (W292, W293 corregidos).

---

## 💡 Posibles mejoras

- **[x]** IA rival con minimax y poda alfa-beta (ya implementada).
- **[ ]** Marcar visualmente las 4 fichas ganadoras.
- **[ ]** Contador de victorias X vs. O.
- **[x]** Escribir tests del modelo → 25 tests ✔
- **[ ]** Animación de la ficha al caer.
- **[x]** Limpiar avisos de `flake8` ✔

---

## 📄 Licencia

Proyecto académico — *Estructura de Datos II*.
