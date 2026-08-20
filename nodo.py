"""
Autor: Charles Jesus Morales Velasco
Titulo: Clase Nodo para el juego tres en raya
Version: 1.0.0
Fecha: 2026
"""


class Nodo:
    """
    Clase que representa un nodo de un árbol binario.

    Cada nodo almacena un elemento (valor de una celda del tablero
    de Tres en Raya: 'X', 'O' o None) y referencias a sus
    hijos izquierdo y derecho.
    """

    def __init__(self, elemento=None):
        """
        Inicializa un nodo con un elemento y sin hijos.

        Args:
            elemento: Valor del nodo. Puede ser 'X', 'O' o None.
                    Por defecto es None (celda vacía).
        """
        self._elemento = elemento
        self._hijo_izquierdo = None
        self._hijo_derecho = None


    # Getters


    def get_elemento(self):
        """
        Retorna el elemento almacenado en el nodo.

        Returns:
            El valor del nodo ('X', 'O' o None).
        """
        return self._elemento

    def get_hijo_izquierdo(self):
        """
        Retorna el hijo izquierdo del nodo.

        Returns:
            Nodo hijo izquierdo o None si no existe.
        """
        return self._hijo_izquierdo

    def get_hijo_derecho(self):
        """
        Retorna el hijo derecho del nodo.

        Returns:
            Nodo hijo derecho o None si no existe.
        """
        return self._hijo_derecho


    # Setters


    def set_elemento(self, elemento):
        """
        Establece el elemento del nodo.

        Args:
            elemento: Nuevo valor del nodo. Debe ser 'X', 'O' o None.

        Raises:
            ValueError: Si el elemento no es un valor válido.
        """
        if elemento not in ('X', 'O', None):
            raise ValueError(
                f"Elemento inválido: '{elemento}'. "
                "Los valores permitidos son 'X', 'O' o None."
            )
        self._elemento = elemento

    def set_hijo_izquierdo(self, nodo):
        """
        Establece el hijo izquierdo del nodo.

        Args:
            nodo: Instancia de Nodo o None.

        Raises:
            TypeError: Si el argumento no es una instancia de Nodo o None.
        """
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError(
                "El hijo izquierdo debe ser una instancia de Nodo o None."
            )
        self._hijo_izquierdo = nodo

    def set_hijo_derecho(self, nodo):
        """
        Establece el hijo derecho del nodo.

        Args:
            nodo: Instancia de Nodo o None.

        Raises:
            TypeError: Si el argumento no es una instancia de Nodo o None.
        """
        if nodo is not None and not isinstance(nodo, Nodo):
            raise TypeError(
                "El hijo derecho debe ser una instancia de Nodo o None."
            )
        self._hijo_derecho = nodo

    # Métodos auxiliares

    def tiene_hijo_izquierdo(self):
        """
        Verifica si el nodo tiene hijo izquierdo.

        Returns:
            True si tiene hijo izquierdo, False en caso contrario.
        """
        return self._hijo_izquierdo is not None

    def tiene_hijo_derecho(self):
        """
        Verifica si el nodo tiene hijo derecho.

        Returns:
            True si tiene hijo derecho, False en caso contrario.
        """
        return self._hijo_derecho is not None

    def es_hoja(self):
        """
        Verifica si el nodo es una hoja (sin hijos).

        Returns:
            True si no tiene hijos, False en caso contrario.
        """
        return not self.tiene_hijo_izquierdo() and not self.tiene_hijo_derecho()

    def __str__(self):
        """
        Retorna una representación legible del nodo.

        Returns:
            Cadena con el valor del elemento o 'Vacío' si es None.
        """
        valor = self._elemento if self._elemento is not None else "Vacío"
        return f"Nodo({valor})"

    def __repr__(self):
        """
        Retorna una representación oficial del nodo.

        Returns:
            Cadena con la representación técnica del nodo.
        """
        return (
            f"Nodo(elemento={self._elemento!r}, "
            f"hijo_izquierdo={self._hijo_izquierdo!r}, "
            f"hijo_derecho={self._hijo_derecho!r})"
        )



# Bloque de prueba rápida


if __name__ == "__main__":
    # Crear nodos individuales
    nodo_raiz = Nodo('X')
    nodo_izq = Nodo('O')
    nodo_der = Nodo('X')

    # Asignar hijos mediante setters
    nodo_raiz.set_hijo_izquierdo(nodo_izq)
    nodo_raiz.set_hijo_derecho(nodo_der)

    # Mostrar información con getters
    print("=== Prueba de la clase Nodo ===")
    print(f"Raíz:           {nodo_raiz}")
    print(f"Elemento raíz:  {nodo_raiz.get_elemento()}")
    print(f"Hijo izquierdo: {nodo_raiz.get_hijo_izquierdo()}")
    print(f"Hijo derecho:   {nodo_raiz.get_hijo_derecho()}")
    print(f"¿Es hoja?:      {nodo_raiz.es_hoja()}")
    print(f"¿Nodo izq es hoja?: {nodo_izq.es_hoja()}")
    print(f"¿Nodo der es hoja?: {nodo_der.es_hoja()}")
    # Probar validación del setter
    print("\n=== Prueba de validación ===")
    try:
        nodo_raiz.set_elemento('Z')
    except ValueError as e:
        print(f"Error: {e}")