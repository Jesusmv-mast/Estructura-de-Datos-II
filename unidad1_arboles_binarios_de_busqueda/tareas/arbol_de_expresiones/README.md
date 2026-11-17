# Árbol de Expresiones

## Descripción

Sistema de terminal que recibe expresiones matemáticas en **notación infija**, las valida, construye su **árbol de expresión** y permite convertir la expresión a **notación posfija**, evaluarla y generar una gráfica del árbol.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `Nodo.py` | Nodo del árbol de expresión |
| `Tokenizador.py` | Convierte la cadena de entrada en tokens |
| `Validador.py` | Verifica paréntesis, operadores y operandos |
| `Arbol_expresion.py` | Construye el árbol con el algoritmo Shunting Yard y lo recorre |
| `Main.py` | Menú principal del programa |
| `requirements.txt` | Dependencia opcional para generar gráficos con Graphviz |

## Cómo ejecutar

Desde esta carpeta:

```bash
python Main.py
```

## Funcionalidades del menú

1. Cargar una nueva expresión.
2. Ver todas las expresiones cargadas.
3. Ver el detalle de una expresión.
4. Convertir una expresión a posfija.
5. Evaluar el resultado de una expresión.
6. Ver el árbol visual de una expresión.
7. Eliminar una expresión.
8. Salir.

## Ejemplos de expresiones válidas

```text
3 + 5 * 10
(3 + 5) * 10
2 ^ 3 + -4 / 2
(10 - 2) * (3 + 4)
```

## Notaciones

- **Infija:** `3 + 5 * 10` (la que escribe el usuario).
- **Posfija:** `3 5 10 * +` (la que se obtiene al recorrer el árbol en postorden).
- **Árbol:** los operadores quedan en los nodos internos y los operandos en las hojas.

## Gráfico del árbol

La opción 6 usa la librería de Python `graphviz`. Para instalarla:

```bash
pip install -r requirements.txt
```

También es necesario tener instalado el programa **Graphviz** del sistema y que el comando `dot` esté disponible en el `PATH`.

## Complejidad

- Construcción del árbol: O(n), donde `n` es la cantidad de tokens.
- Evaluación: O(n).
- Recorridos: O(n).
