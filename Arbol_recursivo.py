"""
Autor: Charles Jesus Morales Velasco
Titulo: Árbol Binario de Búsqueda - Implementación Recursiva
Version: 2.1.0
Fecha: 2026
"""

from collections import deque
from Nodo import Nodo   


class ArbolBinarioBusquedaRecursivo:
    """
    Árbol Binario de Búsqueda (ABB) con implementación recursiva.

    Propiedad ABB: para cada nodo N,
        - subárbol izquierdo < N.dato
        - subárbol derecho   > N.dato

    Operaciones básicas : insertar, eliminar, buscar, buscar_dato,
                        esta_vacio, raiz.
    Operaciones consulta: altura, contar_nodos, minimo, maximo,
                        es_balanceado.
    Recorridos          : inorden, preorden, postorden, por_niveles.
    Visualización       : imprimir.
    """

    def __init__(self):
        """Inicializa el árbol vacío."""
        self._raiz = None
        self._tamanio = 0

    ##########################
    ## Getters and Setters  ##
    ##########################

    @property
    def raiz_nodo(self):
        """Retorna el nodo raíz interno del árbol."""
        return self._raiz

    @raiz_nodo.setter
    def raiz_nodo(self, nodo):
        """
        Asigna el nodo raíz del árbol.

        Args:
            nodo (Nodo | None): Nodo a establecer como raíz.

        Raises:
            TypeError: Si el valor no es un Nodo ni None.
        """
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError("La raíz debe ser un Nodo o None.")
        self._raiz = nodo

    @property
    def tamanio(self):
        """Retorna el número total de nodos del árbol."""
        return self._tamanio

    @tamanio.setter
    def tamanio(self, valor):
        """
        Asigna el tamaño del árbol.

        Args:
            valor (int): Nuevo tamaño del árbol.

        Raises:
            TypeError: Si el valor no es entero.
            ValueError: Si el valor es negativo.
        """
        if not isinstance(valor, int):
            raise TypeError("El tamaño debe ser un entero.")
        if valor < 0:
            raise ValueError("El tamaño no puede ser negativo.")
        self._tamanio = valor

    #########################
    ## Operaciones básicas ##
    #########################

    def esta_vacio(self) -> bool:
        """
        Verifica si el árbol no tiene nodos.

        Returns:
            True si el árbol está vacío, False en caso contrario.
        """
        return self._raiz is None

    def __len__(self) -> int:
        """Retorna el número total de nodos."""
        return self._tamanio

    def raiz(self):
        """
        Retorna el dato almacenado en la raíz.

        Returns:
            Dato de la raíz o None si el árbol está vacío.
        """
        if self.esta_vacio():
            return None
        return self._raiz.dato

    def insertar(self, dato) -> None:
        """
        Agrega un nuevo nodo manteniendo la propiedad ABB.
        Los valores duplicados son ignorados.

        Args:
            dato: Valor comparable a insertar.

        Complejidad: O(h) donde h = altura del árbol.
        """
        self._raiz = self._insertar_rec(self._raiz, dato)

    def _insertar_rec(self, nodo, dato):
        """
        Auxiliar recursivo para insertar un dato en el subárbol dado.

        Args:
            nodo (Nodo | None): Raíz del subárbol actual.
            dato: Valor a insertar.

        Returns:
            Nodo raíz del subárbol (modificado si fue necesario).
        """
        if nodo is None:
            self._tamanio += 1
            return Nodo(dato)

        if dato < nodo.dato:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._insertar_rec(nodo.derecho, dato)
        # dato == nodo.dato → duplicado, ignorar

        return nodo

    def buscar(self, dato) -> bool:
        """
        Busca un valor en el árbol.

        Args:
            dato: Valor a buscar.

        Returns:
            True si el valor existe, False en caso contrario.

        Complejidad: O(h)
        """
        return self._buscar_rec(self._raiz, dato)

    def _buscar_rec(self, nodo, dato) -> bool:
        """
        Auxiliar recursivo para buscar un dato en el subárbol dado.

        Args:
            nodo (Nodo | None): Raíz del subárbol actual.
            dato: Valor a buscar.

        Returns:
            True si se encuentra, False en caso contrario.
        """
        if nodo is None:
            return False
        if dato == nodo.dato:
            return True
        if dato < nodo.dato:
            return self._buscar_rec(nodo.izquierdo, dato)
        return self._buscar_rec(nodo.derecho, dato)

    def buscar_dato(self, dato):
        """
        Busca un valor en el árbol y lo retorna si existe.

        A diferencia de buscar(), este método retorna el dato encontrado
        en lugar de un booleano, lo que permite usarlo directamente.

        Args:
            dato: Valor a buscar.

        Returns:
            El dato encontrado si existe, None si no existe.

        Complejidad: O(h)
        """
        return self._buscar_dato_rec(self._raiz, dato)

    def _buscar_dato_rec(self, nodo, dato):
        """
        Auxiliar recursivo para buscar y retornar el dato en el subárbol dado.

        Args:
            nodo (Nodo | None): Raíz del subárbol actual.
            dato: Valor a buscar.

        Returns:
            El dato encontrado si existe, None en caso contrario.
        """
        if nodo is None:
            return None
        if dato == nodo.dato:
            return nodo.dato
        if dato < nodo.dato:
            return self._buscar_dato_rec(nodo.izquierdo, dato)
        return self._buscar_dato_rec(nodo.derecho, dato)

    def eliminar(self, dato) -> bool:
        """
        Elimina un nodo del árbol considerando los tres casos posibles:
            1. Nodo hoja (sin hijos).
            2. Nodo con un solo hijo.
            3. Nodo con dos hijos (se reemplaza con el sucesor inorden).

        Args:
            dato: Valor a eliminar.

        Returns:
            True si eliminó, False si el dato no existía.

        Complejidad: O(h)
        """
        if not self.buscar(dato):
            return False
        self._raiz = self._eliminar_rec(self._raiz, dato)
        self._tamanio -= 1
        return True

    def _eliminar_rec(self, nodo, dato):
        """
        Auxiliar recursivo para eliminar un dato del subárbol dado.

        Args:
            nodo (Nodo | None): Raíz del subárbol actual.
            dato: Valor a eliminar.

        Returns:
            Nodo raíz del subárbol (modificado).
        """
        if nodo is None:
            return None

        if dato < nodo.dato:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._eliminar_rec(nodo.derecho, dato)
        else:
            # Caso 1: nodo hoja
            if nodo.es_hoja():
                return None
            # Caso 2a: solo hijo derecho
            if nodo.izquierdo is None:
                return nodo.derecho
            # Caso 2b: solo hijo izquierdo
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos → sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo_nodo(nodo.derecho)
            nodo.dato = sucesor.dato
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.dato)

        return nodo

    #############################
    ## Operaciones de consulta ##
    #############################

    def altura(self) -> int:
        """
        Calcula la altura del árbol.

        La altura de un árbol vacío es -1.
        La altura de un árbol con solo la raíz es 0.

        Returns:
            Entero con la altura del árbol.
        """
        return self._altura_rec(self._raiz)

    def _altura_rec(self, nodo) -> int:
        """
        Auxiliar recursivo para calcular la altura del subárbol dado.

        Args:
            nodo (Nodo | None): Raíz del subárbol actual.

        Returns:
            Entero con la altura del subárbol.
        """
        if nodo is None:
            return -1
        return 1 + max(
            self._altura_rec(nodo.izquierdo),
            self._altura_rec(nodo.derecho)
        )

    def contar_nodos(self) -> int:
        """
        Cuenta el total de nodos en el árbol.

        Returns:
            Entero con el número de nodos.
        """
        return self._tamanio

    def minimo(self):
        """
        Retorna el valor mínimo del árbol (nodo más a la izquierda).

        Returns:
            Dato mínimo del árbol.

        Raises:
            ValueError: Si el árbol está vacío.
        """
        if self.esta_vacio():
            raise ValueError("El árbol está vacío.")
        return self._minimo_nodo(self._raiz).dato

    def _minimo_nodo(self, nodo):
        """
        Auxiliar recursivo que retorna el nodo con el valor mínimo
        del subárbol dado.

        Args:
            nodo (Nodo): Raíz del subárbol actual.

        Returns:
            Nodo con el valor mínimo.
        """
        if nodo.izquierdo is None:
            return nodo
        return self._minimo_nodo(nodo.izquierdo)

    def maximo(self):
        """
        Retorna el valor máximo del árbol (nodo más a la derecha).

        Returns:
            Dato máximo del árbol.

        Raises:
            ValueError: Si el árbol está vacío.
        """
        if self.esta_vacio():
            raise ValueError("El árbol está vacío.")
        return self._maximo_nodo(self._raiz).dato

    def _maximo_nodo(self, nodo):
        """
        Auxiliar recursivo que retorna el nodo con el valor máximo
        del subárbol dado.

        Args:
            nodo (Nodo): Raíz del subárbol actual.

        Returns:
            Nodo con el valor máximo.
        """
        if nodo.derecho is None:
            return nodo
        return self._maximo_nodo(nodo.derecho)

    def es_balanceado(self) -> bool:
        """
        Verifica si el árbol está balanceado.

        Un árbol es balanceado si para cada nodo la diferencia
        de altura entre sus subárboles es a lo sumo 1.

        Returns:
            True si está balanceado, False en caso contrario.
        """
        return self._es_balanceado_rec(self._raiz) != -2

    def _es_balanceado_rec(self, nodo) -> int:
        """
        Auxiliar recursivo para verificar balance.

        Returns:
            Altura del subárbol o -2 si está desbalanceado.
        """
        if nodo is None:
            return -1
        alt_izq = self._es_balanceado_rec(nodo.izquierdo)
        if alt_izq == -2:
            return -2
        alt_der = self._es_balanceado_rec(nodo.derecho)
        if alt_der == -2:
            return -2
        if abs(alt_izq - alt_der) > 1:
            return -2
        return 1 + max(alt_izq, alt_der)

    ################
    ## Recorridos ##
    ################

    def inorden(self) -> list:
        """
        Recorre el árbol en orden (izquierdo → raíz → derecho).
        Produce los valores ordenados de menor a mayor.

        Returns:
            Lista con los datos en orden inorden.
        """
        resultado = []
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado) -> None:
        """Auxiliar recursivo para el recorrido inorden."""
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self) -> list:
        """
        Recorre el árbol en preorden (raíz → izquierdo → derecho).

        Returns:
            Lista con los datos en orden preorden.
        """
        resultado = []
        self._preorden_rec(self._raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado) -> None:
        """Auxiliar recursivo para el recorrido preorden."""
        if nodo:
            resultado.append(nodo.dato)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    def postorden(self) -> list:
        """
        Recorre el árbol en postorden (izquierdo → derecho → raíz).

        Returns:
            Lista con los datos en orden postorden.
        """
        resultado = []
        self._postorden_rec(self._raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado) -> None:
        """Auxiliar recursivo para el recorrido postorden."""
        if nodo:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    def por_niveles(self) -> list:
        """
        Recorrido por niveles / BFS (breadth-first search).

        Returns:
            Lista con los datos nivel por nivel de izquierda a derecha.
        """
        if self.esta_vacio():
            return []

        resultado = []
        cola = deque([self._raiz])

        while cola:
            nodo = cola.popleft()
            resultado.append(nodo.dato)
            if nodo.izquierdo:
                cola.append(nodo.izquierdo)
            if nodo.derecho:
                cola.append(nodo.derecho)

        return resultado

    ###################
    ## Visualización ##
    ###################

    def imprimir(self) -> None:
        """Imprime el árbol en formato visual rotado 90° (derecha arriba)."""
        if self.esta_vacio():
            print("Árbol vacío")
            return
        self._imprimir_rec(self._raiz, 0)

    def _imprimir_rec(self, nodo, nivel) -> None:
        """Auxiliar recursivo para imprimir el árbol."""
        if nodo:
            self._imprimir_rec(nodo.derecho, nivel + 1)
            print("    " * nivel + f"[{nodo.dato}]")
            self._imprimir_rec(nodo.izquierdo, nivel + 1)

    ####################
    ## Representación ##
    ####################

    def __str__(self) -> str:
        """Retorna el árbol como cadena en recorrido inorden."""
        datos = self.inorden()
        return " -> ".join(str(d) for d in datos) if datos else "Árbol vacío"


###################
## Prueba rápida ##
###################

if __name__ == "__main__":
    print("=== Prueba ArbolBinarioBusquedaRecursivo ===\n")

    arbol = ArbolBinarioBusquedaRecursivo()

    valores = [50, 30, 70, 20, 40, 60, 80]
    for v in valores:
        arbol.insertar(v)

    arbol.imprimir()
    print(f"\nInorden    : {arbol.inorden()}")
    print(f"Preorden   : {arbol.preorden()}")
    print(f"Postorden  : {arbol.postorden()}")
    print(f"Por niveles: {arbol.por_niveles()}")
    print(f"Raíz       : {arbol.raiz()}")
    print(f"Mínimo     : {arbol.minimo()}")
    print(f"Máximo     : {arbol.maximo()}")
    print(f"Altura     : {arbol.altura()}")
    print(f"Nodos      : {len(arbol)}")
    print(f"Tamaño (getter): {arbol.tamanio}")
    print(f"Balanceado : {arbol.es_balanceado()}")

    # buscar() → True/False
    print(f"\n¿Existe 40? (buscar)     : {arbol.buscar(40)}")
    print(f"¿Existe 99? (buscar)     : {arbol.buscar(99)}")

    # buscar_dato() → el dato o None
    print(f"¿Existe 40? (buscar_dato): {arbol.buscar_dato(40)}")
    print(f"¿Existe 99? (buscar_dato): {arbol.buscar_dato(99)}")

    print(f"\nEliminando 20 (hoja)      → {arbol.eliminar(20)} | {arbol.inorden()}")
    print(f"Eliminando 30 (un hijo)   → {arbol.eliminar(30)} | {arbol.inorden()}")
    print(f"Eliminando 50 (dos hijos) → {arbol.eliminar(50)} | {arbol.inorden()}")
    print(f"Eliminando 99 (no existe) → {arbol.eliminar(99)}")