import math
import random
from models.Server import Server
from models.Patient import Patient
from models.WaitQueue import WaitQueue
from helpers.generateNames import generateNames

class Simulation:
    def __init__(self, numpatients):
        self.activationQueue = WaitQueue()
        self.simulation(numpatients)
        

    def simulation(self, numpatients): 
        activationServer = Server("Modulo de Activación de Citas")
        lastTime = 0
        for i in range(numpatients):
            if(i == 0):
                patient = self.createPatient(0,0)
                self.activationQueue.addPatient(patient)
                lastTime = self.addTimeToServer(activationServer, patient.arrivalTime, 0)
            else:
                previousPatient = self.activationQueue.patients[-1]
                patient = self.createPatient(previousPatient.arrivalTime, previousPatient.intervalArrivalTime)
                self.activationQueue.addPatient(patient)
                lastTime = self.addTimeToServer(activationServer, patient.arrivalTime, lastTime)
        
        
        timesServer = list(activationServer.times)
        patients = list(self.activationQueue.patients)
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
            
    def createPatient(self, previousAT, previousIAT): 
        first_name, second_name = generateNames()
        arrivalTime = previousAT + previousIAT
        ri = random.random()
        return Patient(first_name + ' ' + second_name, arrivalTime, ri, self.calculateIntervalTime(5, ri)) 

    def calculateIntervalTime(self, const, ri):
        return -math.log(1 - ri) / const

    def addTimeToServer(self, server, ATPatient, previousETTotal):  
        if ATPatient == 0:  
            startTime = 0
        else: 
            startTime = max(ATPatient, previousETTotal)
        ri = random.random()
        exitTime = self.calculateIntervalTime(6, ri)  
        exitTimeTotal = exitTime + startTime
        server.addTime(startTime, ri, exitTime, exitTimeTotal)
        return exitTimeTotal

if __name__ == "__main__":
    print('Ingrese el numero de pacientes')
    num = int(input())
    Simulation(num)
