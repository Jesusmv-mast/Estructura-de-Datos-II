# Unidad 3: Árboles B y B+

En esta unidad se estudian los **árboles B** y **árboles B+**, que son árboles M-vías balanceados diseñados para almacenamiento en disco y bases de datos.

## Contenido

- [Investigación sobre árboles B y B+](investigacion.md)
- [Algoritmos: Árboles B y B+ en Python](algoritmos/README.md)

## Idea principal

Un árbol B mantiene todas las hojas al mismo nivel y garantiza que el árbol permanezca balanceado después de cada inserción o eliminación. Un árbol B+ es una variante en la que todas las claves se almacenan en las hojas y las hojas están enlazadas entre sí, lo que facilita los recorridos por rango.

## Aplicaciones

- Índices de bases de datos (MySQL InnoDB, PostgreSQL, SQLite).
- Sistemas de archivos (NTFS, ext4, APFS, HFS+).
- Almacenamiento en bloques y memoria secundaria.
