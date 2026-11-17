# Árbol Binario de Búsqueda (ABB)

## Descripción

Implementación de un **Árbol Binario de Búsqueda** en dos versiones: una **recursiva** y una **iterativa**. Ambas comparten la clase `Nodo` y ofrecen las mismas operaciones.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `Nodo.py` | Nodo del árbol con `dato`, `izquierdo` y `derecho` |
| `Arbol_recursivo.py` | ABB con inserción, búsqueda y eliminación recursivas |
| `Arbol_iterativo.py` | ABB con inserción, búsqueda y eliminación iterativas |

## Cómo ejecutar

Desde esta carpeta:

```bash
python Arbol_recursivo.py
```

```bash
python Arbol_iterativo.py
```

## Operaciones implementadas

- `insertar(dato)`: agrega un valor respetando la propiedad del ABB.
- `buscar(dato)`: retorna `True` o `False`.
- `buscar_dato(dato)`: retorna el dato encontrado o `None`.
- `eliminar(dato)`: elimina un nodo y retorna si la operación tuvo éxito.
- `esta_vacio()` / `raiz()`: consultan el estado del árbol.
- `altura()` / `contar_nodos()` / `es_balanceado()`: métricas del árbol.
- `minimo()` / `maximo()`: valores extremos.
- `inorden()`, `preorden()`, `postorden()` y `por_niveles()`: recorridos.
- `imprimir()`: representación visual en consola.

## Propiedad del ABB

Para cada nodo `N`:

- Todos los valores del subárbol izquierdo son menores que `N.dato`.
- Todos los valores del subárbol derecho son mayores que `N.dato`.

El recorrido **inorden** devuelve los datos ordenados de menor a mayor.

## Complejidad

| Operación | Caso promedio | Peor caso |
| --- | --- | --- |
| Inserción | O(log n) | O(n) |
| Búsqueda | O(log n) | O(n) |
| Eliminación | O(log n) | O(n) |

El peor caso aparece cuando el árbol se degenera en una lista.
