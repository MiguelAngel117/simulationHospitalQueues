import queue
import threading
import time
import numpy as np
import tkinter as tk
from tkinter import ttk
from models.patient import Patient
from models.server import Server1, Server2, Server4
import sys

class PrintRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.configure(state=tk.NORMAL)
        self.textbox.insert(tk.END, text)
        self.textbox.configure(state=tk.DISABLED)
        self.textbox.see(tk.END)

def exp_time(rate):
    ri = np.random.random()
    return -(1 / rate) * np.log(1 - ri)

def simulate_hospital(n, arrival_rate, service_rate_1, service_rate_2, service_rate_3):
    queue_2 = queue.PriorityQueue()
    queue_3 = queue.PriorityQueue()
    global_clock = [0]
    
    patients = []
    arrival_time = 0
    for i in range(n):
        if i == 0:
            arrival_time = 0
        else:
            interarrival_time = exp_time(arrival_rate)
            arrival_time += interarrival_time
        patient = Patient(arrival_time, service_rate_1, service_rate_2, service_rate_3)
        patients.append(patient)
        
    server_1 = Server1(global_clock)
    server_2 = Server2(global_clock, 2)
    server_3 = Server2(global_clock, 3)
    server_4 = Server4(global_clock)
    
    server_1_thread = threading.Thread(target=server_1.process_patients, args=(patients, queue_2))
    server_1_thread.start()

    server_2_thread = threading.Thread(target=server_2.process_patients, args=(queue_2, queue_3))
    server_3_thread = threading.Thread(target=server_3.process_patients, args=(queue_2, queue_3))
    server_2_thread.start()
    server_3_thread.start()

    server_4_thread = threading.Thread(target=server_4.process_patients, args=(queue_3,))
    server_4_thread.start()
    
    server_1_thread.join()

    return server_1.log, server_2.log, server_3.log, server_4.log

def display_table(log, table):
    for row in table.get_children():
        table.delete(row)
    for row_id, log_entry in enumerate(log, start=1):
        table.insert("", "end", values=(row_id,) + log_entry)

def update_table():
    if current_server_log:
        display_table(current_server_log, table)
    root.after(1000, update_table)

def show_server_1():
    global current_server_log
    current_server_log = server_1_log

def show_server_2():
    global current_server_log
    current_server_log = server_2_log

def show_server_3():
    global current_server_log
    current_server_log = server_3_log

def show_server_4():
    global current_server_log
    current_server_log = server_4_log

def run_simulation():
    global server_1_log, server_2_log, server_3_log, server_4_log
    try:
        num_patients = int(entry_patients.get())
        server_1_log, server_2_log, server_3_log, server_4_log = simulate_hospital(
            num_patients, arrival_rate, service_rate_1, service_rate_2, service_rate_3
        )
    except ValueError:
        print("Error: El número de pacientes debe ser un entero.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def start_simulation():
    try:
        # Limpiar la tabla y las variables globales
        for row in table.get_children():
            table.delete(row)
        global server_1_log, server_2_log, server_3_log, server_4_log, current_server_log
        server_1_log, server_2_log, server_3_log, server_4_log = [], [], [], []
        current_server_log = []

        # Redirigir la salida estándar al textbox
        sys.stdout = PrintRedirector(message_box)

        # Iniciar la simulación en un hilo separado
        simulation_thread = threading.Thread(target=run_simulation)
        simulation_thread.start()
    except Exception as e:
        print(f"Error al iniciar la simulación: {e}")

if __name__ == "__main__":
    arrival_rate = 5  # tasa de llegada (lambda)
    service_rate_1 = 6  # tasa de servicio del primer servidor (miu)
    service_rate_2 = 2  # tasa de servicio de los segundos servidores (miu)
    service_rate_3 = 2  # tasa de servicio del cuarto servidor (miu)

    current_server_log = []

    # Crear la interfaz gráfica
    root = tk.Tk()
    root.title("Simulación del Hospital")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    lbl_patients = tk.Label(frame, text="Número de pacientes:")
    lbl_patients.pack(side="left")

    entry_patients = tk.Entry(frame)
    entry_patients.pack(side="left", padx=5)

    btn_start = tk.Button(frame, text="Iniciar", command=start_simulation)
    btn_start.pack(side="left", padx=5)

    table_frame = tk.Frame(root)
    table_frame.pack(pady=20)

    table = ttk.Treeview(table_frame, columns=("Paciente", "Llegada", "Inicio", "Fin"), show="headings")
    table.heading("Paciente", text="Paciente")
    table.heading("Llegada", text="Llegada")
    table.heading("Inicio", text="Inicio")
    table.heading("Fin", text="Fin")
    table.pack()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    btn_server_1 = tk.Button(button_frame, text="Servidor 1", command=show_server_1)
    btn_server_1.pack(side="left", padx=5)

    btn_server_2 = tk.Button(button_frame, text="Servidor 2", command=show_server_2)
    btn_server_2.pack(side="left", padx=5)

    btn_server_3 = tk.Button(button_frame, text="Servidor 3", command=show_server_3)
    btn_server_3.pack(side="left", padx=5)

    btn_server_4 = tk.Button(button_frame, text="Servidor 4", command=show_server_4)
    btn_server_4.pack(side="left", padx=5)

    # Crear un campo de texto para mostrar los mensajes
    message_box = tk.Text(root, height=30, width=160)
    message_box.pack()

    # Actualizar la tabla periódicamente
    root.after(1000, update_table)

    root.mainloop()
