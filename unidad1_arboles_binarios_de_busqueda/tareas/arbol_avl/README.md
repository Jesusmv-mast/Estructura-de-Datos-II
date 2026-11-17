# Árbol AVL

## Descripción

Implementación de un **árbol AVL**, que es un árbol binario de búsqueda balanceado. Después de cada inserción o eliminación se calcula el factor de balance y, si es necesario, se aplican rotaciones para mantener la altura bajo control.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `nodoavl.py` | Nodo con `dato`, hijos y altura |
| `arbolavl.py` | Árbol AVL con rotaciones, inserción, búsqueda y eliminación |
| `mainavl.py` | Programa de prueba con inserciones y eliminaciones |

## Cómo ejecutar

Desde esta carpeta:

```bash
python mainavl.py
```

## Operaciones implementadas

- `insertar(dato)`: inserta y rebalancea el árbol.
- `buscar(dato)`: indica si el dato existe.
- `eliminar(dato)`: elimina un nodo y rebalancea.
- `inorden()` / `preorden()`: recorridos del árbol.
- `imprimir()`: representación visual en consola.

## Rotaciones

- Rotación simple a la derecha.
- Rotación simple a la izquierda.
- Rotación doble izquierda-derecha.
- Rotación doble derecha-izquierda.

El factor de balance de un nodo es:

```text
factor = altura(subárbol izquierdo) - altura(subárbol derecho)
```

Un AVL se mantiene balanceado si el factor de cada nodo está en `-1`, `0` o `1`.

## Complejidad

| Operación | Complejidad |
| --- | --- |
| Inserción | O(log n) |
| Búsqueda | O(log n) |
| Eliminación | O(log n) |

La diferencia con un ABB sin balanceo es que el AVL garantiza O(log n) incluso en el peor caso.
