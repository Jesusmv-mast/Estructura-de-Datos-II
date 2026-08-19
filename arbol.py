"""
Módulo que contiene la clase Arbol para la representación
del juego Tres en Raya mediante una matriz 3x3 de Nodos.

Autor: [Tu nombre]
Fecha: 2026
"""

from nodo import Nodo


class Arbol:
    """
    Clase que representa el tablero del juego Tres en Raya
    mediante una matriz 3x3 de nodos organizados en un árbol binario.

    La matriz almacena instancias de Nodo en cada celda,
    donde cada nodo puede contener 'X', 'O' o None (vacío).
    """

    FILAS = 3
    COLUMNAS = 3

    def __init__(self):
        """
        Inicializa el árbol con una matriz 3x3 de nodos vacíos
        y sin raíz definida.
        """
        self._raiz = None
        self._matriz = self._crear_matriz()

    # -------------------------
    # Métodos privados
    # -------------------------

    def _crear_matriz(self):
        """
        Crea una matriz 3x3 inicializada con nodos vacíos.

        Returns:
            Lista de listas con instancias de Nodo (elemento=None).
        """
        matriz = []
        for _ in range(self.FILAS):
            fila = [Nodo() for _ in range(self.COLUMNAS)]
            matriz.append(fila)
        return matriz

    # -------------------------
    # Getters
    # -------------------------

    def get_raiz(self):
        """
        Retorna el nodo raíz del árbol.

        Returns:
            Nodo raíz o None si no está definido.
        """
        return self._raiz

    def get_matriz(self):
        """
        Retorna la matriz 3x3 completa de nodos.

        Returns:
            Lista de listas con instancias de Nodo.
        """
        return self._matriz

    def get_nodo(self, fila, columna):
        """
        Retorna el nodo ubicado en la posición indicada de la matriz.

        Args:
            fila (int): Índice de la fila (0 a 2).
            columna (int): Índice de la columna (0 a 2).

        Returns:
            Instancia de Nodo en la posición dada.

        Raises:
            IndexError: Si la fila o columna están fuera de rango.
        """
        self._validar_posicion(fila, columna)
        return self._matriz[fila][columna]

    def get_valor(self, fila, columna):
        """
        Retorna el elemento del nodo en la posición indicada.

        Args:
            fila (int): Índice de la fila (0 a 2).
            columna (int): Índice de la columna (0 a 2).

        Returns:
            El valor del nodo ('X', 'O' o None).
        """
        return self.get_nodo(fila, columna).get_elemento()

    # -------------------------
    # Setters
    # -------------------------

    def set_raiz(self, nodo):
        """
        Establece el nodo raíz del árbol.

        Args:
            nodo: Instancia de Nodo o None.

        Raises:
            TypeError: Si el argumento no es una instancia de Nodo o None.
        """
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError(
                "La raíz debe ser una instancia de Nodo o None."
            )
        self._raiz = nodo

    def set_valor(self, fila, columna, valor):
        """
        Establece el valor del nodo en la posición indicada.

        Args:
            fila (int): Índice de la fila (0 a 2).
            columna (int): Índice de la columna (0 a 2).
            valor: Valor a asignar ('X', 'O' o None).

        Raises:
            IndexError: Si la fila o columna están fuera de rango.
            ValueError: Si la celda ya está ocupada.
        """
        self._validar_posicion(fila, columna)
        nodo = self._matriz[fila][columna]

        if nodo.get_elemento() is not None:
            raise ValueError(
                f"La celda ({fila}, {columna}) ya está ocupada "
                f"con '{nodo.get_elemento()}'."
            )
        nodo.set_elemento(valor)

    # -------------------------
    # Métodos de validación
    # -------------------------

    def _validar_posicion(self, fila, columna):
        """
        Valida que la fila y columna estén dentro del rango permitido.

        Args:
            fila (int): Índice de la fila.
            columna (int): Índice de la columna.

        Raises:
            IndexError: Si alguno de los índices está fuera de rango.
        """
        if not (0 <= fila < self.FILAS):
            raise IndexError(
                f"Fila {fila} fuera de rango. Debe estar entre 0 y "
                f"{self.FILAS - 1}."
            )
        if not (0 <= columna < self.COLUMNAS):
            raise IndexError(
                f"Columna {columna} fuera de rango. Debe estar entre 0 y "
                f"{self.COLUMNAS - 1}."
            )

    # -------------------------
    # Métodos del juego
    # -------------------------

    def esta_vacia(self, fila, columna):
        """
        Verifica si una celda está vacía.

        Args:
            fila (int): Índice de la fila (0 a 2).
            columna (int): Índice de la columna (0 a 2).

        Returns:
            True si la celda está vacía, False en caso contrario.
        """
        return self.get_valor(fila, columna) is None

    def tablero_lleno(self):
        """
        Verifica si el tablero está completamente lleno.

        Returns:
            True si no hay celdas vacías, False en caso contrario.
        """
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                if self.esta_vacia(fila, columna):
                    return False
        return True

    def reiniciar(self):
        """
        Reinicia el tablero creando una nueva matriz 3x3 de nodos vacíos.
        """
        self._matriz = self._crear_matriz()
        self._raiz = None

    def mostrar_tablero(self):
        """
        Imprime el tablero en consola de forma visual.
        """
        print("\n  0   1   2")
        for i, fila in enumerate(self._matriz):
            valores = []
            for nodo in fila:
                elemento = nodo.get_elemento()
                valores.append(elemento if elemento is not None else ".")
            print(f"{i} {' | '.join(valores)}")
            if i < self.FILAS - 1:
                print("  ---------")
        print()

    def __str__(self):
        """
        Retorna una representación en cadena del tablero.

        Returns:
            Cadena con el estado actual del tablero.
        """
        filas = []
        for fila in self._matriz:
            valores = []
            for nodo in fila:
                elemento = nodo.get_elemento()
                valores.append(elemento if elemento is not None else ".")
            filas.append(" | ".join(valores))
        return "\n".join(filas)


# -------------------------
# Bloque de prueba rápida
# -------------------------

if __name__ == "__main__":
    print("=== Prueba de la clase Arbol ===")

    arbol = Arbol()

    # Mostrar tablero vacío
    print("Tablero inicial:")
    arbol.mostrar_tablero()

    # Asignar valores con setter
    arbol.set_valor(0, 0, 'X')
    arbol.set_valor(1, 1, 'O')
    arbol.set_valor(2, 2, 'X')
    arbol.set_valor(0, 2, 'O')

    print("Tablero tras jugadas:")
    arbol.mostrar_tablero()

    # Usar getter de valor
    print(f"Valor en (0,0): {arbol.get_valor(0, 0)}")
    print(f"Valor en (1,1): {arbol.get_valor(1, 1)}")
    print(f"¿Celda (0,1) vacía?: {arbol.esta_vacia(0, 1)}")
    print(f"¿Tablero lleno?: {arbol.tablero_lleno()}")

    # Probar raíz
    nodo_raiz = Nodo('X')
    arbol.set_raiz(nodo_raiz)
    print(f"\nRaíz del árbol: {arbol.get_raiz()}")

    # Probar validación de celda ocupada
    print("\n=== Prueba de validación ===")
    try:
        arbol.set_valor(0, 0, 'O')
    except ValueError as e:
        print(f"Error esperado: {e}")

    # Reiniciar tablero
    arbol.reiniciar()
    print("\nTablero tras reiniciar:")
    arbol.mostrar_tablero()