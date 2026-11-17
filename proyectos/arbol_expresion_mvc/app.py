"""
Autor: Charles Jesus Morales Velasco
Titulo: Árbol de Expresión - MVC
Version: 1.0.0
Fecha: 2026
"""

from flask import Flask
from Controllers.arbol_controller import arbol_bp

app = Flask(__name__)
app.secret_key = "arbol_expresion_key"
app.jinja_env.globals["enumerate"] = enumerate

app.register_blueprint(arbol_bp)

if __name__ == "__main__":
    app.run(debug=True)