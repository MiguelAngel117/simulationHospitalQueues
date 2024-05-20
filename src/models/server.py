import time
import random
import numpy as np

class Server1:
    def __init__(self, global_clock):
        self.global_clock = global_clock
        self.log = []
        self.free_time = 0

    def process_patients(self, patients, queue_2):
        for patient in patients:
            if patient.arrival_time >= self.free_time:
                patient.start_time = patient.arrival_time
            else:
                patient.start_time = self.free_time
            patient.end_time = patient.start_time + patient.service_time1
            self.free_time = patient.end_time
            queue_2.put((patient.end_time, patient.service_time2, patient.service_time2, patient.name))
            print(f"{patient.name} llega a la cola 1 a las {patient.arrival_time:.3f}, empieza a ser atendido a las {patient.start_time:.3f} y termina a las {patient.end_time:.3f}, tiempo servicio {patient.service_time1:.3f} \n")
            self.log.append((patient.name, patient.arrival_time, patient.start_time, patient.end_time))
            self.global_clock[0] = max(self.global_clock[0], patient.end_time)
            time.sleep(patient.service_time1 * 10)
    

class Server2:
    def __init__(self, global_clock, server_id):
        self.global_clock = global_clock
        self.log = []
        self.free_time = 0
        self.server_id = server_id

    def process_patients(self, queue_2, queue_3):
        while True:
            end_time_1, service_time2, service_time3, patient_name = queue_2.get()
            start_time_2 = max(self.free_time, end_time_1)
            end_time_2 = start_time_2 + service_time2
            self.free_time = end_time_2
            print(f"{patient_name} llega a la cola 2 a las {end_time_1:.3f}, empieza a ser atendido por el servidor {self.server_id} a las {start_time_2:.3f} y termina a las {end_time_2:.3f}, tiempo servicio {service_time2:.3f} \n")
            if random.random() < 0.25:
                queue_3.put((end_time_2, service_time3, patient_name))
                print(f"{patient_name} del servidor {self.server_id} necesita medicamentos y se dirige a la cola 3 a las {end_time_2:.3f} \n")
            self.log.append((patient_name, end_time_1, start_time_2, end_time_2))
            self.global_clock[0] = max(self.global_clock[0], end_time_2)
            time.sleep(service_time2 * 10)

class Server4:
    def __init__(self, global_clock):
        self.global_clock = global_clock
        self.log = []
        self.free_time = 0

    def process_patients(self, queue_3):
        while True:
            end_time_2, service_time ,patient_name = queue_3.get()
            start_time_3 = max(self.free_time, end_time_2)
            end_time_3 = start_time_3 + service_time
            self.free_time = end_time_3
            print(f"{patient_name} llega a la cola 3 a las {end_time_2:.3f}, empieza a ser atendido por el servidor 4 a las {start_time_3:.3f} y termina a las {end_time_3:.3f}, tiempo servicio {service_time:.3f} \n")
            self.log.append((patient_name, end_time_2, start_time_3, end_time_3))
            self.global_clock[0] = max(self.global_clock[0], end_time_3)
            time.sleep(service_time * 10)
