"""Busqueda en profundidad (DFS) sobre un grafo.

Autor: Charles Jesus Morales Velasco
Titulo: Recorrido DFS recursivo e iterativo
Version: 1.0.0
Fecha: 2026
"""


def dfs(grafo, inicio, visitados=None, orden=None):
    """Recorre un grafo en profundidad de forma recursiva.

    Args:
        grafo: Diccionario de listas de adyacencia.
        inicio: Vertice desde donde comienza el recorrido.
        visitados: Conjunto compartido entre llamadas.
        orden: Lista donde se guarda el orden de visita.

    Returns:
        Lista con los vertices en el orden en que fueron visitados.
    """
    if visitados is None:
        visitados = set()
    if orden is None:
        orden = []

    visitados.add(inicio)
    orden.append(inicio)

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            dfs(grafo, vecino, visitados, orden)

    return orden


def dfs_iterativo(grafo, inicio):
    """Recorre un grafo en profundidad usando una pila."""
    visitados = set()
    orden = []
    pila = [inicio]

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue

        visitados.add(actual)
        orden.append(actual)

        for vecino in reversed(grafo[actual]):
            if vecino not in visitados:
                pila.append(vecino)

    return orden


def main():
    """Ejecuta una demostracion de DFS."""
    grafo = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D", "E"],
        "D": ["B", "C"],
        "E": ["C"],
    }

    print("=== DFS recursivo ===")
    print(dfs(grafo, "A"))

    print("\n=== DFS iterativo ===")
    print(dfs_iterativo(grafo, "A"))


if __name__ == "__main__":
    main()
