import random
def generateNames():
    male_first_names = ['Juan', 'Pedro', 'Luis', 'Carlos', 'Alex', 'Andres', 'Miguel', 'Benito', 'José', 'Diego', 'Alejandro', 'Manuel', 'Fabian', 'Daniel']
    female_first_names = ['María', 'Ana', 'Sofía', 'Laura', 'Andrea', 'Luisa', 'Rogelia', 'Josefina', 'Danna', 'Magdalena', 'Lupe', 'Julia', 'Victoria' ]
    
    male_second_names = ['Ivan', 'Antonio', 'Angel', 'Javier', 'Diego', 'Jorge', 'Ricardo', 'Carlos' , 'Andres', 'Felipe' 'Antonio', 'Dario']
    female_second_names = ['Isabel', 'Gabriela', 'Valentina', 'Camila', 'Daniela', 'Lucía', 'Karina', 'Angela', 'Dora', 'Elena', 'Milena', 'Mariela']

    if random.choice(['male', 'female']) == 'male':
        first_name = random.choice(male_first_names)
        second_name = random.choice(male_second_names)
    else:
        first_name = random.choice(female_first_names)
        second_name = random.choice(female_second_names)
    
    return first_name + ' '+ second_name