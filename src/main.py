import math
import random
from models.Server import Server
from models.Patient import Patient
from models.Doctor import Doctor
from models.WaitQueue import WaitQueue
from helpers.generateNames import generateNames

def simulation():
    activationservice = WaitQueue()
    attentionservice = WaitQueue()
    medicos = [Doctor("Dr. García", "Pediatra"), Doctor("Dra. López", "Cardiólogo")]
    activationServer = Server("Modulo de Activación de Citas", 0, 0, 0)
    
    attentionServers = [Server("Modulo 1 - Atención", 0, 0, 0,0), 
                        Server("Modulo 2 - Atención", 0, 0, 0,0), 
                        Server("Modulo 3 - Atención", 0, 0, 0,0), 
                        Server("Modulo 4 - Atención", 0, 0, 0,0)]
    
    
    paciente1 = createPatient(0)
    paciente2 = createPatient(paciente1.intervalArrivalTime)

    activationservice.addPatient(paciente1)
    activationservice.addPatient(paciente2)
    pacientes_en_espera = list(activationservice.patients)

    for paciente in pacientes_en_espera:
        print(paciente.name)
        print(paciente.arrivalTime )
        print(paciente.ri)
        print(paciente.intervalArrivalTime)
        print(paciente.leftService)
        
        for medico in medicos:
            if medico.available:
                activationservice.movePatient(activationservice.patients.index(paciente), attentionservice)
                medico.available = False
                print(paciente.name + medico.nameDoctor)
                break
            
    # Simular consulta y liberación de médicos
    for paciente in attentionservice.patients:
        for medico in medicos:
            if medico.nameDoctor == "Dr. García":  # Simular consulta solo con Dr. García
                medico.available = True
                
                attentionservice.movePatient(attentionservice.patients.index(paciente), activationservice)

    print("Simulación completa.")
    
def createPatient(previousIAT):
    first_name, second_name = generateNames()
    ri = random.random()
    leftService = False if random.random() < 0.95 else True
    return Patient(first_name + ' ' + second_name, previousIAT, ri, calculateIntervalTime(6, ri), leftService, 1)

def calculateIntervalTime(num, ri):
    return - math.log(1 - ri) / num

if __name__ == "__main__":
    simulation()
