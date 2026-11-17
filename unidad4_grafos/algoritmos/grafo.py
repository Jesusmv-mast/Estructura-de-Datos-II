"""Representacion de grafos con lista y matriz de adyacencia.

Autor: Charles Jesus Morales Velasco
Titulo: Grafo no dirigido con lista y matriz de adyacencia
Version: 1.0.0
Fecha: 2026
"""


class Grafo:
    """Grafo no dirigido representado con una lista de adyacencia.

    Attributes:
        _adyacencia: Diccionario que asocia cada vertice con sus vecinos.
    """

    def __init__(self):
        """Inicializa un grafo vacio."""
        self._adyacencia = {}

    def agregar_vertice(self, vertice):
        """Agrega un vertice al grafo si no existe."""
        if vertice not in self._adyacencia:
            self._adyacencia[vertice] = []

    def agregar_arista(self, origen, destino):
        """Agrega una arista no dirigida entre dos vertices."""
        self.agregar_vertice(origen)
        self.agregar_vertice(destino)
        self._adyacencia[origen].append(destino)
        self._adyacencia[destino].append(origen)

    def vecinos(self, vertice):
        """Retorna la lista de vecinos de un vertice."""
        return list(self._adyacencia[vertice])

    def lista_adyacencia(self):
        """Retorna una copia de la lista de adyacencia."""
        return {
            vertice: list(vecinos)
            for vertice, vecinos in self._adyacencia.items()
        }

    def matriz_adyacencia(self):
        """Construye la matriz de adyacencia del grafo.

        Returns:
            Tupla con la lista de vertices y la matriz de enteros.
        """
        vertices = list(self._adyacencia)
        matriz = [[0] * len(vertices) for _ in vertices]
        posiciones = {vertice: i for i, vertice in enumerate(vertices)}

        for origen, vecinos in self._adyacencia.items():
            for destino in vecinos:
                matriz[posiciones[origen]][posiciones[destino]] = 1

        return vertices, matriz

    def grado(self, vertice):
        """Retorna el grado de un vertice."""
        return len(self._adyacencia[vertice])

    def mostrar_lista(self):
        """Imprime la lista de adyacencia."""
        print("Lista de adyacencia:")
        for vertice, vecinos in self._adyacencia.items():
            print(f"  {vertice}: {vecinos}")

    def mostrar_matriz(self):
        """Imprime la matriz de adyacencia."""
        vertices, matriz = self.matriz_adyacencia()
        print("Matriz de adyacencia:")
        print("    " + " ".join(vertices))
        for vertice, fila in zip(vertices, matriz):
            valores = " ".join(str(valor) for valor in fila)
            print(f"  {vertice} {valores}")

    def __len__(self):
        """Retorna la cantidad de vertices."""
        return len(self._adyacencia)

    def __str__(self):
        """Retorna la lista de adyacencia como texto."""
        return str(self.lista_adyacencia())


def main():
    """Ejecuta una demostracion de las representaciones."""
    grafo = Grafo()
    for vertice in "ABCDE":
        grafo.agregar_vertice(vertice)

    aristas = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "D"),
        ("C", "E"),
    ]
    for origen, destino in aristas:
        grafo.agregar_arista(origen, destino)

    print("=== Grafo no dirigido ===")
    print(f"Vertices: {len(grafo)}")
    grafo.mostrar_lista()
    print()
    grafo.mostrar_matriz()
    print()
    print(f"Grado de A: {grafo.grado('A')}")
    print(f"Grado de C: {grafo.grado('C')}")


if __name__ == "__main__":
    main()
