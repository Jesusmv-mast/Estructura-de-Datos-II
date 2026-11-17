"""Camino mas corto con el algoritmo de Bellman-Ford.

Autor: Charles Jesus Morales Velasco
Titulo: Algoritmo de Bellman-Ford
Version: 1.0.0
Fecha: 2026

Bellman-Ford acepta aristas con peso negativo y detecta ciclos de peso
negativo. Relaja todas las aristas V - 1 veces.
"""


def bellman_ford(vertices, aristas, inicio):
    """Calcula las distancias minimas desde un vertice inicial.

    Args:
        vertices: Lista de vertices del grafo.
        aristas: Lista de tuplas (origen, destino, peso).
        inicio: Vertice desde donde comienzan los caminos.

    Returns:
        Tupla con el diccionario de distancias y el de anteriores.

    Raises:
        ValueError: Si existe un ciclo de peso negativo alcanzable.
    """
    distancias = {vertice: float("inf") for vertice in vertices}
    anteriores = {vertice: None for vertice in vertices}
    distancias[inicio] = 0

    for _ in range(len(vertices) - 1):
        actualizado = False

        for origen, destino, peso in aristas:
            if distancias[origen] == float("inf"):
                continue

            nueva_distancia = distancias[origen] + peso
            if nueva_distancia < distancias[destino]:
                distancias[destino] = nueva_distancia
                anteriores[destino] = origen
                actualizado = True

        if not actualizado:
            break

    for origen, destino, peso in aristas:
        if distancias[origen] == float("inf"):
            continue
        if distancias[origen] + peso < distancias[destino]:
            raise ValueError(
                "El grafo contiene un ciclo de peso negativo alcanzable."
            )

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
    """Ejecuta una demostracion del algoritmo de Bellman-Ford."""
    vertices = ["A", "B", "C", "D"]
    aristas = [
        ("A", "B", 4),
        ("A", "C", 5),
        ("B", "C", -3),
        ("C", "D", 2),
    ]

    print("=== Bellman-Ford desde A ===")
    distancias, anteriores = bellman_ford(vertices, aristas, "A")

    for vertice, distancia in distancias.items():
        print(f"  {vertice}: {distancia}")

    camino = reconstruir_camino(anteriores, "A", "D")
    print(f"\nCamino A -> D: {' -> '.join(camino)}")
    print(f"Costo: {distancias['D']}")


if __name__ == "__main__":
    main()
