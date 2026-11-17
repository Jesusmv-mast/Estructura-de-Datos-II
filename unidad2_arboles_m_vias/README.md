# Unidad 2: Árboles M-vías

En esta unidad se introducen los **árboles M-vías** (también llamados árboles multicamino o de búsqueda m-aria), que generalizan los árboles binarios permitiendo más de dos hijos por nodo.

## Contenido

- [Investigación sobre árboles M-vías](investigacion.md)
- [Algoritmo: Árbol M-vías en Python](algoritmos/README.md)

## Idea principal

En un árbol M-vías, cada nodo puede tener hasta **M hijos** y almacenar hasta **M - 1 claves** ordenadas. Las claves separan los rangos de búsqueda de cada hijo, lo que reduce la altura del árbol y el número de accesos necesarios para encontrar un elemento.

## Relación con otras estructuras

- Un árbol binario de búsqueda es un caso particular con `M = 2`.
- Los árboles B y B+ son árboles M-vías balanceados.
- Se usan en bases de datos y sistemas de archivos porque están pensados para bloques de disco, no para memoria principal.
