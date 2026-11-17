"""
Autor: Charles Jesus Morales Velasco
Titulo: Árbol de Expresión - Controlador Web
Version: 1.0.0
Fecha: 2026
"""

from flask import Blueprint, render_template, request, session, send_file
from Models.Tokenizador import tokenizar
from Models.Validador import validar_expresion
from Models.Arbol_expresion import ArbolExpresion
import io

arbol_bp = Blueprint("arbol", __name__)


@arbol_bp.route("/")
def index():
    """Muestra la página principal con las expresiones cargadas."""
    arboles = session.get("arboles", [])
    return render_template("index.html", arboles=arboles)


@arbol_bp.route("/cargar", methods=["POST"])
def cargar():
    """Recibe una expresión del formulario, la valida y la guarda en sesión."""
    expresion = request.form.get("expresion", "").strip()
    arboles = session.get("arboles", [])
    error = None

    if not expresion:
        error = "No ingresó ninguna expresión."
    else:
        tokens = tokenizar(expresion)
        es_valida, mensaje = validar_expresion(tokens)

        if not es_valida:
            error = mensaje
        else:
            arbol = ArbolExpresion()
            arbol.construir(tokens, expresion)
            arboles.append({
                "infija": arbol.expresion_infija,
                "prefija": " ".join(arbol.preorden()),
                "posfija": " ".join(arbol.postorden()),
                "inorden": " ".join(arbol.inorden()),
                "resultado": _evaluar(arbol),
            })
            session["arboles"] = arboles
            session.modified = True

    return render_template("index.html", arboles=arboles, error=error)


@arbol_bp.route("/eliminar/<int:indice>")
def eliminar(indice):
    """Elimina una expresión de la sesión según su índice."""
    arboles = session.get("arboles", [])
    if 0 <= indice < len(arboles):
        arboles.pop(indice)
        session["arboles"] = arboles
        session.modified = True
    return render_template("index.html", arboles=arboles)


@arbol_bp.route("/graficar/<int:indice>")
def graficar(indice):
    """Genera y devuelve la imagen PNG del árbol de expresión."""
    arboles = session.get("arboles", [])

    if indice < 0 or indice >= len(arboles):
        return "Expresión no encontrada", 404

    datos = arboles[indice]
    tokens = tokenizar(datos["infija"])
    arbol = ArbolExpresion()
    arbol.construir(tokens, datos["infija"])

    png_bytes = _generar_png(arbol)
    return send_file(io.BytesIO(png_bytes), mimetype="image/png")


def _generar_png(arbol: ArbolExpresion) -> bytes:
    """
    Genera el PNG del árbol con Graphviz y lo devuelve como bytes.

    Returns:
        bytes: Contenido del PNG.
    """
    from graphviz import Digraph

    dot = Digraph(comment=arbol.expresion_infija)
    dot.attr(rankdir="TB")
    dot.attr("node", fontsize="14")

    _graficar_rec(arbol.raiz, dot, contador=[0])

    return dot.pipe(format="png")


def _graficar_rec(nodo, dot, contador):
    """Construye el grafo recursivamente."""
    if nodo is None:
        return None

    nodo_id = str(contador[0])
    contador[0] += 1

    if nodo.es_hoja():
        dot.node(nodo_id, label=str(nodo.dato),
                shape="circle", style="filled", fillcolor="lightgreen")
    else:
        dot.node(nodo_id, label=str(nodo.dato),
                shape="circle", style="filled", fillcolor="lightblue")

    id_izq = _graficar_rec(nodo.izquierdo, dot, contador)
    if id_izq:
        dot.edge(nodo_id, id_izq)

    id_der = _graficar_rec(nodo.derecho, dot, contador)
    if id_der:
        dot.edge(nodo_id, id_der)

    return nodo_id


def _evaluar(arbol: ArbolExpresion) -> str:
    """
    Evalúa el árbol y retorna el resultado como string.

    Returns:
        Resultado numérico o mensaje de error.
    """
    try:
        resultado = arbol.evaluar()
        if resultado == int(resultado):
            return str(int(resultado))
        return f"{resultado:.6f}".rstrip("0")
    except ZeroDivisionError:
        return "Error: división por cero"