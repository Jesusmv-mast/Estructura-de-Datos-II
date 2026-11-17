"""Arbol de expansion minima con el algoritmo de Kruskal.

Autor: Charles Jesus Morales Velasco
Titulo: Algoritmo de Kruskal con Union-Find
Version: 1.0.0
Fecha: 2026

Kruskal ordena las aristas por peso y las agrega al bosque si no forman
un ciclo. Para detectar ciclos se usa la estructura Union-Find.
"""


class UnionFind:
    """Estructura de conjuntos disjuntos con compresion de caminos."""

    def __init__(self, vertices):
        """Inicializa cada vertice como un conjunto independiente."""
        self._padre = {vertice: vertice for vertice in vertices}
        self._rango = {vertice: 0 for vertice in vertices}

    def encontrar(self, vertice):
        """Retorna el representante del conjunto del vertice."""
        if self._padre[vertice] != vertice:
            self._padre[vertice] = self.encontrar(self._padre[vertice])
        return self._padre[vertice]

    def unir(self, primero, segundo):
        """Une dos conjuntos y retorna False si ya estaban unidos."""
        raiz_primero = self.encontrar(primero)
        raiz_segundo = self.encontrar(segundo)

        if raiz_primero == raiz_segundo:
            return False

        if self._rango[raiz_primero] < self._rango[raiz_segundo]:
            raiz_primero, raiz_segundo = raiz_segundo, raiz_primero

        self._padre[raiz_segundo] = raiz_primero
        if self._rango[raiz_primero] == self._rango[raiz_segundo]:
            self._rango[raiz_primero] += 1

        return True


def kruskal(vertices, aristas):
    """Calcula el arbol de expansion minima de un grafo conexo.

    Args:
        vertices: Lista de vertices del grafo.
        aristas: Lista de tuplas (origen, destino, peso).

    Returns:
        Tupla con las aristas del arbol y su costo total.

    Raises:
        ValueError: Si el grafo no es conexo.
    """
    conjuntos = UnionFind(vertices)
    arbol = []
    costo_total = 0

    for origen, destino, peso in sorted(aristas, key=lambda arista: arista[2]):
        if conjuntos.unir(origen, destino):
            arbol.append((origen, destino, peso))
            costo_total += peso

            if len(arbol) == len(vertices) - 1:
                break

    if len(arbol) != len(vertices) - 1:
        raise ValueError("El grafo no es conexo.")

    return arbol, costo_total


def main():
    """Ejecuta una demostracion del algoritmo de Kruskal."""
    vertices = list("ABCDEFGHI")
    aristas = [
        ("A", "B", 4),
        ("A", "H", 8),
        ("B", "C", 8),
        ("B", "H", 11),
        ("C", "D", 7),
        ("C", "F", 4),
        ("C", "I", 2),
        ("D", "E", 9),
        ("D", "F", 14),
        ("E", "F", 10),
        ("F", "G", 2),
        ("G", "H", 1),
        ("G", "I", 6),
        ("H", "I", 7),
    ]

    print("=== Kruskal ===")
    arbol, costo = kruskal(vertices, aristas)

    for origen, destino, peso in arbol:
        print(f"  {origen} - {destino}: {peso}")

    print(f"\nCosto total: {costo}")


if __name__ == "__main__":
    main()
