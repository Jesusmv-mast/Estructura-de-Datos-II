"""
Autor: Charles Jesus Morales Velasco
Titulo: Validador - Validación de expresiones infijas durante la carga
Version: 1.0.0
Fecha: 2026
"""

import re

OPERADORES = {"+", "-", "*", "/", "^"}
PARENTESIS_APERTURA = "("
PARENTESIS_CIERRE = ")"


def validar_expresion(tokens: list) -> tuple:
    """
    Valida una lista de tokens de una expresión infija.

    Realiza las siguientes comprobaciones en orden:
        1. Lista vacía.
        2. Caracteres / tokens inválidos.
        3. Paréntesis balanceados y correctamente anidados.
        4. El primer y último token son válidos.
        5. No hay dos operadores consecutivos (excluyendo unarios ya absorbidos).
        6. No hay dos operandos consecutivos.
        7. Paréntesis vacíos '()'.
        8. Operador justo antes de paréntesis de cierre.
        9. Operador justo después de paréntesis de apertura
            (casos como '(* 3 + 5)').

    Args:
        tokens (list): Lista de strings generada por Tokenizador.tokenizar().

    Returns:
        tuple: (es_valida: bool, mensaje: str)
            - Si es_valida es True  → mensaje es cadena vacía.
            - Si es_valida es False → mensaje describe el primer error encontrado.

    Examples:
        >>> validar_expresion(['3', '+', '5'])
        (True, '')
        >>> validar_expresion(['+', '5'])
        (False, 'La expresión no puede comenzar con el operador "+".')
    """
    # 1. Expresión vacía
    if not tokens:
        return False, "La expresión está vacía."

    # 2. Tokens inválidos (ni número, ni operador, ni paréntesis)
    for token in tokens:
        if not _es_token_valido(token):
            return False, f'Token inválido encontrado: "{token}".'

    # 3. Paréntesis balanceados
    ok, msg = _validar_parentesis(tokens)
    if not ok:
        return False, msg

    # 4. Primer token
    primero = tokens[0]
    if primero in OPERADORES:
        return False, f'La expresión no puede comenzar con el operador "{primero}".'
    if primero == PARENTESIS_CIERRE:
        return False, 'La expresión no puede comenzar con ")".'

    # 5. Último token
    ultimo = tokens[-1]
    if ultimo in OPERADORES:
        return False, f'La expresión no puede terminar con el operador "{ultimo}".'
    if ultimo == PARENTESIS_APERTURA:
        return False, 'La expresión no puede terminar con "(".'

    # 6-9. Revisión de pares de tokens consecutivos
    for i in range(len(tokens) - 1):
        actual = tokens[i]
        siguiente = tokens[i + 1]

        # 6. Dos operadores consecutivos
        if actual in OPERADORES and siguiente in OPERADORES:
            return (
                False,
                f'Operadores consecutivos no permitidos: "{actual}" seguido de "{siguiente}".'
            )

        # 7. Paréntesis vacíos
        if actual == PARENTESIS_APERTURA and siguiente == PARENTESIS_CIERRE:
            return False, 'Paréntesis vacíos "()" no están permitidos.'

        # 8. Operador justo antes de ')'
        if actual in OPERADORES and siguiente == PARENTESIS_CIERRE:
            return (
                False,
                f'Operador "{actual}" no puede ir justo antes de ")".'
            )

        # 9. Operador justo después de '(' (cuando no es unario)
        if actual == PARENTESIS_APERTURA and siguiente in OPERADORES:
            return (
                False,
                f'Operador "{siguiente}" no puede ir justo después de "(".'
            )

        # 10. Dos operandos consecutivos (sin operador entre ellos)
        if _es_operando(actual) and _es_operando(siguiente):
            return (
                False,
                f'Operandos consecutivos sin operador: "{actual}" y "{siguiente}".'
            )

    return True, ""


#######################
# Auxiliares privadas #
#######################

def _es_token_valido(token: str) -> bool:
    """
    Verifica si un token es un número, operador o paréntesis válido.

    Args:
        token (str): Token a comprobar.

    Returns:
        bool: True si el token es válido.
    """
    if token in OPERADORES:
        return True
    if token in (PARENTESIS_APERTURA, PARENTESIS_CIERRE):
        return True
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", token))


def _es_operando(token: str) -> bool:
    """
    Verifica si un token es un número (operando).

    Args:
        token (str): Token a comprobar.

    Returns:
        bool: True si el token es un número.
    """
    return bool(re.fullmatch(r"-?\d+(\.\d+)?", token))


def _validar_parentesis(tokens: list) -> tuple:
    """
    Verifica que los paréntesis estén correctamente balanceados y anidados.

    Args:
        tokens (list): Lista de tokens.

    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    contador = 0
    for i, token in enumerate(tokens, start=1):
        if token == PARENTESIS_APERTURA:
            contador += 1
        elif token == PARENTESIS_CIERRE:
            contador -= 1
            if contador < 0:
                return False, f'Paréntesis de cierre ")" inesperado en la posición {i}.'
    if contador != 0:
        return False, f"Faltan {contador} paréntesis de cierre \")\"."
    return True, ""