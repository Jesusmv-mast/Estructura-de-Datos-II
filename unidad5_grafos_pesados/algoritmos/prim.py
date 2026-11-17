"""Arbol de expansion minima con el algoritmo de Prim.

Autor: Charles Jesus Morales Velasco
Titulo: Algoritmo de Prim con cola de prioridad
Version: 1.0.0
Fecha: 2026

Prim crece el arbol desde un vertice inicial. En cada paso agrega la
arista de menor peso que conecta el arbol con un vertice no visitado.
"""

import heapq


def prim(grafo, inicio):
    """Calcula el arbol de expansion minima de un grafo conexo.

    Args:
        grafo: Diccionario de adyacencia con pares (vecino, peso).
        inicio: Vertice desde donde crece el arbol.

    Returns:
        Tupla con las aristas del arbol y su costo total.

    Raises:
        ValueError: Si el grafo no es conexo.
    """
    visitados = {inicio}
    arbol = []
    costo_total = 0

    cola = [
        (peso, inicio, vecino)
        for vecino, peso in grafo[inicio]
    ]
    heapq.heapify(cola)

    while cola:
        peso, origen, destino = heapq.heappop(cola)

        if destino in visitados:
            continue

        visitados.add(destino)
        arbol.append((origen, destino, peso))
        costo_total += peso

        for vecino, peso_vecino in grafo[destino]:
            if vecino not in visitados:
                heapq.heappush(cola, (peso_vecino, destino, vecino))

    if len(visitados) != len(grafo):
        raise ValueError("El grafo no es conexo.")

    return arbol, costo_total


def main():
    """Ejecuta una demostracion del algoritmo de Prim."""
    grafo = {
        "A": [("B", 4), ("H", 8)],
        "B": [("A", 4), ("C", 8), ("H", 11)],
        "C": [("B", 8), ("D", 7), ("F", 4), ("I", 2)],
        "D": [("C", 7), ("E", 9), ("F", 14)],
        "E": [("D", 9), ("F", 10)],
        "F": [("C", 4), ("D", 14), ("E", 10), ("G", 2)],
        "G": [("F", 2), ("H", 1), ("I", 6)],
        "H": [("A", 8), ("B", 11), ("G", 1), ("I", 7)],
        "I": [("C", 2), ("G", 6), ("H", 7)],
    }

    print("=== Prim desde A ===")
    arbol, costo = prim(grafo, "A")

    for origen, destino, peso in arbol:
        print(f"  {origen} - {destino}: {peso}")

    print(f"\nCosto total: {costo}")


if __name__ == "__main__":
    main()
