import numpy as np

def exp_time(rate, ri):
    """
    Calcula el tiempo de un evento según una distribución exponencial.

    Parámetros:
    - rate (float): Tasa de llegada de eventos (parámetro lambda o miu).
    - ri (float): Número aleatorio generado entre 0 y 1.

    Retorna:
    - float: Tiempo del próximo evento según la distribución exponencial.
    """
    return -(1 / rate) * np.log(1 - ri)
