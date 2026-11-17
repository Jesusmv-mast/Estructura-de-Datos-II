# Algoritmos: Grafos

## Archivos

| Archivo | Descripción |
| --- | --- |
| `grafo.py` | Representación de un grafo con lista y matriz de adyacencia |
| `dfs.py` | Búsqueda en profundidad (DFS) recursiva e iterativa |
| `bfs.py` | Búsqueda en anchura (BFS) y distancias en grafos no pesados |

## Conceptos básicos

Un **grafo** es un conjunto de vértices o nodos conectados por aristas. Puede ser:

- **Dirigido:** las aristas tienen dirección.
- **No dirigido:** las aristas se recorren en ambos sentidos.
- **Ponderado:** cada arista tiene un peso o costo.
- **No ponderado:** todas las aristas tienen el mismo costo.

## Representaciones

### Lista de adyacencia

Cada vértice guarda una lista de sus vecinos. Es eficiente cuando el grafo tiene pocas aristas.

```text
A: [B, C]
B: [A, D]
C: [A, D, E]
D: [B, C]
E: [C]
```

### Matriz de adyacencia

Se usa una matriz de `V × V`. La celda `[i][j]` vale `1` si existe una arista entre los vértices y `0` si no.

```text
    A B C D E
  A 0 1 1 0 0
  B 1 0 0 1 0
  C 1 0 0 1 1
  D 0 1 1 0 0
  E 0 0 1 0 0
```

| Representación | Ventaja | Desventaja |
| --- | --- | --- |
| Lista de adyacencia | Ahorra memoria con pocas aristas | Comprobar una arista puede ser más lento |
| Matriz de adyacencia | Comprobar una arista es inmediato | Ocupa O(V²) aunque haya pocas aristas |

## DFS

La **búsqueda en profundidad** visita un vértice y continúa por uno de sus vecinos hasta no poder avanzar; después retrocede. Se implementa con recursión o con una pila.

- Complejidad: O(V + E).
- Uso típico: detectar ciclos, componentes conexas y ordenamiento topológico.

## BFS

La **búsqueda en anchura** visita primero todos los vecinos de un vértice y después pasa al siguiente nivel. Se implementa con una cola.

- Complejidad: O(V + E).
- Uso típico: camino más corto en cantidad de aristas y recorrido por niveles.

## Cómo ejecutar

Desde esta carpeta:

```bash
python grafo.py
python dfs.py
python bfs.py
```

## Ejemplo de uso

```python
from dfs import dfs
from bfs import bfs, bfs_distancias

grafo = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C"],
}

print(dfs(grafo, "A"))
print(bfs(grafo, "A"))
print(bfs_distancias(grafo, "A"))
```
