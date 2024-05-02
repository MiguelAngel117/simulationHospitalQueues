import math
import random
from models.Server import Server
from models.Patient import Patient
from models.WaitQueue import WaitQueue
from helpers.generateNames import generateNames

def simulation():
    activationQueue = WaitQueue()
    activationServer = Server("Modulo de Activación de Citas")
        
    paciente1 = createPatient(0,0)
    activationQueue.addPatient(paciente1)
    lastTime = addTimeToServer(activationServer, paciente1.arrivalTime, 0)
    
    paciente2 = createPatient(paciente1.arrivalTime, paciente1.intervalArrivalTime)
    activationQueue.addPatient(paciente2)
    lastTime = addTimeToServer(activationServer, paciente2.arrivalTime, lastTime)
    
    paciente3 = createPatient(paciente2.arrivalTime, paciente2.intervalArrivalTime)
    activationQueue.addPatient(paciente3)
    lastTime = addTimeToServer(activationServer, paciente3.arrivalTime, lastTime)
    

    timesServer = list(activationServer.times)
    patients = list(activationQueue.patients)
    for patient in patients:
        print('--------------PATIENTS------------------')
        print(patient.name)
        print(patient.arrivalTime)
        print(patient.ri)
        print(patient.intervalArrivalTime)
    
    for time in timesServer:
        print('--------------SERVER------------------')
        print(time.startTime)
        print(time.ri)
        print(time.exitTime)
        print(time.exitTimeTotal)
        
    

    
def createPatient(previousAT, previousIAT):
    first_name, second_name = generateNames()
    arrivalTime = previousAT + previousIAT
    ri = random.random()
    leftService = False if random.random() < 0.95 else True
    return Patient(first_name + ' ' + second_name, arrivalTime, ri, calculateIntervalTime(5, ri), leftService, 1)

def calculateIntervalTime(const, ri):
    return - math.log(1 - ri) / const

def addTimeToServer(server, ATPatient, previousETTotal):
    if(ATPatient == 0):
        startTime = 0
    else: 
        startTime = max(ATPatient, previousETTotal)
    ri = random.random()
    exitTime = calculateIntervalTime(6, ri)
    exitTimeTotal = exitTime + startTime
    server.addTime(startTime,ri,exitTime,exitTimeTotal)
    return exitTimeTotal

if __name__ == "__main__":
    simulation()
