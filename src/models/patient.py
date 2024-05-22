from helpers.generateNames import generateNames
import numpy as np

class Patient:
    def __init__(self, arrival_time, rate1, rate2, rate3):
        self.name = generateNames()
        self.arrival_time = arrival_time
        self.service_time1 = self.generate_service_time(rate1)
        self.service_time2 = self.generate_service_time(rate2)
        self.service_time3 = self.generate_service_time(rate3)
        self.start_time = None
        self.end_time = None
        self.waiting_time = 0 

    def generate_service_time(self, rate):
        ri = np.random.random()
        return -(1 / rate) * np.log(1 - ri)
