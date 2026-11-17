"""
Autor: Charles Jesus Morales Velasco
Titulo: Árbol de Expresión - Construcción desde infija y conversión a posfija
Version: 1.0.0
Fecha: 2026
"""

from Nodo import Nodo


#############################
# Precedencia de operadores #
#############################

PRECEDENCIA = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
}

OPERADORES = set(PRECEDENCIA.keys())
PARENTESIS_APERTURA = "("
PARENTESIS_CIERRE = ")"


class ArbolExpresion:
    """
    Árbol binario de expresión matemática.

    Construido a partir de una lista de tokens en notación infija
    usando el algoritmo Shunting Yard de Dijkstra.

    Estructura:
        - Nodos internos : operadores  (+, -, *, /, ^)
        - Nodos hoja     : operandos   (números)

    El recorrido postorden del árbol produce la notación posfija
    (Notación Polaca Inversa).

    Attributes:
        _raiz        (Nodo | None): Nodo raíz del árbol.
        _expresion_infija  (str) : Expresión original en infija.
        _tokens            (list): Lista de tokens de la expresión.
    """

    def __init__(self):
        """Inicializa el árbol de expresión vacío."""
        self._raiz = None
        self._expresion_infija = ""
        self._tokens = []

    #####################
    # Getters / Setters #
    #####################

    @property
    def raiz(self) -> Nodo:
        """Retorna el nodo raíz del árbol."""
        return self._raiz

    @property
    def expresion_infija(self) -> str:
        """Retorna la expresión infija original."""
        return self._expresion_infija

    @property
    def tokens(self) -> list:
        """Retorna la lista de tokens."""
        return list(self._tokens)

    def esta_vacio(self) -> bool:
        """
        Verifica si el árbol no tiene nodos.

        Returns:
            True si el árbol está vacío, False en caso contrario.
        """
        return self._raiz is None

    ##########################
    # Construcción del árbol #
    ##########################

    def construir(self, tokens: list, expresion_original: str) -> None:
        """
        Construye el árbol de expresión a partir de los tokens validados.

        Utiliza el algoritmo Shunting Yard de Dijkstra para respetar
        la precedencia y asociatividad de los operadores:
            - Paréntesis : mayor prioridad
            - ^ (potencia): prioridad 3, asociatividad derecha
            - * /         : prioridad 2
            - + -         : prioridad 1

        Args:
            tokens           (list): Tokens en notación infija (ya validados).
            expresion_original (str): Expresión original para referencia.
        """
        self._expresion_infija = expresion_original
        self._tokens = tokens
        self._raiz = self._shunting_yard(tokens)

    def _shunting_yard(self, tokens: list) -> Nodo:
        """
        Implementa el algoritmo Shunting Yard adaptado para construir
        un árbol binario de expresión (en lugar de producir posfija en lista).

        Args:
            tokens (list): Lista de tokens en infija.

        Returns:
            Nodo: Raíz del árbol de expresión construido.
        """
        pila_operandos = []
        pila_operadores = []

        for token in tokens:

            if _es_operando(token):
                pila_operandos.append(Nodo(token))

            elif token == PARENTESIS_APERTURA:
                pila_operadores.append(token)

            elif token == PARENTESIS_CIERRE:
                while pila_operadores and pila_operadores[-1] != PARENTESIS_APERTURA:
                    self._combinar_nodos(pila_operadores, pila_operandos)
                pila_operadores.pop()

            elif token in OPERADORES:
                while (
                    pila_operadores
                    and pila_operadores[-1] != PARENTESIS_APERTURA
                    and pila_operadores[-1] in OPERADORES
                    and self._debe_procesar(token, pila_operadores[-1])
                ):
                    self._combinar_nodos(pila_operadores, pila_operandos)
                pila_operadores.append(token)

        while pila_operadores:
            self._combinar_nodos(pila_operadores, pila_operandos)

        return pila_operandos[0] if pila_operandos else None

    def _debe_procesar(self, operador_actual: str, operador_tope: str) -> bool:
        """
        Determina si el operador en el tope de la pila debe procesarse
        antes del operador actual, según precedencia y asociatividad.

        Args:
            operador_actual (str): Operador que se está procesando.
            operador_tope   (str): Operador en el tope de la pila.

        Returns:
            bool: True si el tope debe procesarse primero.
        """
        prec_actual = PRECEDENCIA[operador_actual]
        prec_tope = PRECEDENCIA[operador_tope]

        if operador_actual == "^":
            return prec_tope > prec_actual

        return prec_tope >= prec_actual

    def _combinar_nodos(
        self,
        pila_operadores: list,
        pila_operandos: list
    ) -> None:
        """
        Extrae un operador y sus dos operandos, forma un subárbol
        y lo empuja de vuelta a la pila de operandos.

        Args:
            pila_operadores (list): Pila de operadores (strings).
            pila_operandos  (list): Pila de nodos (subárboles).
        """
        nodo_op = Nodo(pila_operadores.pop())
        nodo_op.derecho = pila_operandos.pop()
        nodo_op.izquierdo = pila_operandos.pop()
        pila_operandos.append(nodo_op)

    ##############
    # Recorridos #
    ##############

    def postorden(self) -> list:
        """
        Recorre el árbol en postorden (izquierdo → derecho → raíz).

        Returns:
            list: Lista de tokens en notación posfija.
        """
        resultado = []
        self._postorden_rec(self._raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido postorden."""
        if nodo:
            self._postorden_rec(nodo.izquierdo, resultado)
            self._postorden_rec(nodo.derecho, resultado)
            resultado.append(nodo.dato)

    def inorden(self) -> list:
        """
        Recorre el árbol en inorden (izquierdo → raíz → derecho).

        Returns:
            list: Lista de tokens en notación infija.
        """
        resultado = []
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido inorden."""
        if nodo:
            self._inorden_rec(nodo.izquierdo, resultado)
            resultado.append(nodo.dato)
            self._inorden_rec(nodo.derecho, resultado)

    def preorden(self) -> list:
        """
        Recorre el árbol en preorden (raíz → izquierdo → derecho).

        Returns:
            list: Lista de tokens en notación prefija.
        """
        resultado = []
        self._preorden_rec(self._raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo: Nodo, resultado: list) -> None:
        """Auxiliar recursivo para el recorrido preorden."""
        if nodo:
            resultado.append(nodo.dato)
            self._preorden_rec(nodo.izquierdo, resultado)
            self._preorden_rec(nodo.derecho, resultado)

    ##############
    # Evaluación #
    ##############

    def evaluar(self) -> float:
        """
        Evalúa la expresión recorriendo el árbol de forma recursiva.

        Returns:
            float: Resultado numérico de la expresión.

        Raises:
            ZeroDivisionError: Si hay división por cero.
            ValueError       : Si el árbol está vacío.
        """
        if self.esta_vacio():
            raise ValueError("El árbol de expresión está vacío.")
        return self._evaluar_rec(self._raiz)

    def _evaluar_rec(self, nodo: Nodo) -> float:
        """
        Auxiliar recursivo para evaluar el árbol.

        Args:
            nodo (Nodo): Nodo actual.

        Returns:
            float: Resultado del subárbol.
        """
        if nodo.es_hoja():
            return float(nodo.dato)

        izq = self._evaluar_rec(nodo.izquierdo)
        der = self._evaluar_rec(nodo.derecho)

        operaciones = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b,
        }

        if nodo.dato == "/" and der == 0:
            raise ZeroDivisionError("División por cero detectada en la expresión.")

        return operaciones[nodo.dato](izq, der)

    ###########################
    # Visualización del árbol #
    ###########################

    def graficar(self) -> None:
        """
        Genera y abre una imagen gráfica del árbol de expresión
        usando Graphviz.

        Operadores : nodos azules
        Operandos  : nodos verdes
        """
        from graphviz import Digraph

        if self.esta_vacio():
            print("  (árbol vacío, nada que graficar)")
            return

        dot = Digraph(comment=self._expresion_infija)
        dot.attr(rankdir="TB")
        dot.attr("node", fontsize="14")

        self._graficar_rec(self._raiz, dot, contador=[0])

        dot.render("arbol_expresion", format="png", view=True, cleanup=True)
        print("  ✓ Árbol abierto como 'arbol_expresion.png'")

    def _graficar_rec(self, nodo: Nodo, dot, contador: list) -> str:
        """Auxiliar recursivo para construir el grafo nodo por nodo."""
        if nodo is None:
            return None

        nodo_id = str(contador[0])
        contador[0] += 1

        if nodo.es_hoja():
            dot.node(nodo_id, label=str(nodo.dato),
                    shape="circle", style="filled",
                    fillcolor="lightgreen")
        else:
            dot.node(nodo_id, label=str(nodo.dato),
                    shape="circle", style="filled",
                    fillcolor="lightblue")

        id_izq = self._graficar_rec(nodo.izquierdo, dot, contador)
        if id_izq:
            dot.edge(nodo_id, id_izq)

        id_der = self._graficar_rec(nodo.derecho, dot, contador)
        if id_der:
            dot.edge(nodo_id, id_der)

        return nodo_id

    ##################
    # Representación #
    ##################

    def __str__(self) -> str:
        """Retorna la expresión infija original almacenada."""
        return self._expresion_infija if self._expresion_infija else "Árbol vacío"


######################
# Auxiliar de módulo #
######################

def _es_operando(token: str) -> bool:
    """
    Verifica si un token es un número (operando).

    Args:
        token (str): Token a comprobar.

    Returns:
        bool: True si el token es un número (entero o decimal, con signo).
    """
    import re
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", token))