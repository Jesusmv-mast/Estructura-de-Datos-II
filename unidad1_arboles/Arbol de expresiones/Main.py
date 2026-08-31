"""
Autor: Charles Jesus Morales Velasco
Titulo: Sistema de Árbol de Expresión - Menú Principal
Version: 1.0.0
Fecha: 2026

Descripción:
    Programa de terminal que permite cargar múltiples expresiones
    matemáticas en notación infija, validarlas, construir su árbol
    de expresión y convertirlas a notación posfija.

Uso:
    python main.py
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from Tokenizador import tokenizar
from Validador import validar_expresion
from Arbol_expresion import ArbolExpresion


##############################
# Constantes de presentación #
##############################

LINEA_SIMPLE = "-" * 60
LINEA_DOBLE = "=" * 60


#########################################
# Funciones de presentación en pantalla #
#########################################

def limpiar_pantalla() -> None:
    """Imprime líneas en blanco para separar secciones."""
    print("\n" * 2)


def imprimir_encabezado() -> None:
    """Imprime el encabezado principal del programa."""
    print(LINEA_DOBLE)
    print("   SISTEMA DE ÁRBOL DE EXPRESIÓN MATEMÁTICA")
    print("   Notación Infija → Árbol → Notación Posfija")
    print(LINEA_DOBLE)


def imprimir_menu() -> None:
    """Imprime el menú de opciones del sistema."""
    print(f"\n{LINEA_SIMPLE}")
    print("  MENÚ PRINCIPAL")
    print(LINEA_SIMPLE)
    print("  [1] Cargar nueva expresión")
    print("  [2] Ver todas las expresiones cargadas")
    print("  [3] Ver detalle de una expresión")
    print("  [4] Convertir expresión a posfija")
    print("  [5] Evaluar resultado de una expresión")
    print("  [6] Ver árbol visual de una expresión")
    print("  [7] Eliminar una expresión")
    print("  [8] Salir")
    print(LINEA_SIMPLE)


def imprimir_resultado_carga(exito: bool, expresion: str, mensaje: str = "") -> None:
    """
    Imprime el resultado del proceso de carga y validación.

    Args:
        exito    (bool): True si la expresión es válida.
        expresion (str): Expresión procesada.
        mensaje   (str): Mensaje de error si no es válida.
    """
    print(f"\n  Expresión : {expresion}")
    if exito:
        print("  Estado    : ✓ Válida - Árbol construido correctamente.")
    else:
        print(f"  Estado    : ✗ Inválida")
        print(f"  Error     : {mensaje}")


#####################
# Lógica de negocio #
#####################

def cargar_expresion(arboles: list) -> None:
    """
    Solicita una expresión al usuario, la valida, construye su árbol
    y lo agrega a la lista de árboles cargados.

    El proceso de validación ocurre durante la carga:
        1. Tokenización de la expresión.
        2. Validación de tokens (paréntesis, operadores, operandos).
        3. Construcción del árbol si la expresión es válida.

    Args:
        arboles (list): Lista donde se almacenan los árboles cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  CARGAR NUEVA EXPRESIÓN")
    print(LINEA_SIMPLE)
    print("  Ejemplos válidos:")
    print("    3 + 5 * 10")
    print("    (3 + 5) * 10")
    print("    2 ^ 3 + -4 / 2")
    print("    (10 - 2) * (3 + 4)")

    expresion = input("\n  Ingrese la expresión: ").strip()

    if not expresion:
        print("  ✗ No ingresó ninguna expresión.")
        return

    # ── Paso 1: Tokenizar ──
    tokens = tokenizar(expresion)

    # ── Paso 2: Validar ──
    es_valida, mensaje_error = validar_expresion(tokens)

    if not es_valida:
        imprimir_resultado_carga(False, expresion, mensaje_error)
        return

    # ── Paso 3: Construir árbol ──
    arbol = ArbolExpresion()
    arbol.construir(tokens, expresion)

    arboles.append(arbol)
    imprimir_resultado_carga(True, expresion)
    print(f"  Índice    : {len(arboles) - 1}")


def ver_todas(arboles: list) -> None:
    """
    Muestra todas las expresiones cargadas con su índice.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  EXPRESIONES CARGADAS")
    print(LINEA_SIMPLE)

    if not arboles:
        print("  No hay expresiones cargadas aún.")
        return

    for i, arbol in enumerate(arboles):
        print(f"  [{i}]  {arbol.expresion_infija}")

    print(f"\n  Total: {len(arboles)} expresión(es).")


def seleccionar_arbol(arboles: list, accion: str = "seleccionar") -> ArbolExpresion | None:
    """
    Solicita al usuario un índice y retorna el árbol correspondiente.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
        accion   (str): Texto descriptivo de la acción (para el prompt).

    Returns:
        ArbolExpresion | None: El árbol seleccionado o None si el índice es inválido.
    """
    if not arboles:
        print("  No hay expresiones cargadas.")
        return None

    ver_todas(arboles)

    try:
        indice = int(input(f"\n  Ingrese el índice para {accion}: "))
    except ValueError:
        print("  ✗ Índice inválido. Debe ingresar un número entero.")
        return None

    if indice < 0 or indice >= len(arboles):
        print(f"  ✗ Índice fuera de rango. Válidos: 0 a {len(arboles) - 1}.")
        return None

    return arboles[indice]


def ver_detalle(arboles: list) -> None:
    """
    Muestra el detalle completo de una expresión seleccionada:
    tokens, infija, prefija, posfija.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  DETALLE DE EXPRESIÓN")
    print(LINEA_SIMPLE)

    arbol = seleccionar_arbol(arboles, "ver detalle")
    if arbol is None:
        return

    posfija = " ".join(arbol.postorden())
    prefija = " ".join(arbol.preorden())
    infija_tokens = " ".join(arbol.inorden())

    print(f"\n  Expresión original : {arbol.expresion_infija}")
    print(f"  Tokens             : {arbol.tokens}")
    print(f"  Infija (árbol)     : {infija_tokens}")
    print(f"  Prefija            : {prefija}")
    print(f"  Posfija            : {posfija}")


def convertir_posfija(arboles: list) -> None:
    """
    Convierte la expresión seleccionada a notación posfija
    usando el recorrido postorden del árbol.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  CONVERTIR A NOTACIÓN POSFIJA")
    print(LINEA_SIMPLE)

    arbol = seleccionar_arbol(arboles, "convertir")
    if arbol is None:
        return

    posfija = arbol.postorden()

    print(f"\n  Infija  : {arbol.expresion_infija}")
    print(f"  Posfija : {' '.join(posfija)}")
    print()
    print("  Explicación del recorrido postorden:")
    print("    izquierdo → derecho → raíz")
    print(f"    Tokens en orden: {posfija}")


def evaluar_expresion(arboles: list) -> None:
    """
    Evalúa numéricamente la expresión seleccionada recorriendo el árbol.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  EVALUAR EXPRESIÓN")
    print(LINEA_SIMPLE)

    arbol = seleccionar_arbol(arboles, "evaluar")
    if arbol is None:
        return

    try:
        resultado = arbol.evaluar()
        # Mostrar entero si no tiene decimales significativos
        if resultado == int(resultado):
            resultado_str = str(int(resultado))
        else:
            resultado_str = f"{resultado:.6f}".rstrip("0")

        print(f"\n  Expresión : {arbol.expresion_infija}")
        print(f"  Resultado : {resultado_str}")

    except ZeroDivisionError as e:
        print(f"\n  ✗ Error: {e}")


def ver_arbol_visual(arboles: list) -> None:
    """
    Muestra la representación visual del árbol de expresión seleccionado.

    El árbol se imprime rotado 90°: el subárbol derecho aparece arriba,
    la raíz en el centro y el subárbol izquierdo abajo.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  ÁRBOL VISUAL DE EXPRESIÓN")
    print(LINEA_SIMPLE)

    arbol = seleccionar_arbol(arboles, "visualizar")
    if arbol is None:
        return

    print(f"\n  Expresión: {arbol.expresion_infija}")
    print(f"\n  Árbol (derecha = arriba, izquierda = abajo):\n")
    arbol.imprimir()


def eliminar_expresion(arboles: list) -> None:
    """
    Elimina una expresión de la lista según el índice indicado.

    Args:
        arboles (list): Lista de árboles de expresión cargados.
    """
    print(f"\n{LINEA_SIMPLE}")
    print("  ELIMINAR EXPRESIÓN")
    print(LINEA_SIMPLE)

    arbol = seleccionar_arbol(arboles, "eliminar")
    if arbol is None:
        return

    confirmacion = input(
        f"\n  ¿Eliminar \"{arbol.expresion_infija}\"? (s/n): "
    ).strip().lower()

    if confirmacion == "s":
        arboles.remove(arbol)
        print("  ✓ Expresión eliminada correctamente.")
    else:
        print("  Eliminación cancelada.")


##############################
# Punto de entrada principal #
##############################

def main() -> None:
    """
    Función principal del programa.

    Controla el ciclo del menú y delega cada opción a su función
    correspondiente. Mantiene la lista de árboles cargados en memoria
    durante toda la sesión.
    """
    arboles = []

    imprimir_encabezado()

    while True:
        imprimir_menu()
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            cargar_expresion(arboles)

        elif opcion == "2":
            ver_todas(arboles)

        elif opcion == "3":
            ver_detalle(arboles)

        elif opcion == "4":
            convertir_posfija(arboles)

        elif opcion == "5":
            evaluar_expresion(arboles)

        elif opcion == "6":
            ver_arbol_visual(arboles)

        elif opcion == "7":
            eliminar_expresion(arboles)

        elif opcion == "8":
            print(f"\n{LINEA_DOBLE}")
            print("  Saliendo del sistema. ¡Hasta luego!")
            print(LINEA_DOBLE)
            break

        else:
            print("  ✗ Opción inválida. Ingrese un número del 1 al 8.")

        input("\n  Presione ENTER para continuar...")


if __name__ == "__main__":
    main()