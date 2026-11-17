# Investigación sobre árboles M-vías

## Descripción

Investigación sobre los árboles M-vías: definición, propiedades, operaciones básicas, ventajas frente a los árboles binarios y aplicaciones.

## Contenido de la investigación

### 1. Definición

Un **árbol M-vías** es un árbol de búsqueda en el que cada nodo puede tener como máximo `M` hijos y almacenar como máximo `M - 1` claves. Las claves de cada nodo están ordenadas de menor a mayor y separan los rangos de valores de sus hijos.

Formalmente, un nodo con `k` claves (`k <= M - 1`) tiene `k + 1` hijos:

```text
        [ k1 | k2 | k3 ]
       /    |    |    \
    <k1  k1..k2 k2..k3  >k3
```

Cada hijo contiene valores comprendidos entre las claves que lo delimitan.

### 2. Propiedades

- El número máximo de hijos de un nodo es `M`.
- El número máximo de claves por nodo es `M - 1`.
- Las claves dentro de un nodo están ordenadas.
- Todos los valores del subárbol de un hijo están dentro del rango definido por las claves del padre.
- Un árbol M-vías **no tiene por qué estar balanceado**; si se exige equilibrio se obtiene un árbol B.
- La altura puede reducirse mucho frente a un árbol binario, porque cada nodo guarda varias claves.

### 3. Operaciones básicas

#### Búsqueda

1. Comparar la clave buscada con las claves del nodo actual.
2. Si coincide con alguna clave, se encontró.
3. Si no coincide, elegir el hijo cuyo rango contiene la clave.
4. Repetir hasta encontrar la clave o llegar a una hoja.

#### Inserción

1. Buscar la posición donde debería ir la nueva clave.
2. Insertarla ordenadamente en el nodo correspondiente.
3. Si el nodo supera el máximo de claves, dividirlo y subir la clave media al padre.
4. Repetir la división hacia arriba si es necesario.

#### Eliminación

1. Localizar la clave.
2. Si está en una hoja, quitarla.
3. Si está en un nodo interno, reemplazarla por un predecesor o sucesor.
4. Si el nodo queda con muy pocas claves, redistribuir o fusionar con un hermano.

### 4. Ejemplo con M = 3

Con `M = 3`, cada nodo puede tener hasta 2 claves y 3 hijos. Este caso se conoce como **árbol 2-3**.

```text
          [ 10 | 20 ]
         /     |     \
     [5, 7]  [15]   [25, 30]
```

- La búsqueda de `15` va al hijo central porque `10 < 15 < 20`.
- La búsqueda de `30` va al hijo derecho porque `30 > 20`.

### 5. Ventajas

- Menor altura que un árbol binario para el mismo número de claves.
- Menos accesos a disco, porque cada nodo puede llenar un bloque completo.
- Buen rendimiento en estructuras de almacenamiento externo.
- Base conceptual de los árboles B y B+.

### 6. Desventajas

- Implementación más compleja que un árbol binario.
- Los nodos suelen desperdiciar espacio si no están llenos.
- Las divisiones y fusiones requieren manejar varios casos.
- Sin balanceo, el rendimiento puede degradarse.

### 7. Aplicaciones

- Sistemas de bases de datos y archivos.
- Índices en memoria secundaria.
- Estructuras de almacenamiento por bloques.
- Implementación de diccionarios y mapas ordenados en algunos sistemas.

### 8. Comparación con un árbol binario de búsqueda

| Característica | Árbol binario de búsqueda | Árbol M-vías |
| --- | --- | --- |
| Hijos por nodo | Máximo 2 | Hasta M |
| Claves por nodo | 1 | Hasta M - 1 |
| Altura | Mayor | Menor |
| Accesos a disco | Muchos | Pocos |
| Implementación | Sencilla | Más compleja |
| Uso típico | Memoria principal | Bases de datos y archivos |

## Conclusión

Los árboles M-vías son una generalización de los árboles de búsqueda pensada para aprovechar bloques de almacenamiento. Su principal ventaja es reducir la altura del árbol, y son la base de estructuras balanceadas como los árboles B y B+.

## Referencias

- Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. *Introduction to Algorithms*.
- Knuth, D. E. *The Art of Computer Programming, Volume 3: Sorting and Searching*.
- Documentación de estructuras de datos en bases de datos: árboles B y B+.
