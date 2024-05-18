import random

def generateNames():
    first_names = ['Juan', 'María', 'Pedro', 'Ana', 'Luis', 'Sofía', 'Carlos', 'Laura', 'Alex', 'Andrea', 'Andres', 'Luisa', 'Luis', 'Rogelia', 'Benito', 'Josefina', 'José']
    second_names = ['Alejandro', 'Isabel', 'Antonio', 'Gabriela', 'Miguel', 'Valentina', 'Javier', 'Camila', 'Diego', 'Daniela', 'Felipe', 'Lucía', 'Karina', 'Pacheca', 'Ricardo']
    first_name = random.choice(first_names)
    second_name = random.choice(second_names)
    return first_name, second_name