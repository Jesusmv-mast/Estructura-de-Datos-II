"""Busqueda en anchura (BFS) sobre un grafo.

Autor: Charles Jesus Morales Velasco
Titulo: Recorrido BFS y distancias en grafos no pesados
Version: 1.0.0
Fecha: 2026
"""

from collections import deque


def bfs(grafo, inicio):
    """Recorre un grafo en anchura.

    Args:
        grafo: Diccionario de listas de adyacencia.
        inicio: Vertice desde donde comienza el recorrido.

    Returns:
        Lista con los vertices en el orden en que fueron visitados.
    """
    visitados = {inicio}
    cola = deque([inicio])
    orden = []

    while cola:
        actual = cola.popleft()
        orden.append(actual)

        for vecino in grafo[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return orden


def bfs_distancias(grafo, inicio):
    """Calcula distancias minimas en cantidad de aristas.

    Args:
        grafo: Diccionario de listas de adyacencia.
        inicio: Vertice desde donde comienza el recorrido.

    Returns:
        Diccionario con la distancia desde inicio hasta cada vertice.
    """
    distancias = {vertice: float("inf") for vertice in grafo}
    distancias[inicio] = 0
    cola = deque([inicio])

    while cola:
        actual = cola.popleft()
        for vecino in grafo[actual]:
            if distancias[vecino] == float("inf"):
                distancias[vecino] = distancias[actual] + 1
                cola.append(vecino)

    return distancias


def main():
    """Ejecuta una demostracion de BFS."""
    grafo = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D", "E"],
        "D": ["B", "C"],
        "E": ["C"],
    }

    print("=== BFS ===")
    print(bfs(grafo, "A"))

    print("\n=== Distancias desde A ===")
    for vertice, distancia in bfs_distancias(grafo, "A").items():
        print(f"  {vertice}: {distancia}")


if __name__ == "__main__":
    main()
