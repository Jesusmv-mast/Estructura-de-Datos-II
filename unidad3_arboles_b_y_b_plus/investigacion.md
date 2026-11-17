# Investigación sobre árboles B y B+

## Descripción

Investigación sobre los árboles B y B+: definición, propiedades, operaciones, diferencias y aplicaciones.

## 1. Árbol B

Un **árbol B de orden `m`** es un árbol M-vías balanceado con las siguientes propiedades:

- Cada nodo tiene como máximo `m` hijos.
- Cada nodo, excepto la raíz, tiene al menos `ceil(m / 2)` hijos.
- La raíz tiene al menos 2 hijos si no es hoja.
- Un nodo con `k` hijos contiene `k - 1` claves ordenadas.
- Todas las hojas están al mismo nivel.
- Las claves de un nodo separan los rangos de sus hijos.

Ejemplo de árbol B de orden 3 (2-3):

```text
            [ 10 | 20 ]
           /     |     \
      [5, 7]   [15]   [25, 30]
```

### Operaciones

#### Búsqueda

Se compara la clave con las claves del nodo y se desciende por el hijo cuyo rango la contiene. La altura es O(log n).

#### Inserción

1. Se busca la hoja donde debe ir la clave.
2. Se inserta ordenadamente.
3. Si el nodo supera `m - 1` claves, se divide en dos y la clave media sube al padre.
4. La división puede propagarse hasta la raíz, que es la única forma de que el árbol crezca en altura.

#### Eliminación

1. Se localiza la clave.
2. Si está en un nodo interno, se sustituye por el predecesor o sucesor.
3. Si el nodo queda por debajo del mínimo, se pide prestada una clave a un hermano o se fusiona con él.
4. La fusión puede propagarse hacia arriba y reducir la altura.

## 2. Árbol B+

Un **árbol B+** es una variante del árbol B con estas diferencias:

- Todas las claves reales se almacenan en las hojas.
- Los nodos internos solo contienen claves de guía para dirigir la búsqueda.
- Las hojas están enlazadas entre sí mediante una lista, lo que permite recorridos secuenciales eficientes.
- Se pueden almacenar más claves por nodo interno, porque no guardan datos asociados.
- Las búsquedas siempre terminan en una hoja, por lo que el rendimiento es uniforme.

```text
Nodos internos:       [ 10 | 20 ]
                      /    |    \
Hojas:          [5,7] -> [10,15] -> [20,25,30]
```

### Ventajas del B+

- Mejor rendimiento en consultas por rango (`BETWEEN`, `ORDER BY`).
- Recorrido secuencial sencillo gracias a los enlaces entre hojas.
- Mayor fan-out en nodos internos, lo que reduce la altura.
- Búsquedas con tiempo uniforme, porque siempre se llega a una hoja.

### Desventajas del B+

- Las claves se duplican: aparecen como guía en nodos internos y como dato en hojas.
- Requiere más espacio que un árbol B.
- La implementación es más compleja.

## 3. Comparación

| Característica | Árbol B | Árbol B+ |
| --- | --- | --- |
| Ubicación de los datos | En nodos internos y hojas | Solo en hojas |
| Claves duplicadas | No | Sí, como guías |
| Recorrido por rango | Menos eficiente | Muy eficiente |
| Enlaces entre hojas | No | Sí |
| Altura | Ligeramente mayor | Menor |
| Uso típico | Índices generales | Bases de datos relacionales |

## 4. Complejidad

Para un árbol con `n` claves y orden `m`:

- Altura: `O(log_m n)`.
- Búsqueda: `O(log_m n)`.
- Inserción: `O(log_m n)`.
- Eliminación: `O(log_m n)`.
- Recorrido completo: `O(n)`.

## 5. Aplicaciones

- **Bases de datos:** MySQL InnoDB usa árboles B+ para sus índices; SQLite usa árboles B.
- **Sistemas de archivos:** NTFS, ext4, APFS y HFS+ usan variantes de árboles B.
- **Motores de almacenamiento:** índices de claves primarias y secundarias.
- **Sistemas con memoria secundaria:** cualquier estructura que necesite minimizar accesos a disco.

## 6. Conclusión

Los árboles B y B+ son la evolución balanceada de los árboles M-vías. El árbol B es más general y el B+ está optimizado para consultas por rango y recorridos secuenciales, por eso es el más usado en bases de datos.

## Referencias

- Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. *Introduction to Algorithms*.
- Silberschatz, A., Korth, H. F. y Sudarshan, S. *Database System Concepts*.
- Documentación de MySQL InnoDB y SQLite sobre índices B-tree.
