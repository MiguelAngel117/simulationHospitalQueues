import time
import math

# Clase para la generación de números aleatorios con el metodo de congruencia lineal
class ReduceLinear:
    def __init__(self, quantity=None):
        self.init_logical()
        self.list_ri = []
        if quantity is not None:
            self.generate_numbers_ri(quantity)  # Genera la cantidad especificada de números aleatorios

    def init_logical(self):
        self.seed = int(time.time() * 1000)  # Inicializa la semilla con el tiempo actual en milisegundos
        self.a = 1664525  # Constante multiplicativa
        self.c = 7  # Constante aditiva
        self.m = int(math.pow(2, 32))  # Módulo, potencia de 2 de 32 bits

    def generate_numbers_ri(self, quantity):
        for _ in range(quantity):
            random_number = self.generate_ri()  # Genera un número aleatorio
            self.list_ri.append(random_number)  # Agrega el número a la lista de números aleatorios

    def generate_ri(self):
        self.seed = ((self.a * self.seed) + self.c) % self.m  # Calcula el próximo valor de la semilla
        return self.seed / self.m  # Retorna el número aleatorio normalizado entre 0 y 1

    def get_next_ri(self):
        if self.list_ri:
            return self.list_ri.pop(0)  # Obtiene y elimina el próximo número aleatorio de la lista
        else:
            return None
