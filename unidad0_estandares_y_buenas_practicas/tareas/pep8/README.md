# Guía de PEP 8 aplicada a una estructura de datos

## Descripción

La tarea consiste en investigar las reglas de estilo de **PEP 8** y mostrar cómo se aplican en la implementación de una estructura de datos. Como ejemplo se usa una **pila** (stack) implementada con una lista de Python.

## Archivos

| Archivo | Descripción |
| --- | --- |
| `guia_pep8.md` | Resumen de las reglas principales de PEP 8 con ejemplos de antes y después |
| `pila_pep8.py` | Implementación de una pila siguiendo PEP 8, PEP 257 y buenas prácticas |

## Cómo ejecutar

Desde esta carpeta:

```bash
python pila_pep8.py
```

## Qué se demuestra

- Indentación de 4 espacios.
- Nombres en `snake_case` para variables y funciones.
- Nombres en `PascalCase` para clases.
- Constantes en `UPPER_CASE`.
- Líneas de máximo 79 caracteres.
- Docstrings en módulos, clases y métodos.
- Separación de imports, clases y bloques principales.
- Manejo explícito de errores con una excepción propia.
- Uso de `if __name__ == "__main__":` para el código de prueba.
