"""Ejemplo de una pila implementada siguiendo PEP 8 y PEP 257.

Autor: Charles Jesus Morales Velasco
Titulo: Pila (stack) con buenas practicas de codificacion
Version: 1.0.0
Fecha: 2026
"""

from typing import Any


class PilaVaciaError(Exception):
    """Se lanza cuando se intenta operar sobre una pila vacia."""


class Pila:
    """Estructura de datos LIFO (last in, first out).

    El ultimo elemento en entrar es el primero en salir. Se implementa
    sobre una lista interna de Python.

    Attributes:
        _elementos: Lista que almacena los elementos de la pila.
    """

    def __init__(self) -> None:
        """Inicializa una pila vacia."""
        self._elementos: list[Any] = []

    def esta_vacia(self) -> bool:
        """Indica si la pila no tiene elementos.

        Returns:
            True si la pila esta vacia, False en caso contrario.
        """
        return len(self._elementos) == 0

    def apilar(self, elemento: Any) -> None:
        """Agrega un elemento en la cima de la pila.

        Args:
            elemento: Valor que se desea agregar. No puede ser None.
        """
        self._elementos.append(elemento)

    def desapilar(self) -> Any:
        """Quita y retorna el elemento que esta en la cima.

        Returns:
            El ultimo elemento agregado.

        Raises:
            PilaVaciaError: Si la pila no tiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar una pila vacia.")
        return self._elementos.pop()

    def cima(self) -> Any:
        """Retorna el elemento de la cima sin quitarlo.

        Returns:
            El ultimo elemento agregado.

        Raises:
            PilaVaciaError: Si la pila no tiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("La pila esta vacia.")
        return self._elementos[-1]

    def tamano(self) -> int:
        """Retorna la cantidad de elementos de la pila."""
        return len(self._elementos)

    def __len__(self) -> int:
        """Permite usar len(pila)."""
        return self.tamano()

    def __str__(self) -> str:
        """Retorna una representacion legible de la pila."""
        if self.esta_vacia():
            return "Pila([])"
        elementos = " <- ".join(str(elemento) for elemento in self._elementos)
        return f"Pila([{elementos}])"


def main() -> None:
    """Ejecuta una prueba rapida de la clase Pila."""
    pila = Pila()

    print("=== Prueba de la clase Pila ===")
    print(f"Esta vacia: {pila.esta_vacia()}")

    pila.apilar("A")
    pila.apilar("B")
    pila.apilar("C")

    print(f"Pila actual: {pila}")
    print(f"Cima: {pila.cima()}")
    print(f"Tamano: {len(pila)}")

    print(f"Desapilado: {pila.desapilar()}")
    print(f"Pila actual: {pila}")

    print("\n=== Prueba de pila vacia ===")
    pila.desapilar()
    pila.desapilar()

    try:
        pila.desapilar()
    except PilaVaciaError as error:
        print(f"Error esperado: {error}")


if __name__ == "__main__":
    main()
