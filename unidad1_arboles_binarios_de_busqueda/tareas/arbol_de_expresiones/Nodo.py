"""
Autor: Charles Jesus Morales Velasco
Titulo: Clase Nodo - Representación de un nodo en un árbol binario
Version: 2.0.0
Fecha: 2026
"""


class Nodo:
    """
    Clase que representa un nodo de un árbol binario.

    Cada nodo almacena un dato comparable (entero, float, string, etc.)
    y referencias a sus hijos izquierdo y derecho.
    """

    def __init__(self, dato):
        """
        Inicializa un nodo con un dato y sin hijos.

        Args:
            dato: Valor del nodo. Puede ser número u operador.
        """
        self.dato = dato
        self.izquierdo = None
        self.derecho = None

    def es_hoja(self):
        """
        Verifica si el nodo es una hoja (sin hijos).

        Returns:
            True si no tiene hijos, False en caso contrario.
        """
        return self.izquierdo is None and self.derecho is None

    def __repr__(self):
        """
        Retorna una representación oficial del nodo.

        Returns:
            Cadena con la representación técnica del nodo.
        """
        return f"Nodo({self.dato})"

    def __str__(self):
        """
        Retorna una representación legible del nodo.

        Returns:
            Cadena con el valor del dato.
        """
        return str(self.dato)