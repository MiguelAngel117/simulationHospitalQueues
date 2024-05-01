class WaitQueue:
    def __init__(self):
        self.patients = []
        
    def addPatient(self, patient):
        self.patients.append(patient)

    def movePatient(self, indexPatient, otherQueue):
        patient = self.patients.pop(indexPatient)
        otherQueue.addPatient(patient)