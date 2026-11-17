"""Arbol B+ con busqueda, insercion y consultas por rango.

Autor: Charles Jesus Morales Velasco
Titulo: Arbol B+ con hojas enlazadas
Version: 1.0.0
Fecha: 2026

En un arbol B+ todas las claves reales viven en las hojas. Los nodos
internos solo guardan separadores para dirigir la busqueda. Las hojas
estan enlazadas, lo que permite recorrer los datos en orden.

Convencion usada: cada separador es la clave maxima del subarbol
izquierdo. Si una clave es igual al separador, se desciende por la
izquierda.
"""

from bisect import bisect_left


class NodoBPlus:
    """Nodo de un arbol B+."""

    def __init__(self, hoja=False):
        """Inicializa un nodo indicando si es hoja."""
        self.hoja = hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None

    def __repr__(self):
        """Representacion tecnica del nodo."""
        return f"NodoBPlus(hoja={self.hoja}, claves={self.claves!r})"


class ArbolBPlus:
    """Arbol B+ con hojas enlazadas.

    Args:
        orden: Cantidad maxima de hijos por nodo. Debe ser al menos 3.
    """

    def __init__(self, orden=4):
        """Crea un arbol B+ vacio."""
        if orden < 3:
            raise ValueError("El orden debe ser mayor o igual a 3.")
        self._orden = orden
        self._max_claves = orden - 1
        self._raiz = NodoBPlus(hoja=True)

    @property
    def orden(self):
        """Retorna el orden del arbol."""
        return self._orden

    @property
    def raiz(self):
        """Retorna la raiz del arbol."""
        return self._raiz

    def esta_vacio(self):
        """Indica si el arbol no tiene claves."""
        return self._raiz.hoja and not self._raiz.claves

    def buscar(self, clave):
        """Busca una clave en las hojas.

        Args:
            clave: Valor que se desea buscar.

        Returns:
            True si la clave existe, False en caso contrario.
        """
        nodo = self._buscar_hoja(clave)
        indice = bisect_left(nodo.claves, clave)
        return (indice < len(nodo.claves)
                and nodo.claves[indice] == clave)

    def _buscar_hoja(self, clave):
        """Desciende hasta la hoja que podria contener la clave."""
        nodo = self._raiz
        while not nodo.hoja:
            indice = bisect_left(nodo.claves, clave)
            nodo = nodo.hijos[indice]
        return nodo

    def insertar(self, clave):
        """Inserta una clave en la hoja correspondiente.

        Args:
            clave: Valor que se desea insertar.

        Returns:
            True si se inserto, False si ya existia.
        """
        if self.buscar(clave):
            return False

        nodo = self._raiz
        ruta = []

        while not nodo.hoja:
            indice = bisect_left(nodo.claves, clave)
            ruta.append((nodo, indice))
            nodo = nodo.hijos[indice]

        nodo.claves.insert(bisect_left(nodo.claves, clave), clave)

        while len(nodo.claves) > self._max_claves:
            clave_separadora, nodo_derecho = self._dividir(nodo)
            if not ruta:
                nueva_raiz = NodoBPlus(hoja=False)
                nueva_raiz.claves = [clave_separadora]
                nueva_raiz.hijos = [nodo, nodo_derecho]
                self._raiz = nueva_raiz
                break

            padre, indice = ruta.pop()
            padre.claves.insert(indice, clave_separadora)
            padre.hijos.insert(indice + 1, nodo_derecho)
            nodo = padre

        return True

    def _dividir(self, nodo):
        """Divide un nodo lleno y retorna el separador y el nodo derecho."""
        medio = len(nodo.claves) // 2

        if nodo.hoja:
            clave_separadora = nodo.claves[medio - 1]
            nodo_derecho = NodoBPlus(hoja=True)
            nodo_derecho.claves = nodo.claves[medio:]
            nodo.claves = nodo.claves[:medio]
            nodo_derecho.siguiente = nodo.siguiente
            nodo.siguiente = nodo_derecho
            return clave_separadora, nodo_derecho

        clave_separadora = nodo.claves[medio]
        nodo_derecho = NodoBPlus(hoja=False)
        nodo_derecho.claves = nodo.claves[medio + 1:]
        nodo_derecho.hijos = nodo.hijos[medio + 1:]
        nodo.claves = nodo.claves[:medio]
        nodo.hijos = nodo.hijos[:medio + 1]
        return clave_separadora, nodo_derecho

    def recorrido(self):
        """Retorna todas las claves en orden ascendente."""
        if self.esta_vacio():
            return []

        resultado = []
        nodo = self._buscar_hoja(self._primera_clave())
        while nodo is not None:
            resultado.extend(nodo.claves)
            nodo = nodo.siguiente
        return resultado

    def _primera_clave(self):
        """Retorna la primera clave del arbol."""
        nodo = self._raiz
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

    def rango(self, inicio, fin):
        """Retorna las claves dentro de [inicio, fin]."""
        if self.esta_vacio() or inicio > fin:
            return []

        resultado = []
        nodo = self._buscar_hoja(inicio)
        while nodo is not None:
            for clave in nodo.claves:
                if inicio <= clave <= fin:
                    resultado.append(clave)
            if nodo.claves and nodo.claves[-1] >= fin:
                break
            nodo = nodo.siguiente
        return resultado

    def altura(self):
        """Retorna la altura del arbol (una hoja tiene altura 0)."""
        if self.esta_vacio():
            return 0
        altura = 0
        nodo = self._raiz
        while not nodo.hoja:
            altura += 1
            nodo = nodo.hijos[0]
        return altura

    def hojas(self):
        """Retorna las hojas enlazadas en orden."""
        if self.esta_vacio():
            return []
        nodo = self._buscar_hoja(self._primera_clave())
        resultado = []
        while nodo is not None:
            resultado.append(nodo.claves)
            nodo = nodo.siguiente
        return resultado

    def __str__(self):
        """Muestra el arbol por niveles."""
        if self.esta_vacio():
            return "ArbolBPlus([])"

        lineas = []
        nivel = [self._raiz]
        numero_nivel = 0
        while nivel:
            claves = [nodo.claves for nodo in nivel]
            lineas.append(f"Nivel {numero_nivel}: {claves}")
            siguiente = []
            for nodo in nivel:
                siguiente.extend(nodo.hijos)
            nivel = siguiente
            numero_nivel += 1
        return "\n".join(lineas)


def main():
    """Ejecuta una demostracion del arbol B+."""
    arbol = ArbolBPlus(orden=4)
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 40, 50, 15]

    print("=== Arbol B+ de orden 4 ===")
    for valor in valores:
        arbol.insertar(valor)

    print(arbol)
    print(f"\nHojas enlazadas: {arbol.hojas()}")
    print(f"Recorrido: {arbol.recorrido()}")
    print(f"Altura: {arbol.altura()}")
    print(f"Buscar 17: {arbol.buscar(17)}")
    print(f"Buscar 99: {arbol.buscar(99)}")
    print(f"Rango [6, 20]: {arbol.rango(6, 20)}")


if __name__ == "__main__":
    main()
