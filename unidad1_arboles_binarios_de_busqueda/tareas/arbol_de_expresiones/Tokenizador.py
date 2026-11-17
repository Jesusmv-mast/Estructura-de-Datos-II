"""
Autor: Charles Jesus Morales Velasco
Titulo: Tokenizador - Separación de expresiones infijas en tokens
Version: 1.0.0
Fecha: 2026
"""

OPERADORES = {"+", "-", "*", "/", "^"}
PARENTESIS_APERTURA = "("
PARENTESIS_CIERRE = ")"


def tokenizar(expresion: str) -> list:
    """
    Convierte una expresión infija en una lista de tokens.

    Soporta:
        - Números enteros y decimales (ej: 3, 3.14)
        - Números negativos al inicio o tras operador/paréntesis (ej: -5 + 3)
        - Operadores: +  -  *  /  ^
        - Paréntesis: ( )

    Args:
        expresion (str): Expresión matemática en notación infija.

    Returns:
        list: Lista de strings, cada uno es un token.

    Examples:
        >>> tokenizar("3 + 5 * 10")
        ['3', '+', '5', '*', '10']
        >>> tokenizar("(3 + 5) * -2")
        ['(', '3', '+', '5', ')', '*', '-2']
    """
    tokens = []
    i = 0
    expresion = expresion.strip()

    while i < len(expresion):
        caracter = expresion[i]

        # Ignorar espacios
        if caracter == " ":
            i += 1
            continue

        # Número: entero o decimal, con posible signo negativo
        if caracter.isdigit() or caracter == ".":
            token, i = _leer_numero(expresion, i)
            tokens.append(token)
            continue

        # Signo negativo unario: al inicio o tras operador / paréntesis apertura
        if caracter == "-" and _es_negativo_unario(tokens):
            token, i = _leer_numero(expresion, i)
            tokens.append(token)
            continue

        # Operador o paréntesis
        if caracter in OPERADORES or caracter in (PARENTESIS_APERTURA, PARENTESIS_CIERRE):
            tokens.append(caracter)
            i += 1
            continue

        # Carácter inválido: lo devolvemos igual para que el Validador lo detecte
        tokens.append(caracter)
        i += 1

    return tokens


def _leer_numero(expresion: str, inicio: int) -> tuple:
    """
    Lee un número (entero o decimal, con posible signo) desde la posición dada.

    Args:
        expresion (str): Cadena completa de la expresión.
        inicio (int): Índice de inicio de la lectura.

    Returns:
        tuple: (token_str, nuevo_indice)
    """
    j = inicio
    if expresion[j] == "-":
        j += 1

    while j < len(expresion) and (expresion[j].isdigit() or expresion[j] == "."):
        j += 1

    return expresion[inicio:j], j


def _es_negativo_unario(tokens: list) -> bool:
    """
    Determina si el signo '-' actual es un operador unario (negativo).

    Un '-' es unario si la lista de tokens está vacía o el último token
    es un operador o un paréntesis de apertura.

    Args:
        tokens (list): Lista de tokens procesados hasta el momento.

    Returns:
        bool: True si '-' debe interpretarse como signo negativo.
    """
    if not tokens:
        return True
    ultimo = tokens[-1]
    return ultimo in OPERADORES or ultimo == PARENTESIS_APERTURA