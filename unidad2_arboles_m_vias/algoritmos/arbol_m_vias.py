"""Arbol M-vias de busqueda (arbol multicamino).

Autor: Charles Jesus Morales Velasco
Titulo: Arbol M-vias con busqueda, insercion y recorrido
Version: 1.0.0
Fecha: 2026

Un arbol M-vias permite hasta M hijos y M - 1 claves por nodo.
Este ejemplo mantiene el arbol balanceado: cuando un nodo supera el
maximo de claves, se divide y la clave media sube al padre.
"""

from bisect import bisect_left
from collections import deque


class NodoMVias:
    """Nodo de un arbol M-vias.

    Attributes:
        claves: Claves ordenadas del nodo.
        hijos: Referencias a los hijos. Un nodo con k claves tiene k + 1
            hijos si no es hoja.
    """

    def __init__(self):
        """Inicializa un nodo sin claves ni hijos."""
        self.claves = []
        self.hijos = []

    def es_hoja(self):
        """Indica si el nodo no tiene hijos."""
        return len(self.hijos) == 0

    def __repr__(self):
        """Representacion tecnica del nodo."""
        return f"NodoMVias(claves={self.claves!r})"


class ArbolMVias:
    """Arbol de busqueda M-vias balanceado.

    Args:
        orden: Cantidad maxima de hijos por nodo. Debe ser al menos 3.
    """

    def __init__(self, orden=3):
        """Crea un arbol vacio con el orden indicado."""
        if orden < 3:
            raise ValueError("El orden debe ser mayor o igual a 3.")
        self._orden = orden
        self._max_claves = orden - 1
        self._raiz = NodoMVias()

    @property
    def orden(self):
        """Retorna el orden del arbol."""
        return self._orden

    @property
    def raiz(self):
        """Retorna el nodo raiz."""
        return self._raiz

    def esta_vacio(self):
        """Indica si el arbol no tiene claves."""
        return len(self._raiz.claves) == 0 and self._raiz.es_hoja()

    def buscar(self, clave):
        """Busca una clave en el arbol.

        Args:
            clave: Valor que se desea buscar.

        Returns:
            True si la clave existe, False en caso contrario.
        """
        nodo = self._raiz
        while nodo is not None:
            indice = bisect_left(nodo.claves, clave)
            if indice < len(nodo.claves) and nodo.claves[indice] == clave:
                return True
            if nodo.es_hoja():
                return False
            nodo = nodo.hijos[indice]
        return False

    def insertar(self, clave):
        """Inserta una clave y divide los nodos que se desbordan.

        Args:
            clave: Valor que se desea insertar.

        Returns:
            True si se inserto, False si la clave ya existia.
        """
        if self.buscar(clave):
            return False

        nodo = self._raiz
        ruta = []

        while not nodo.es_hoja():
            indice = bisect_left(nodo.claves, clave)
            ruta.append((nodo, indice))
            nodo = nodo.hijos[indice]

        nodo.claves.insert(bisect_left(nodo.claves, clave), clave)

        while len(nodo.claves) > self._max_claves:
            clave_media, nodo_derecho = self._dividir(nodo)
            if not ruta:
                nueva_raiz = NodoMVias()
                nueva_raiz.claves = [clave_media]
                nueva_raiz.hijos = [nodo, nodo_derecho]
                self._raiz = nueva_raiz
                break

            padre, indice = ruta.pop()
            padre.claves.insert(indice, clave_media)
            padre.hijos.insert(indice + 1, nodo_derecho)
            nodo = padre

        return True

    def _dividir(self, nodo):
        """Divide un nodo que supero el maximo de claves.

        Args:
            nodo: Nodo que se va a dividir.

        Returns:
            Tupla con la clave media y el nuevo nodo derecho.
        """
        medio = len(nodo.claves) // 2
        clave_media = nodo.claves[medio]

        nodo_derecho = NodoMVias()
        nodo_derecho.claves = nodo.claves[medio + 1:]
        nodo.claves = nodo.claves[:medio]

        if not nodo.es_hoja():
            nodo_derecho.hijos = nodo.hijos[medio + 1:]
            nodo.hijos = nodo.hijos[:medio + 1]

        return clave_media, nodo_derecho

    def recorrido(self):
        """Retorna las claves en orden ascendente."""
        resultado = []
        self._recorrer(self._raiz, resultado)
        return resultado

    def _recorrer(self, nodo, resultado):
        """Recorre el subarbol en inorden."""
        for indice, clave in enumerate(nodo.claves):
            if not nodo.es_hoja():
                self._recorrer(nodo.hijos[indice], resultado)
            resultado.append(clave)
        if not nodo.es_hoja():
            self._recorrer(nodo.hijos[-1], resultado)

    def altura(self):
        """Retorna la altura del arbol (una hoja tiene altura 0)."""
        if self.esta_vacio():
            return 0
        altura = 0
        nodo = self._raiz
        while not nodo.es_hoja():
            altura += 1
            nodo = nodo.hijos[0]
        return altura

    def niveles(self):
        """Retorna una lista con las claves de cada nivel."""
        if self.esta_vacio():
            return []

        resultado = []
        cola = deque([self._raiz])
        while cola:
            nivel = []
            for _ in range(len(cola)):
                nodo = cola.popleft()
                nivel.append(nodo.claves)
                cola.extend(nodo.hijos)
            resultado.append(nivel)
        return resultado

    def __str__(self):
        """Muestra el arbol por niveles."""
        if self.esta_vacio():
            return "ArbolMVias([])"
        lineas = []
        for nivel, nodos in enumerate(self.niveles()):
            lineas.append(f"Nivel {nivel}: {nodos}")
        return "\n".join(lineas)


def main():
    """Ejecuta una demostracion del arbol M-vias."""
    arbol = ArbolMVias(orden=3)
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 40, 50, 15]

    print("=== Arbol M-vias de orden 3 (arbol 2-3) ===")
    for valor in valores:
        arbol.insertar(valor)

    print(arbol)
    print(f"\nRecorrido: {arbol.recorrido()}")
    print(f"Altura: {arbol.altura()}")
    print(f"Buscar 17: {arbol.buscar(17)}")
    print(f"Buscar 99: {arbol.buscar(99)}")
    print(f"Insertar 17 de nuevo: {arbol.insertar(17)}")


if __name__ == "__main__":
    main()
