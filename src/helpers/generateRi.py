import time
import math

class ReduceLinear:
    """Clase para la generación de números aleatorios con el método de congruencia lineal."""

    def __init__(self, quantity=None):
        """
        Constructor de la clase ReduceLinear.

        Parámetros:
        - quantity (int): Cantidad de números aleatorios a generar.
        """
        self.init_logical()
        self.list_ri = []
        if quantity is not None:
            self.generate_numbers_ri(quantity)

    def init_logical(self):
        """Inicializa las variables lógicas para la generación de números aleatorios."""
        self.seed = int(time.time() * 1000)  # Semilla basada en el tiempo en milisegundos
        self.a = 1664525  # Constante multiplicativa
        self.c = 7  # Constante aditiva
        self.m = int(math.pow(2, 32))  # Módulo, potencia de 2 de 32 bits

    def generate_numbers_ri(self, quantity):
        """
        Genera una cantidad especificada de números aleatorios.

        Parámetros:
        - quantity (int): Cantidad de números aleatorios a generar.
        """
        for _ in range(quantity):
            random_number = self.generate_ri()
            self.list_ri.append(random_number)

    def generate_ri(self):
        """
        Genera un número aleatorio utilizando el método de congruencia lineal.

        Retorna:
        - float: Número aleatorio normalizado entre 0 y 1.
        """
        self.seed = ((self.a * self.seed) + self.c) % self.m
        return self.seed / self.m

    def get_next_ri(self):
        """
        Obtiene el próximo número aleatorio de la lista generada.

        Retorna:
        - float or None: Próximo número aleatorio de la lista o None si la lista está vacía.
        """
        if self.list_ri:
            return self.list_ri.pop(0)
        else:
            return None