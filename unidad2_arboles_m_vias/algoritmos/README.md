# Algoritmo: Árbol M-vías

## Archivo

| Archivo | Descripción |
| --- | --- |
| `arbol_m_vias.py` | Árbol M-vías balanceado con búsqueda, inserción, recorrido y altura |

## Qué implementa

- Nodos con hasta `M - 1` claves y hasta `M` hijos.
- Búsqueda de una clave descendiendo por el hijo correspondiente.
- Inserción ordenada en la hoja.
- División de nodos cuando se supera el máximo de claves.
- Propagación de la clave media hacia el padre.
- Recorrido inorden para obtener las claves ordenadas.
- Cálculo de altura y representación por niveles.

## Ejemplo

Con `orden=3` se obtiene un **árbol 2-3**: cada nodo tiene como máximo 2 claves y 3 hijos.

```text
Nivel 0: [[10, 20]]
Nivel 1: [[6], [15], [30]]
Nivel 2: [[3, 5], [7], [12], [17], [25], [40, 50]]
```

## Cómo ejecutar

Desde esta carpeta:

```bash
python arbol_m_vias.py
```

## Uso desde otro programa

```python
from arbol_m_vias import ArbolMVias

arbol = ArbolMVias(orden=3)
for valor in [10, 20, 5, 6, 12, 30]:
    arbol.insertar(valor)

print(arbol.recorrido())   # [5, 6, 10, 12, 20, 30]
print(arbol.buscar(12))    # True
print(arbol.altura())
```

## Complejidad

Para `n` claves y orden `M`:

- Búsqueda: O(log n).
- Inserción: O(log n) más el costo de dividir nodos.
- Recorrido completo: O(n).
- Altura: O(log n), porque todas las hojas quedan al mismo nivel.

## Nota

La eliminación no está implementada en este ejemplo. Se puede agregar como ejercicio usando préstamos entre hermanos y fusiones, igual que en un árbol B.
