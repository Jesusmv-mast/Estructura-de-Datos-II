# Unidad 1: Árboles binarios de búsqueda

En esta unidad se estudian los árboles binarios y, en particular, los **árboles binarios de búsqueda (BST)**. También se incluyen las prácticas y los proyectos de aplicación relacionados con árboles.

## Tareas

| Carpeta | Tema |
| --- | --- |
| [tablero_tres_en_raya](tareas/tablero_tres_en_raya/README.md) | Tablero Tres en Raya con nodos y árbol |
| [arbol_binario_busqueda](tareas/arbol_binario_busqueda/README.md) | Árbol Binario de Búsqueda recursivo e iterativo |
| [arbol_avl](tareas/arbol_avl/README.md) | Árbol AVL balanceado |
| [arbol_de_expresiones](tareas/arbol_de_expresiones/README.md) | Árbol de expresiones matemáticas |

## Proyectos

Los proyectos de aplicación están en la carpeta [`proyectos/`](../proyectos/README.md) de la raíz del repositorio:

| Proyecto | Tema |
| --- | --- |
| [arbol_expresion_mvc](../proyectos/arbol_expresion_mvc/README.md) | Árbol de expresiones con MVC y Flask |
| [conecta_4](../proyectos/conecta_4/README.md) | Conecta 4 con MVC, Minimax y árbol de decisión |

## Conceptos clave

- **Nodo:** unidad básica del árbol. Almacena un elemento y referencias a sus hijos.
- **Raíz:** nodo superior del árbol, sin padre.
- **Hoja:** nodo sin hijos.
- **Árbol binario:** cada nodo tiene como máximo dos hijos.
- **Árbol binario de búsqueda:** para cada nodo, los valores menores van al subárbol izquierdo y los mayores al derecho.
- **Recorridos:** preorden, inorden, postorden y por niveles.

## Propiedad de un BST

Para todo nodo `N`:

- Todos los valores del subárbol izquierdo son menores que `N`.
- Todos los valores del subárbol derecho son mayores que `N`.
- No se permiten duplicados (o se define una política para ellos).

El recorrido **inorden** de un BST devuelve los elementos ordenados de menor a mayor.

## Complejidad

| Operación | Caso promedio | Peor caso |
| --- | --- | --- |
| Búsqueda | O(log n) | O(n) |
| Inserción | O(log n) | O(n) |
| Eliminación | O(log n) | O(n) |

El peor caso ocurre cuando el árbol queda degenerado en una lista (por ejemplo, al insertar valores ya ordenados).
