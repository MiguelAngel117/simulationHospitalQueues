import queue
import threading
import numpy as np
from models.patient import Patient
from models.server import Server1, Server2, Server4

def exp_time(rate):
    return np.random.exponential(1 / rate)

def simulate_hospital(n, arrival_rate, service_rate_1, service_rate_2, service_rate_3):
    queue_2 = queue.PriorityQueue()
    queue_3 = queue.PriorityQueue()
    global_clock = [0]

    server_1 = Server1(service_rate_1, global_clock)
    server_2 = Server2(service_rate_2, global_clock, 2)
    server_3 = Server2(service_rate_2, global_clock, 3)
    server_4 = Server4(service_rate_3, global_clock)

    patients = []
    arrival_time = 0
    for i in range(n):
        if i == 0:
            arrival_time = 0
        else:
            interarrival_time = exp_time(arrival_rate)
            arrival_time += interarrival_time
        patient = Patient(arrival_time, service_rate_1)
        patients.append(patient)

    server_1_thread = threading.Thread(target=server_1.process_patients, args=(patients, queue_2))
    server_1_thread.start()

    server_2_thread = threading.Thread(target=server_2.process_patients, args=(queue_2, queue_3))
    server_3_thread = threading.Thread(target=server_3.process_patients, args=(queue_2, queue_3))
    server_2_thread.start()
    server_3_thread.start()

    server_4_thread = threading.Thread(target=server_4.process_patients, args=(queue_3,))
    server_4_thread.start()

    server_1_thread.join()

    print("\nResumen del Servidor 1:")
    for log in server_1.log:
        print(f"{log[0]} llegó a las {log[1]:.3f}, empezó a ser atendido a las {log[2]:.3f} y terminó a las {log[3]:.3f}")

    print("\nResumen del Servidor 2:")
    for log in server_2.log:
        print(f"{log[0]} llegó a las {log[1]:.3f}, empezó a ser atendido a las {log[2]:.3f} y terminó a las {log[3]:.3f}")

    print("\nResumen del Servidor 3:")
    for log in server_3.log:
        print(f"{log[0]} llegó a las {log[1]:.3f}, empezó a ser atendido a las {log[2]:.3f} y terminó a las {log[3]:.3f}")

    print("\nResumen del Servidor 4:")
    for log in server_4.log:
        print(f"{log[0]} llegó a las {log[1]:.3f}, empezó a ser atendido a las {log[2]:.3f} y terminó a las {log[3]:.3f}")

if __name__ == "__main__":
    n = int(input("Ingrese el número de pacientes: "))
    arrival_rate = 5  # tasa de llegada (lambda)
    service_rate_1 = 6  # tasa de servicio del primer servidor (miu)
    service_rate_2 = 2  # tasa de servicio de los segundos servidores (miu)
    service_rate_3 = 2  # tasa de servicio del cuarto servidor (miu)
    simulate_hospital(n, arrival_rate, service_rate_1, service_rate_2, service_rate_3)
