"""
Autor: Charles Jesus Morales Velasco
Titulo: Arbol AVL
Fecha: 2026
"""

from nodoavl import NodoAVL


class ArbolAVL:

    def __init__(self):
        self._raiz = None

    
    # -------- Altura y factor de balance -------------
    

    def _altura(self, nodo):
        # nodo None cuenta como -1
        if nodo is None:
            return -1
        return nodo.altura

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierdo),
                            self._altura(nodo.derecho))

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izquierdo) - self._altura(nodo.derecho)

    # ─────────────────────────────
    #  Rotaciones
    # ─────────────────────────────

    def _rotar_derecha(self, y):
        #        y                x
        #       / \             /   \
        #      x   T3   →     T1    y
        #     / \                  / \
        #   T1   T2              T2   T3

        x = y.izquierdo
        T2 = x.derecho

        x.derecho = y
        y.izquierdo = T2

        self._actualizar_altura(y)
        self._actualizar_altura(x)

        return x  # nueva raiz del subarbol

    def _rotar_izquierda(self, x):
        #      x                  y
        #     / \               /   \
        #   T1   y     →       x    T3
        #       / \           / \
        #     T2   T3       T1   T2

        y = x.derecho
        T2 = y.izquierdo

        y.izquierdo = x
        x.derecho = T2

        self._actualizar_altura(x)
        self._actualizar_altura(y)

        return y  # nueva raiz del subarbol

    def _balancear(self, nodo):
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Caso 1 izquierda-izquierda
        if fb == 2 and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)

        # Caso 2 izquierda-derecha
        if fb == 2 and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        # Caso 3 derecha-derecha
        if fb == -2 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)

        # Caso 4 derecha-izquierda
        if fb == -2 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        return nodo  # ya estaba balanceado

    # ─────────────────────────────
    #  Insertar
    # ─────────────────────────────

    def insertar(self, dato):
        self._raiz = self._insertar_rec(self._raiz, dato)

    def _insertar_rec(self, nodo, dato):
        # caso base: lugar vacio encontrado
        if nodo is None:
            return NodoAVL(dato)

        if dato < nodo.dato:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._insertar_rec(nodo.derecho, dato)
        else:
            # dato duplicado, no se inserta
            return nodo

        return self._balancear(nodo)

    # ─────────────────────────────
    #  Buscar
    # ─────────────────────────────

    def buscar(self, dato):
        return self._buscar_rec(self._raiz, dato)

    def _buscar_rec(self, nodo, dato):
        if nodo is None:
            return False
        if dato == nodo.dato:
            return True
        if dato < nodo.dato:
            return self._buscar_rec(nodo.izquierdo, dato)
        return self._buscar_rec(nodo.derecho, dato)

    # ─────────────────────────────
    #  Sucesor inorden
    # ─────────────────────────────

    def _sucesor(self, nodo):
        # baja todo lo posible a la izquierda
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # ─────────────────────────────
    #  Eliminar
    # ─────────────────────────────

    def eliminar(self, dato):
        self._raiz = self._eliminar_rec(self._raiz, dato)

    def _eliminar_rec(self, nodo, dato):
        if nodo is None:
            return None

        if dato < nodo.dato:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            nodo.derecho = self._eliminar_rec(nodo.derecho, dato)
        else:
            # nodo encontrado, hay que eliminarlo

            # caso 1: hoja o un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo

            # caso 2: dos hijos → buscar sucesor
            sucesor = self._sucesor(nodo.derecho)
            nodo.dato = sucesor.dato
            # eliminar el sucesor de su posicion original
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.dato)

        return self._balancear(nodo)

    # ─────────────────────────────
    #  Recorridos
    # ─────────────────────────────

    def inorden(self):
        resultado = []
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self):
        resultado = []
        self._preorden_rec(self._raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.dato)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    # ─────────────────────────────
    #  Imprimir en consola
    # ─────────────────────────────

    def imprimir(self):
        if self._raiz is None:
            print("  (arbol vacio)")
            return
        self._imprimir_rec(self._raiz, "", True)

    def _imprimir_rec(self, nodo, prefijo, es_derecho):
        if nodo is None:
            return
        conector = "└── " if es_derecho else "├── "
        print(prefijo + conector + str(nodo.dato) +
            f"  (h={nodo.altura}, fb={self._factor_balance(nodo)})")
        nuevo_prefijo = prefijo + ("    " if es_derecho else "│   ")
        self._imprimir_rec(nodo.derecho, nuevo_prefijo, True)
        self._imprimir_rec(nodo.izquierdo, nuevo_prefijo, False)