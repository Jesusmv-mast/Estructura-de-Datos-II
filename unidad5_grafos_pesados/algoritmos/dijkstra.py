"""Camino mas corto desde un origen con el algoritmo de Dijkstra.

Autor: Charles Jesus Morales Velasco
Titulo: Algoritmo de Dijkstra
Version: 1.0.0
Fecha: 2026

Dijkstra funciona con aristas de peso no negativo. Usa una cola de
prioridad para visitar siempre el vertice pendiente con menor distancia.
"""

import heapq


def dijkstra(grafo, inicio):
    """Calcula las distancias minimas desde un vertice inicial.

    Args:
        grafo: Diccionario de adyacencia con pares (vecino, peso).
        inicio: Vertice desde donde comienzan los caminos.

    Returns:
        Tupla con el diccionario de distancias y el de anteriores.

    Raises:
        ValueError: Si alguna arista tiene peso negativo.
    """
    for vecinos in grafo.values():
        for _, peso in vecinos:
            if peso < 0:
                raise ValueError(
                    "Dijkstra no acepta aristas con peso negativo."
                )

    distancias = {vertice: float("inf") for vertice in grafo}
    anteriores = {vertice: None for vertice in grafo}
    distancias[inicio] = 0

    cola = [(0, inicio)]
    while cola:
        distancia_actual, actual = heapq.heappop(cola)

        if distancia_actual > distancias[actual]:
            continue

        for vecino, peso in grafo[actual]:
            nueva_distancia = distancia_actual + peso
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = actual
                heapq.heappush(cola, (nueva_distancia, vecino))

    return distancias, anteriores


def reconstruir_camino(anteriores, inicio, destino):
    """Reconstruye el camino desde inicio hasta destino.

    Args:
        anteriores: Diccionario de predecesores.
        inicio: Vertice de origen.
        destino: Vertice final.

    Returns:
        Lista con el camino, o lista vacia si no es alcanzable.
    """
    camino = []
    actual = destino

    while actual is not None:
        camino.append(actual)
        if actual == inicio:
            return list(reversed(camino))
        actual = anteriores[actual]

    return []


def main():
    """Ejecuta una demostracion del algoritmo de Dijkstra."""
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
    }

    print("=== Dijkstra desde A ===")
    distancias, anteriores = dijkstra(grafo, "A")

    for vertice, distancia in distancias.items():
        print(f"  {vertice}: {distancia}")

    camino = reconstruir_camino(anteriores, "A", "F")
    print(f"\nCamino A -> F: {' -> '.join(camino)}")
    print(f"Costo: {distancias['F']}")


if __name__ == "__main__":
    main()
