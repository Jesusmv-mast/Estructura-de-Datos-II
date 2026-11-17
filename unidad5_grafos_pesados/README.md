# Unidad 5: Grafos pesados

En esta unidad se estudian los **grafos ponderados** (grafos con peso en las aristas) y los algoritmos clásicos asociados.

## Contenido

- [Algoritmos de grafos pesados](algoritmos/README.md)

## Temas

- Representación de grafos ponderados.
- Camino más corto desde un origen:
  - Algoritmo de Dijkstra.
  - Algoritmo de Bellman-Ford.
- Caminos mínimos entre todos los pares:
  - Algoritmo de Floyd-Warshall.
- Árbol de expansión mínima:
  - Algoritmo de Kruskal.
  - Algoritmo de Prim.

## Algoritmos incluidos

| Archivo | Descripción |
| --- | --- |
| [`dijkstra.py`](algoritmos/dijkstra.py) | Camino más corto con pesos no negativos |
| [`bellman_ford.py`](algoritmos/bellman_ford.py) | Camino más corto con pesos negativos y detección de ciclos negativos |
| [`kruskal.py`](algoritmos/kruskal.py) | Árbol de expansión mínima con Union-Find |
| [`prim.py`](algoritmos/prim.py) | Árbol de expansión mínima con cola de prioridad |

## Pendiente

El algoritmo de Floyd-Warshall sigue como tema de la unidad; no se incluyó porque no formaba parte de los archivos entregados.
