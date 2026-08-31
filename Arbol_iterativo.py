"""
Autor: Charles Jesus Morales Velasco
Titulo: Árbol Binario de Búsqueda - Implementación Iterativa
Version: 2.1.0
Fecha: 2026
"""

from collections import deque
from Nodo import Nodo


class ArbolBinarioBusquedaIterativo:
    """
    Árbol Binario de Búsqueda (ABB) con implementación iterativa.

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
        nuevo = Nodo(dato)

        if self.esta_vacio():
            self._raiz = nuevo
            self._tamanio += 1
            return

        actual = self._raiz
        while True:
            if dato < actual.dato:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    self._tamanio += 1
                    break
                actual = actual.izquierdo
            elif dato > actual.dato:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    self._tamanio += 1
                    break
                actual = actual.derecho
            else:
                # Duplicado, ignorar
                break

    def buscar(self, dato) -> bool:
        """
        Busca un valor en el árbol.

        Args:
            dato: Valor a buscar.

        Returns:
            True si el valor existe, False en caso contrario.

        Complejidad: O(h)
        """
        actual = self._raiz
        while actual is not None:
            if dato == actual.dato:
                return True
            if dato < actual.dato:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return False

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
        actual = self._raiz
        while actual is not None:
            if dato == actual.dato:
                return actual.dato
            if dato < actual.dato:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

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
        padre = None
        actual = self._raiz
        es_hijo_izquierdo = False

        # Localizar el nodo y su padre
        while actual is not None and actual.dato != dato:
            padre = actual
            if dato < actual.dato:
                actual = actual.izquierdo
                es_hijo_izquierdo = True
            else:
                actual = actual.derecho
                es_hijo_izquierdo = False

        if actual is None:
            return False

        # Caso 3: dos hijos
        if actual.izquierdo is not None and actual.derecho is not None:
            # Sucesor inorden: mínimo del subárbol derecho
            padre_sucesor = actual
            sucesor = actual.derecho
            while sucesor.izquierdo is not None:
                padre_sucesor = sucesor
                sucesor = sucesor.izquierdo
            actual.dato = sucesor.dato
            # Eliminar el sucesor (tiene como máximo un hijo derecho)
            if padre_sucesor is actual:
                padre_sucesor.derecho = sucesor.derecho
            else:
                padre_sucesor.izquierdo = sucesor.derecho
            self._tamanio -= 1
            return True

        # Caso 1 y 2: determinar el único hijo (o None si es hoja)
        if actual.izquierdo is not None:
            hijo = actual.izquierdo
        elif actual.derecho is not None:
            hijo = actual.derecho
        else:
            hijo = None

        if padre is None:
            self._raiz = hijo
        elif es_hijo_izquierdo:
            padre.izquierdo = hijo
        else:
            padre.derecho = hijo

        self._tamanio -= 1
        return True

    #############################
    ## Operaciones de consulta ##
    #############################

    def altura(self) -> int:
        """
        Calcula la altura del árbol usando una pila explícita.

        La altura de un árbol vacío es -1.
        La altura de un árbol con solo la raíz es 0.

        Returns:
            Entero con la altura del árbol.
        """
        if self.esta_vacio():
            return -1

        altura_maxima = 0
        pila = [(self._raiz, 0)]

        while pila:
            nodo, nivel = pila.pop()
            altura_maxima = max(altura_maxima, nivel)
            if nodo.izquierdo:
                pila.append((nodo.izquierdo, nivel + 1))
            if nodo.derecho:
                pila.append((nodo.derecho, nivel + 1))

        return altura_maxima

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
        actual = self._raiz
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual.dato

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
        actual = self._raiz
        while actual.derecho is not None:
            actual = actual.derecho
        return actual.dato

    def es_balanceado(self) -> bool:
        """
        Verifica si el árbol está balanceado usando una pila explícita.

        Un árbol es balanceado si para cada nodo la diferencia
        de altura entre sus subárboles es a lo sumo 1.

        Returns:
            True si está balanceado, False en caso contrario.
        """
        if self.esta_vacio():
            return True

        pila = [self._raiz]

        while pila:
            nodo = pila.pop()
            alt_izq = self._altura_subarbol(nodo.izquierdo)
            alt_der = self._altura_subarbol(nodo.derecho)
            if abs(alt_izq - alt_der) > 1:
                return False
            if nodo.izquierdo:
                pila.append(nodo.izquierdo)
            if nodo.derecho:
                pila.append(nodo.derecho)

        return True

    def _altura_subarbol(self, nodo) -> int:
        """
        Calcula la altura de un subárbol usando una pila explícita.

        Args:
            nodo (Nodo | None): Raíz del subárbol.

        Returns:
            Entero con la altura del subárbol.
        """
        if nodo is None:
            return -1

        altura_maxima = 0
        pila = [(nodo, 0)]

        while pila:
            actual, nivel = pila.pop()
            altura_maxima = max(altura_maxima, nivel)
            if actual.izquierdo:
                pila.append((actual.izquierdo, nivel + 1))
            if actual.derecho:
                pila.append((actual.derecho, nivel + 1))

        return altura_maxima

    ############################################
    ## Recorridos (con pila / cola explícita) ##
    ############################################

    def inorden(self) -> list:
        """
        Recorre el árbol en orden (izquierdo → raíz → derecho)
        usando una pila explícita.
        Produce los valores ordenados de menor a mayor.

        Returns:
            Lista con los datos en orden inorden.
        """
        resultado = []
        pila = []
        actual = self._raiz

        while actual is not None or pila:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            resultado.append(actual.dato)
            actual = actual.derecho

        return resultado

    def preorden(self) -> list:
        """
        Recorre el árbol en preorden (raíz → izquierdo → derecho)
        usando una pila explícita.

        Returns:
            Lista con los datos en orden preorden.
        """
        if self.esta_vacio():
            return []

        resultado = []
        pila = [self._raiz]

        while pila:
            nodo = pila.pop()
            resultado.append(nodo.dato)
            if nodo.derecho:
                pila.append(nodo.derecho)
            if nodo.izquierdo:
                pila.append(nodo.izquierdo)

        return resultado

    def postorden(self) -> list:
        """
        Recorre el árbol en postorden (izquierdo → derecho → raíz)
        usando dos pilas explícitas.

        Returns:
            Lista con los datos en orden postorden.
        """
        if self.esta_vacio():
            return []

        resultado = []
        pila = [self._raiz]

        while pila:
            nodo = pila.pop()
            resultado.append(nodo.dato)
            if nodo.izquierdo:
                pila.append(nodo.izquierdo)
            if nodo.derecho:
                pila.append(nodo.derecho)

        resultado.reverse()
        return resultado

    def por_niveles(self) -> list:
        """
        Recorrido por niveles / BFS (breadth-first search) usando una cola.

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
        self._imprimir_iter(self._raiz, 0)

    def _imprimir_iter(self, raiz, nivel_inicial) -> None:
        """
        Imprime el árbol de forma visual usando una pila explícita.
        Orden: derecho primero (aparece arriba), luego raíz, luego izquierdo.
        Cada tupla en la pila: (nodo, nivel, listo_para_imprimir).
        """
        pila = [(raiz, nivel_inicial, False)]

        while pila:
            nodo, nivel, listo = pila.pop()
            if nodo is None:
                continue
            if listo:
                print("    " * nivel + f"[{nodo.dato}]")
            else:
                pila.append((nodo.izquierdo, nivel + 1, False))
                pila.append((nodo, nivel, True))
                pila.append((nodo.derecho, nivel + 1, False))

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
    print("=== Prueba ArbolBinarioBusquedaIterativo ===\n")

    arbol = ArbolBinarioBusquedaIterativo()

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