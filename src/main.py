from models.server import Server1, Server2, Server4
from helpers.generateRi import ReduceLinear
from helpers.expTime import exp_time
from models.patient import Patient
from tkinter import ttk
import tkinter as tk
import threading
import queue
import sys
import matplotlib.pyplot as plt

class PrintRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.configure(state=tk.NORMAL)
        self.textbox.insert(tk.END, text)
        self.textbox.configure(state=tk.DISABLED)
        self.textbox.see(tk.END)

def simulate_hospital(n, arrival_rate, service_rate_1, service_rate_2, service_rate_3, service_rate_4):
    queue_1 = []
    queue_2 = queue.PriorityQueue()
    queue_3 = queue.PriorityQueue()
    global_clock = [0]
    arrival_time = 0
    listRi = ReduceLinear(n * 5)
    for i in range(n):
        if i == 0:
            arrival_time = 0
        else:
            interarrival_time = exp_time(arrival_rate, listRi.get_next_ri())
            arrival_time += interarrival_time
        patient = Patient(arrival_time)
        queue_1.append(patient)
        
    server_1 = Server1(global_clock, service_rate_1)
    server_2 = Server2(global_clock, 2, service_rate_2)
    server_3 = Server2(global_clock, 3, service_rate_3)
    server_4 = Server4(global_clock, service_rate_4)
    
    server_1_thread = threading.Thread(target=server_1.process_patients, args=(queue_1, queue_2, listRi))
    server_1_thread.start()

    server_2_thread = threading.Thread(target=server_2.process_patients, args=(queue_2, queue_3, listRi))
    server_3_thread = threading.Thread(target=server_3.process_patients, args=(queue_2, queue_3, listRi))
    server_2_thread.start()
    server_3_thread.start()

    server_4_thread = threading.Thread(target=server_4.process_patients, args=(queue_3, listRi,))
    server_4_thread.start()
    
    server_1_thread.join()

    return server_1.log, server_2.log, server_3.log, server_4.log, queue_1

def display_table(log, table):
    for row in table.get_children():
        table.delete(row)
    if not log:
        table.insert("", "end", values=("0", "0", "0", "0", "0", "0", "0"))
    else:
        for row_id, log_entry in enumerate(log, start=1):
            formatted_log_entry = tuple(f"{value:.5f}" if isinstance(value, float) else value for value in log_entry)
            table.insert("", "end", values=(row_id,) + formatted_log_entry)

def update_table():
    if current_server_log is not None:
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
    global server_1_log, server_2_log, server_3_log, server_4_log, queue_1
    try:
        num_patients = int(entry_patients.get())
        server_1_log, server_2_log, server_3_log, server_4_log, queue_1 = simulate_hospital(
            num_patients, arrival_rate, service_rate_1, service_rate_2, service_rate_3, service_rate_4
        )
        
    except ValueError:
        print("Error: El número de pacientes debe ser un entero.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def start_simulation():
    try:
        for row in table.get_children():
            table.delete(row)
        global server_1_log, server_2_log, server_3_log, server_4_log, current_server_log
        server_1_log, server_2_log, server_3_log, server_4_log = [], [], [], []
        current_server_log = []

        sys.stdout = PrintRedirector(message_box)

        simulation_thread = threading.Thread(target=run_simulation)
        simulation_thread.start()
    except Exception as e:
        print(f"Error al iniciar la simulación: {e}")

def show_graph():
    patient_names = [patient.name for patient in queue_1]
    total_service_times = [patient.total_time - patient.arrival_time for patient in queue_1]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(patient_names, total_service_times, color='skyblue')
    ax.set_xlabel('Pacientes')
    ax.set_ylabel('Tiempo Total de Servicio')
    ax.set_title('Comparación del Tiempo Total de Servicio por Paciente')
    ax.set_xticklabels(patient_names, rotation=45, ha="right")

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    arrival_rate = 5
    service_rate_1 = 6
    service_rate_2 = 2
    service_rate_3 = 2
    service_rate_4 = 7

    current_server_log = None

    root = tk.Tk()
    root.title("Simulación del Hospital")
    root.configure(bg="#f0f0f0")

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=10)

    lbl_patients = tk.Label(frame, text="Número de pacientes:", bg="#f0f0f0")
    lbl_patients.pack(side="left")

    entry_patients = tk.Entry(frame)
    entry_patients.pack(side="left", padx=5)

    btn_start = tk.Button(frame, text="Iniciar", command=start_simulation, bg="#4caf50", fg="white")
    btn_start.pack(side="left", padx=5)

    table_frame = tk.Frame(root, bg="#f0f0f0")
    table_frame.pack(pady=5)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), foreground="#4caf50")
    style.configure("Treeview", font=("Helvetica", 10))

    table = ttk.Treeview(table_frame, columns=("ID", "Paciente", "Llegada", "Inicio", "Servicio", "Fin", "Espera"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Paciente", text="Paciente")
    table.heading("Llegada", text="Llegada")
    table.heading("Inicio", text="Inicio")
    table.heading("Servicio", text="Servicio")
    table.heading("Fin", text="Fin")
    table.heading("Espera", text="Espera")
    table.pack()

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    btn_server_1 = tk.Button(button_frame, text="Servidor 1", command=show_server_1, bg="#2196f3", fg="white")
    btn_server_1.pack(side="left", padx=5)

    btn_server_2 = tk.Button(button_frame, text="Servidor 2", command=show_server_2, bg="#2196f3", fg="white")
    btn_server_2.pack(side="left", padx=5)

    btn_server_3 = tk.Button(button_frame, text="Servidor 3", command=show_server_3, bg="#2196f3", fg="white")
    btn_server_3.pack(side="left", padx=5)

    btn_server_4 = tk.Button(button_frame, text="Servidor 4", command=show_server_4, bg="#2196f3", fg="white")
    btn_server_4.pack(side="left", padx=5)

    btn_show_graph = tk.Button(button_frame, text="Mostrar Gráfica", command=show_graph, bg="#f44336", fg="white")
    btn_show_graph.pack(side="left", padx=5)

    message_box = tk.Text(root, height=15, width=140, bg="#e8eaf6")
    message_box.pack(pady=10)

    root.after(1000, update_table)
    root.mainloop()
