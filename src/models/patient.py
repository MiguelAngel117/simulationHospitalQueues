from helpers.generateNames import generateNames
import numpy as np

class Patient:
    def __init__(self, arrival_time, service_rate):
        self.name = " ".join(generateNames())
        self.arrival_time = arrival_time
        self.service_time = self.generate_service_time(service_rate)
        self.start_time = None
        self.end_time = None

    def generate_service_time(self, rate):
        return np.random.exponential(1 / rate)
