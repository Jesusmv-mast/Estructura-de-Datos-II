"""
Autor: Charles Jesus Morales Velasco
Titulo: Clase NodoAVL
Fecha: 2026
"""


class NodoAVL:

    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None
        self.altura = 0  # nodo hoja empieza en altura 0

    def __repr__(self):
        return f"NodoAVL({self.dato})"

    def __str__(self):
        return str(self.dato)