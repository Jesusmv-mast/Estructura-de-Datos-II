# Algoritmos: Árboles B y B+

## Archivos

| Archivo | Descripción |
| --- | --- |
| `arbol_b.py` | Árbol B con búsqueda, inserción, eliminación, recorrido y altura |
| `arbol_b_plus.py` | Árbol B+ con búsqueda, inserción, recorrido secuencial y consultas por rango |

## Árbol B

Implementación basada en el **grado mínimo `t`**:

- Cada nodo guarda como máximo `2t - 1` claves.
- Todo nodo distinto de la raíz guarda al menos `t - 1` claves.
- Un nodo con `k` claves tiene `k + 1` hijos si no es hoja.
- Todas las hojas están al mismo nivel.

Operaciones:

- `buscar(clave)`.
- `insertar(clave)` con división de nodos.
- `eliminar(clave)` con préstamo entre hermanos o fusión.
- `recorrido()` en orden ascendente.
- `altura()`.

## Árbol B+

Implementación con **orden `m`**:

- Todas las claves reales están en las hojas.
- Los nodos internos solo guardan separadores.
- Las hojas están enlazadas mediante `siguiente`.
- Cada separador es la clave máxima del subárbol izquierdo.

Operaciones:

- `buscar(clave)`.
- `insertar(clave)` con división y propagación del separador.
- `recorrido()` siguiendo las hojas enlazadas.
- `rango(inicio, fin)` para consultas por intervalo.
- `hojas()` para ver la lista enlazada de hojas.
- `altura()`.

La eliminación no está implementada en el B+; se puede agregar como ejercicio.

## Cómo ejecutar

Desde esta carpeta:

```bash
python arbol_b.py
```

```bash
python arbol_b_plus.py
```

## Ejemplo de árbol B+

```text
Nivel 0: [[20]]
Nivel 1: [[6, 12], [30]]
Nivel 2: [[3, 5, 6], [7, 10, 12], [15, 17, 20], [25, 30], [40, 50]]

Hojas enlazadas:
[3, 5, 6] -> [7, 10, 12] -> [15, 17, 20] -> [25, 30] -> [40, 50]
```

## Uso desde otro programa

```python
from arbol_b import ArbolB
from arbol_b_plus import ArbolBPlus

b = ArbolB(grado_minimo=2)
for valor in [10, 20, 5, 6, 12]:
    b.insertar(valor)

print(b.recorrido())
print(b.buscar(12))
print(b.eliminar(6))

b_plus = ArbolBPlus(orden=4)
for valor in [10, 20, 5, 6, 12, 30]:
    b_plus.insertar(valor)

print(b_plus.recorrido())
print(b_plus.rango(6, 20))
```

## Complejidad

Para `n` claves:

| Operación | Árbol B | Árbol B+ |
| --- | --- | --- |
| Búsqueda | O(log n) | O(log n) |
| Inserción | O(log n) | O(log n) |
| Eliminación | O(log n) | No implementada |
| Recorrido completo | O(n) | O(n) |
| Consulta por rango | O(log n + k) | O(log n + k) |

`k` es la cantidad de claves devueltas por la consulta.
