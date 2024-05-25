import time
from helpers.expTime import exp_time

# Clase para el servicio de activación
class ActivationService:
    def __init__(self, global_clock, rate):
        """
            Constructor de la clase ActivationService.

            Parámetros:
            - global_clock: Reloj global para sincronización.
            - rate: Tasa de servicio.
        """
        self.global_clock = global_clock  # Reloj global para sincronización
        self.log = []  # Registro de eventos
        self.free_time = 0  # Tiempo libre para empezar a atender
        self.rate = rate  # Tasa de servicio

    def process_patients(self, patients, queue_2, listRi):
        """
            Procesa la llegada y atención de pacientes en el servicio de activación.

            Parámetros:
            - patients: Lista de pacientes que llegan al servicio.
            - queue_2: Cola de espera para el siguiente servicio.
            - listRi: Lista de números aleatorios para cálculos.

            Regresa:
            - None
        """
        for patient in patients:
            if patient.arrival_time >= self.free_time:
                patient.start_time = patient.arrival_time
            else:
                patient.start_time = self.free_time
                patient.waiting_time = patient.start_time - patient.arrival_time  # Calcula tiempo de espera
            service_time = exp_time(self.rate, listRi.get_next_ri())  # Calcula tiempo de servicio
            patient.end_time = patient.start_time + service_time
            self.free_time = patient.end_time  # Actualiza tiempo libre para siguiente paciente
            queue_2.put((patient.end_time, patient.name, patient))  # Pone paciente en la cola 2
            print(f"->{patient.name} llega a la cola 1 a las {patient.arrival_time:.3f}, es atendido: {patient.start_time:.3f} y termina a las {patient.end_time:.3f}, tiempo servicio {service_time:.3f}, tiempo espera {patient.waiting_time:.3f}\n")
            self.log.append((patient.name, patient.arrival_time, patient.start_time, service_time, patient.end_time, patient.waiting_time))  # Registra evento
            self.global_clock[0] = max(self.global_clock[0], patient.end_time)  # Actualiza reloj global
            time.sleep(service_time * 10)  # Simula tiempo de servicio

# Clase para el servicio de atención
class AttentionService:
    def __init__(self, global_clock, server_id, rate):
        """
            Constructor de la clase AttentionService.

            Parámetros:
            - global_clock: Reloj global para sincronización.
            - server_id: Identificador del servidor.
            - rate: Tasa de servicio.
        """
        self.global_clock = global_clock  # Reloj global para sincronización
        self.log = []  # Registro de eventos
        self.free_time = 0  # Tiempo libre para empezar a atender
        self.rate = rate  # Tasa de servicio
        self.server_id = server_id  # Identificador del servidor

    def process_patients(self, queue_2, queue_3, listRi):
        """
            Procesa la atención de pacientes en el servicio de atención.

            Parámetros:
            - queue_2: Cola de espera para el servicio de atención.
            - queue_3: Cola de espera para el servicio de medicamentos.
            - listRi: Lista de números aleatorios para cálculos.

            Regresa:
            - None
        """
        while True:
            end_time_1, patient_name, patient = queue_2.get()  # Obtiene paciente de la cola 2
            start_time_2 = max(self.free_time, end_time_1)  # Calcula tiempo de inicio de servicio
            service_time = exp_time(self.rate, listRi.get_next_ri())  # Calcula tiempo de servicio
            end_time_2 = start_time_2 + service_time  # Calcula tiempo de finalización de servicio
            self.free_time = end_time_2  # Actualiza tiempo libre para siguiente paciente
            patient.total_time = end_time_2  # Actualiza tiempo total de servicio para el paciente
            waiting_time_2 = start_time_2 - end_time_1  # Calcula tiempo de espera en la cola 2
            print(f"-->{patient_name} llega a la cola 2 a las {end_time_1:.3f}, es atendido por el servidor {self.server_id} a las {start_time_2:.3f} y termina a las {end_time_2:.3f}, tiempo servicio {service_time:.3f}\n")
            if listRi.get_next_ri() < 0.70:  # Simula necesidad de medicamentos
                queue_3.put((end_time_2, patient_name, patient))
                print(f"#{patient_name} del servidor {self.server_id} necesita medicamentos y se dirige a la cola 3 a las {end_time_2:.3f}\n")
            self.log.append((patient_name, end_time_1, start_time_2, service_time, end_time_2, waiting_time_2))  # Registra evento
            self.global_clock[0] = max(self.global_clock[0], end_time_2)  # Actualiza reloj global
            time.sleep(service_time * 10)  # Simula tiempo de servicio

# Clase para el servicio de medicamentos
class DrugService:
    def __init__(self, global_clock, rate):
        """
            Constructor de la clase DrugService.

            Parámetros:
            - global_clock: Reloj global para sincronización.
            - rate: Tasa de servicio.
        """
        self.global_clock = global_clock  # Reloj global para sincronización
        self.log = []  # Registro de eventos
        self.free_time = 0  # Tiempo libre para empezar a atender
        self.rate = rate  # Tasa de servicio

    def process_patients(self, queue_3, listRi):
        """
            Procesa la atención de pacientes en el servicio de medicamentos.

            Parámetros:
            - queue_3: Cola de espera para el servicio de medicamentos.
            - listRi: Lista de números aleatorios para cálculos.

            Regresa:
            - None
        """
        while True:
            end_time_2, patient_name, patient = queue_3.get()  # Obtiene paciente de la cola 3
            start_time_3 = max(self.free_time, end_time_2)  # Calcula tiempo de inicio de servicio
            service_time = exp_time(self.rate, listRi.get_next_ri())  # Calcula tiempo de servicio
            end_time_3 = start_time_3 + service_time  # Calcula tiempo de finalización de servicio
            patient.total_time = end_time_3  # Actualiza tiempo total de servicio para el paciente
            self.free_time = end_time_3  # Actualiza tiempo libre para siguiente paciente
            waiting_time_3 = start_time_3 - end_time_2  # Calcula tiempo de espera en la cola 3
            print(f"--->{patient_name} llega a la cola 3 a las {end_time_2:.3f}, es atendido por el servidor 4 a las {start_time_3:.3f} y termina a las {end_time_3:.3f}, tiempo servicio {service_time:.3f}\n")
            self.log.append((patient_name, end_time_2, start_time_3, service_time, end_time_3, waiting_time_3))  # Registra evento
            self.global_clock[0] = max(self.global_clock[0], end_time_3)  # Actualiza reloj global
            time.sleep(service_time * 10)  # Simula tiempo de servicio
