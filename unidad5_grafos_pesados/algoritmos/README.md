# Algoritmos: Grafos pesados

## Archivos

| Archivo | Descripción |
| --- | --- |
| `dijkstra.py` | Camino más corto desde un origen con pesos no negativos |
| `bellman_ford.py` | Camino más corto con pesos negativos y detección de ciclos negativos |
| `kruskal.py` | Árbol de expansión mínima usando Union-Find |
| `prim.py` | Árbol de expansión mínima creciendo desde un vértice |

## Grafos ponderados

Un grafo ponderado asigna un **peso** o costo a cada arista. Se representa con un diccionario de adyacencia cuyos valores son pares `(vecino, peso)`:

```python
grafo = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 10)],
    "C": [("B", 5)],
    "D": [],
}
```

## Dijkstra

Encuentra el camino de menor costo desde un origen cuando **todos los pesos son no negativos**. Usa una cola de prioridad y relaja las aristas del vértice con menor distancia pendiente.

- Complejidad con montículo: O((V + E) log V).
- No funciona correctamente con pesos negativos.
- En este ejemplo también se reconstruye el camino usando los predecesores.

## Bellman-Ford

Relaja todas las aristas `V - 1` veces. Puede trabajar con pesos negativos y, con una pasada adicional, detecta ciclos de peso negativo alcanzables.

- Complejidad: O(V · E).
- Es más lento que Dijkstra, pero más general.
- En este ejemplo también se reconstruye el camino.

## Kruskal

Ordena las aristas de menor a mayor peso y las agrega si no forman un ciclo. Usa **Union-Find** para saber si dos vértices ya pertenecen al mismo conjunto.

- Complejidad: O(E log E), dominada por el ordenamiento.
- Funciona con grafos no dirigidos y conexos.
- Si el grafo no es conexo, se lanza `ValueError`.

## Prim

Comienza en un vértice y hace crecer el árbol agregando siempre la arista más liviana que conecta un vértice nuevo. Usa una cola de prioridad.

- Complejidad con montículo: O((V + E) log V).
- Funciona con grafos no dirigidos y conexos.
- Si el grafo no es conexo, se lanza `ValueError`.

## Comparación

| Algoritmo | Problema | Pesos negativos | Complejidad |
| --- | --- | --- | --- |
| Dijkstra | Camino más corto desde un origen | No | O((V + E) log V) |
| Bellman-Ford | Camino más corto desde un origen | Sí, sin ciclos negativos | O(V · E) |
| Kruskal | Árbol de expansión mínima | Sí | O(E log E) |
| Prim | Árbol de expansión mínima | Sí | O((V + E) log V) |

## Cómo ejecutar

Desde esta carpeta:

```bash
python dijkstra.py
python bellman_ford.py
python kruskal.py
python prim.py
```

## Ejemplo de uso

```python
from dijkstra import dijkstra, reconstruir_camino
from bellman_ford import bellman_ford

grafo = {
    "A": [("B", 4), ("C", 2)],
    "B": [("C", 5)],
    "C": [],
}

distancias, anteriores = dijkstra(grafo, "A")
print(distancias)
print(reconstruir_camino(anteriores, "A", "B"))

vertices = ["A", "B", "C"]
aristas = [("A", "B", 4), ("A", "C", 5), ("B", "C", -3)]
distancias, anteriores = bellman_ford(vertices, aristas, "A")
print(distancias)
```
