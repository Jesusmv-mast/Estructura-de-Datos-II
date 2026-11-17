# Tablero Tres en Raya con nodos y árbol

## Descripción

Implementación de las clases `Nodo` y `Arbol` para representar un tablero de **Tres en Raya** mediante una matriz de 3x3 nodos. Cada nodo almacena un valor (`'X'`, `'O'` o `None`) y referencias a un hijo izquierdo y un hijo derecho.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `nodo.py` | Clase `Nodo` con getters, setters, validaciones y métodos auxiliares |
| `arbol.py` | Clase `Arbol` que administra la matriz 3x3 de nodos y las jugadas |

## Cómo ejecutar

Desde esta carpeta:

```bash
python arbol.py
```

También se puede ejecutar `nodo.py` de forma independiente:

```bash
python nodo.py
```

> `arbol.py` importa `Nodo` desde `nodo.py`, por lo que ambos archivos deben permanecer en la misma carpeta.

## Funcionalidades

### Clase `Nodo`

- `get_elemento()` / `set_elemento(valor)`: leen y escriben el valor del nodo.
- `get_hijo_izquierdo()` / `set_hijo_izquierdo(nodo)`: acceden al hijo izquierdo.
- `get_hijo_derecho()` / `set_hijo_derecho(nodo)`: acceden al hijo derecho.
- `tiene_hijo_izquierdo()` / `tiene_hijo_derecho()`: verifican la existencia de hijos.
- `es_hoja()`: indica si el nodo no tiene hijos.
- Validaciones: el elemento debe ser `'X'`, `'O'` o `None`; los hijos deben ser `Nodo` o `None`.

### Clase `Arbol`

- `get_raiz()` / `set_raiz(nodo)`: administran la raíz del árbol.
- `get_matriz()`: retorna la matriz completa de nodos.
- `get_nodo(fila, columna)` / `get_valor(fila, columna)`: consultan una celda.
- `set_valor(fila, columna, valor)`: coloca una ficha si la celda está vacía.
- `esta_vacia(fila, columna)`: indica si una celda está libre.
- `tablero_lleno()`: indica si ya no quedan celdas libres.
- `reiniciar()`: crea un tablero nuevo.
- `mostrar_tablero()`: imprime el tablero en consola.
- Validaciones: posición dentro de la matriz y celda no ocupada.

## Ejemplo de uso

```python
from arbol import Arbol

arbol = Arbol()
arbol.set_valor(0, 0, "X")
arbol.set_valor(1, 1, "O")
arbol.mostrar_tablero()
```
