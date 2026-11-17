# Guía de PEP 8 aplicada a estructuras de datos

**PEP 8** es la guía de estilo oficial de Python. No cambia el comportamiento del programa, pero hace que el código sea más fácil de leer, revisar y mantener.

## 1. Indentación

Usar **4 espacios** por nivel. No mezclar espacios y tabulaciones.

```python
# Correcto
def apilar(self, elemento):
    if elemento is None:
        raise ValueError("El elemento no puede ser None")
    self._elementos.append(elemento)
```

## 2. Longitud de línea

Máximo **79 caracteres** por línea. Si una expresión es muy larga, se puede dividir entre paréntesis.

```python
# Correcto
mensaje = (
    "No se puede desapilar: la pila está vacía"
)
```

## 3. Nombres

| Elemento | Convención | Ejemplo |
| --- | --- | --- |
| Variables y funciones | `snake_case` | `total_elementos`, `esta_vacia()` |
| Clases | `PascalCase` | `Pila`, `NodoArbol` |
| Constantes | `UPPER_CASE` | `CAPACIDAD_MAXIMA` |
| Métodos privados | `_snake_case` | `_validar_indice()` |

```python
CAPACIDAD_MAXIMA = 100


class Pila:
    def __init__(self):
        self._elementos = []

    def esta_vacia(self):
        return len(self._elementos) == 0
```

Evitar nombres como `x`, `dato1`, `aux` cuando no aportan información.

## 4. Espacios en blanco

- Un espacio alrededor de operadores: `a + b`, no `a+b`.
- Sin espacio antes de `:` en slices: `lista[1:3]`.
- Dos líneas en blanco entre clases y funciones de nivel superior.
- Una línea en blanco entre métodos de una clase.

```python
# Correcto
def buscar(self, valor):
    for indice, elemento in enumerate(self._elementos):
        if elemento == valor:
            return indice
    return -1
```

## 5. Importaciones

Cada importación en su propia línea, agrupadas al inicio del archivo: primero la biblioteca estándar, luego librerías externas y finalmente módulos del proyecto.

```python
# Correcto
from collections import deque
from typing import Any
```

Evitar:

```python
# Incorrecto
import os, sys
```

## 6. Comentarios

Los comentarios explican **por qué** se hace algo, no repiten lo que el código ya dice.

```python
# Correcto: explica la intención
# Se recorre de atrás hacia adelante para respetar el orden LIFO.
for indice in range(len(self._elementos) - 1, -1, -1):
    print(self._elementos[indice])
```

## 7. Docstrings (PEP 257)

Toda clase y función pública debe tener un docstring. Se escribe con triple comilla doble.

```python
class Pila:
    """Estructura LIFO (last in, first out)."""

    def desapilar(self):
        """Quita y retorna el último elemento agregado.

        Returns:
            El elemento que estaba en la cima.

        Raises:
            PilaVaciaError: Si la pila no tiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía")
        return self._elementos.pop()
```

## 8. Comparaciones y valores booleanos

No comparar explícitamente contra `True`, `False` o `None` con `==`.

```python
# Correcto
if not self.esta_vacia():
    ...

if nodo is None:
    ...
```

## 9. Manejo de errores

Usar excepciones específicas en lugar de `except:` o de devolver códigos ambiguos.

```python
class PilaVaciaError(Exception):
    """Se lanza cuando se intenta operar sobre una pila vacía."""


# Correcto
if self.esta_vacia():
    raise PilaVaciaError("No se puede desapilar una pila vacía")
```

## 10. Bloque principal

El código de prueba debe ir dentro de `if __name__ == "__main__":` para que el módulo pueda importarse sin ejecutarse.

```python
if __name__ == "__main__":
    pila = Pila()
    pila.apilar(10)
    print(pila.desapilar())
```

## Antes y después

### Antes

```python
class pila:
 def __init__(s):
  s.l=[]
 def apilar(s,x):
  s.l.append(x)
 def desapilar(s):
  return s.l.pop()
```

Problemas: nombre de clase en minúscula, variables sin significado, indentación de 1 espacio, sin docstrings, sin validaciones.

### Después

```python
class Pila:
    """Estructura LIFO implementada sobre una lista."""

    def __init__(self):
        self._elementos = []

    def apilar(self, elemento):
        """Agrega un elemento en la cima de la pila."""
        self._elementos.append(elemento)

    def desapilar(self):
        """Quita y retorna el elemento de la cima."""
        if not self._elementos:
            raise PilaVaciaError("La pila está vacía")
        return self._elementos.pop()
```

## Herramientas recomendadas

- `pycodestyle` o `flake8`: detectan errores de estilo.
- `black`: formatea automáticamente el código.
- `pylint`: revisa estilo, errores y malas prácticas.
- `mypy`: revisa anotaciones de tipos.

## Referencias

- PEP 8: <https://peps.python.org/pep-0008/>
- PEP 257: <https://peps.python.org/pep-0257/>
