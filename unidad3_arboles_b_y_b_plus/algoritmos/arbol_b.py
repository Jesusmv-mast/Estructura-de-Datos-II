"""Arbol B con busqueda, insercion y eliminacion.

Autor: Charles Jesus Morales Velasco
Titulo: Arbol B balanceado
Version: 1.0.0
Fecha: 2026

Implementacion basada en el grado minimo t:
    - Cada nodo guarda como maximo 2t - 1 claves.
    - Todo nodo distinto de la raiz guarda al menos t - 1 claves.
    - Un nodo con k claves tiene k + 1 hijos si no es hoja.
"""

from bisect import bisect_left


class NodoB:
    """Nodo de un arbol B."""

    def __init__(self, hoja=True):
        """Inicializa un nodo indicando si es hoja."""
        self.hoja = hoja
        self.claves = []
        self.hijos = []

    def __repr__(self):
        """Representacion tecnica del nodo."""
        return f"NodoB(hoja={self.hoja}, claves={self.claves!r})"


class ArbolB:
    """Arbol B balanceado.

    Args:
        grado_minimo: Grado minimo t. Debe ser al menos 2.
    """

    def __init__(self, grado_minimo=2):
        """Crea un arbol B vacio."""
        if grado_minimo < 2:
            raise ValueError("El grado minimo debe ser mayor o igual a 2.")
        self._t = grado_minimo
        self._raiz = NodoB(hoja=True)

    @property
    def grado_minimo(self):
        """Retorna el grado minimo del arbol."""
        return self._t

    @property
    def raiz(self):
        """Retorna la raiz del arbol."""
        return self._raiz

    @property
    def max_claves(self):
        """Cantidad maxima de claves por nodo."""
        return 2 * self._t - 1

    @property
    def min_claves(self):
        """Cantidad minima de claves por nodo (excepto la raiz)."""
        return self._t - 1

    def esta_vacio(self):
        """Indica si el arbol no tiene claves."""
        return len(self._raiz.claves) == 0

    def buscar(self, clave):
        """Busca una clave en el arbol.

        Args:
            clave: Valor que se desea buscar.

        Returns:
            True si la clave existe, False en caso contrario.
        """
        return self._buscar(self._raiz, clave)

    def _buscar(self, nodo, clave):
        """Busqueda recursiva dentro de un subarbol."""
        indice = bisect_left(nodo.claves, clave)
        if indice < len(nodo.claves) and nodo.claves[indice] == clave:
            return True
        if nodo.hoja:
            return False
        return self._buscar(nodo.hijos[indice], clave)

    def insertar(self, clave):
        """Inserta una clave y mantiene el balance del arbol.

        Args:
            clave: Valor que se desea insertar.

        Returns:
            True si se inserto, False si ya existia.
        """
        if self.buscar(clave):
            return False

        raiz = self._raiz
        if len(raiz.claves) == self.max_claves:
            nueva_raiz = NodoB(hoja=False)
            nueva_raiz.hijos.append(raiz)
            self._dividir_hijo(nueva_raiz, 0)
            self._raiz = nueva_raiz
            raiz = nueva_raiz

        self._insertar_no_lleno(raiz, clave)
        return True

    def _insertar_no_lleno(self, nodo, clave):
        """Inserta en un nodo que no esta lleno."""
        if nodo.hoja:
            nodo.claves.insert(bisect_left(nodo.claves, clave), clave)
            return

        indice = bisect_left(nodo.claves, clave)
        hijo = nodo.hijos[indice]

        if len(hijo.claves) == self.max_claves:
            self._dividir_hijo(nodo, indice)
            if clave > nodo.claves[indice]:
                indice += 1

        self._insertar_no_lleno(nodo.hijos[indice], clave)

    def _dividir_hijo(self, padre, indice):
        """Divide el hijo lleno en dos y sube la clave media."""
        hijo = padre.hijos[indice]
        nuevo_hijo = NodoB(hoja=hijo.hoja)
        clave_media = hijo.claves[self._t - 1]

        nuevo_hijo.claves = hijo.claves[self._t:]
        hijo.claves = hijo.claves[:self._t - 1]

        if not hijo.hoja:
            nuevo_hijo.hijos = hijo.hijos[self._t:]
            hijo.hijos = hijo.hijos[:self._t]

        padre.claves.insert(indice, clave_media)
        padre.hijos.insert(indice + 1, nuevo_hijo)

    def eliminar(self, clave):
        """Elimina una clave del arbol.

        Args:
            clave: Valor que se desea eliminar.

        Returns:
            True si se elimino, False si no existia.
        """
        if not self.buscar(clave):
            return False

        self._eliminar(self._raiz, clave)

        if not self._raiz.hoja and len(self._raiz.claves) == 0:
            self._raiz = self._raiz.hijos[0]

        return True

    def _eliminar(self, nodo, clave):
        """Elimina una clave dentro del subarbol indicado."""
        indice = bisect_left(nodo.claves, clave)

        if (indice < len(nodo.claves)
                and nodo.claves[indice] == clave):
            if nodo.hoja:
                nodo.claves.pop(indice)
            else:
                self._eliminar_de_interno(nodo, indice)
            return

        if nodo.hoja:
            return

        ultimo_hijo = indice == len(nodo.claves)

        if len(nodo.hijos[indice].claves) < self._t:
            self._llenar(nodo, indice)

        if ultimo_hijo and indice > len(nodo.claves):
            self._eliminar(nodo.hijos[indice - 1], clave)
        else:
            self._eliminar(nodo.hijos[indice], clave)

    def _eliminar_de_interno(self, nodo, indice):
        """Elimina una clave que esta en un nodo interno."""
        clave = nodo.claves[indice]
        hijo_izquierdo = nodo.hijos[indice]
        hijo_derecho = nodo.hijos[indice + 1]

        if len(hijo_izquierdo.claves) >= self._t:
            predecesor = self._maximo(hijo_izquierdo)
            nodo.claves[indice] = predecesor
            self._eliminar(hijo_izquierdo, predecesor)
        elif len(hijo_derecho.claves) >= self._t:
            sucesor = self._minimo(hijo_derecho)
            nodo.claves[indice] = sucesor
            self._eliminar(hijo_derecho, sucesor)
        else:
            self._fusionar(nodo, indice)
            self._eliminar(hijo_izquierdo, clave)

    def _llenar(self, nodo, indice):
        """Garantiza que el hijo tenga al menos t claves."""
        if indice > 0 and len(nodo.hijos[indice - 1].claves) >= self._t:
            self._prestar_de_anterior(nodo, indice)
        elif (indice < len(nodo.hijos) - 1
              and len(nodo.hijos[indice + 1].claves) >= self._t):
            self._prestar_de_siguiente(nodo, indice)
        else:
            if indice < len(nodo.hijos) - 1:
                self._fusionar(nodo, indice)
            else:
                self._fusionar(nodo, indice - 1)

    def _prestar_de_anterior(self, nodo, indice):
        """Toma una clave del hermano izquierdo."""
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice - 1]

        hijo.claves.insert(0, nodo.claves[indice - 1])
        if not hijo.hoja:
            hijo.hijos.insert(0, hermano.hijos.pop())

        nodo.claves[indice - 1] = hermano.claves.pop()

    def _prestar_de_siguiente(self, nodo, indice):
        """Toma una clave del hermano derecho."""
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice + 1]

        hijo.claves.append(nodo.claves[indice])
        if not hijo.hoja:
            hijo.hijos.append(hermano.hijos.pop(0))

        nodo.claves[indice] = hermano.claves.pop(0)

    def _fusionar(self, nodo, indice):
        """Fusiona un hijo con su hermano derecho."""
        hijo = nodo.hijos[indice]
        hermano = nodo.hijos[indice + 1]

        hijo.claves.append(nodo.claves.pop(indice))
        hijo.claves.extend(hermano.claves)

        if not hijo.hoja:
            hijo.hijos.extend(hermano.hijos)

        nodo.hijos.pop(indice + 1)

    def _minimo(self, nodo):
        """Retorna la clave minima de un subarbol."""
        while not nodo.hoja:
            nodo = nodo.hijos[0]
        return nodo.claves[0]

    def _maximo(self, nodo):
        """Retorna la clave maxima de un subarbol."""
        while not nodo.hoja:
            nodo = nodo.hijos[-1]
        return nodo.claves[-1]

    def recorrido(self):
        """Retorna las claves en orden ascendente."""
        resultado = []
        self._recorrer(self._raiz, resultado)
        return resultado

    def _recorrer(self, nodo, resultado):
        """Recorrido inorden del subarbol."""
        for indice, clave in enumerate(nodo.claves):
            if not nodo.hoja:
                self._recorrer(nodo.hijos[indice], resultado)
            resultado.append(clave)
        if not nodo.hoja:
            self._recorrer(nodo.hijos[-1], resultado)

    def altura(self):
        """Retorna la altura del arbol."""
        if self.esta_vacio():
            return 0
        altura = 0
        nodo = self._raiz
        while not nodo.hoja:
            altura += 1
            nodo = nodo.hijos[0]
        return altura

    def __str__(self):
        """Muestra el arbol por niveles."""
        if self.esta_vacio():
            return "ArbolB([])"

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
    """Ejecuta una demostracion del arbol B."""
    arbol = ArbolB(grado_minimo=2)
    valores = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 40, 50, 15]

    print("=== Arbol B con grado minimo 2 ===")
    for valor in valores:
        arbol.insertar(valor)

    print(arbol)
    print(f"\nRecorrido: {arbol.recorrido()}")
    print(f"Altura: {arbol.altura()}")
    print(f"Buscar 17: {arbol.buscar(17)}")
    print(f"Buscar 99: {arbol.buscar(99)}")

    print("\nEliminando 6, 15 y 30:")
    for valor in (6, 15, 30):
        print(f"  Eliminar {valor}: {arbol.eliminar(valor)}")

    print(arbol)
    print(f"Recorrido final: {arbol.recorrido()}")


if __name__ == "__main__":
    main()
