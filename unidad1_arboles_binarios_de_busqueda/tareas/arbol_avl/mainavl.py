"""
Autor: Charles Jesus Morales Velasco
Titulo: Prueba del Arbol AVL
Fecha: 2026
"""

import sys

from arbolavl import ArbolAVL

sys.stdout.reconfigure(encoding="utf-8")

avl = ArbolAVL()

# Insertar numeros
for n in [10, 5, 15, 3, 7, 12, 20]:
    avl.insertar(n)

print("=== Arbol AVL ===")
avl.imprimir()

print("\nInorden:", avl.inorden())
print("Preorden:", avl.preorden())

print("\n=== Buscar ===")
print("Buscar 7:", avl.buscar(7))
print("Buscar 99:", avl.buscar(99))

print("\n=== Eliminar 15 (tiene dos hijos) ===")
avl.eliminar(15)
avl.imprimir()

print("\n=== Eliminar 3 (es hoja) ===")
avl.eliminar(3)
avl.imprimir()

print("\nInorden final:", avl.inorden())