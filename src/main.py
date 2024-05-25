# importaciones
from models.server import ActivationService, AttentionService, DrugService
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
    """
    Simula el funcionamiento de un hospital con múltiples servidores de atención.
    Args:
        n (int): Número de pacientes a simular.
        arrival_rate (int): Tasa de llegada de pacientes.
        service_rate_1, service_rate_2, service_rate_3, service_rate_4 (int): Tasas de servicio de los servidores.
    Returns:
        tuple: Registros de los servidores y colas de pacientes.
    """
    queue_1 = []
    queue_2 = queue.PriorityQueue()
    queue_3 = queue.PriorityQueue() 
    global_clock = [0]  # Inicializa el reloj global
    arrival_time = 0  # Inicializa el tiempo de llegada
    listRi = ReduceLinear(n * 5)  # Inicializa la lista de números aleatorios para la distribución exponencial

    for i in range(n):  # Itera sobre el número de pacientes a simular
        if i == 0:  # Si es el primer paciente
            arrival_time = 0  # El tiempo de llegada es cero
        else:  
            arrival_time += interarrival_time # Actualiza el tiempo de llegada
        interarrival_time = exp_time(arrival_rate, listRi.get_next_ri()) # Calcula el tiempo entre llegadas
        patient = Patient(arrival_time, interarrival_time)
        queue_1.append(patient)  
    
    # Inicializa los servidores de atención con sus tasas de servicio respectivas
    server_1 = ActivationService(global_clock, service_rate_1)
    server_2 = AttentionService(global_clock, 2, service_rate_2)
    server_3 = AttentionService(global_clock, 3, service_rate_3)
    server_4 = DrugService(global_clock, service_rate_4)
    
    # Crea hilos para cada servidor y los inicia para procesar pacientes en paralelo
    server_1_thread = threading.Thread(target=server_1.process_patients, args=(queue_1, queue_2, listRi))
    server_1_thread.start()

    server_2_thread = threading.Thread(target=server_2.process_patients, args=(queue_2, queue_3, listRi))
    server_3_thread = threading.Thread(target=server_3.process_patients, args=(queue_2, queue_3, listRi))
    server_2_thread.start()
    server_3_thread.start()

    server_4_thread = threading.Thread(target=server_4.process_patients, args=(queue_3, listRi,))
    server_4_thread.start()

    server_1_thread.join()  # Espera a que el hilo del servidor 1 termine

    return server_1.log, server_2.log, server_3.log, server_4.log, queue_1

def display_table(log, table):
    """
    Muestra los registros de los servidores en una tabla de la interfaz gráfica.
    Args:
        log (list): Registros de los servidores.
        table (ttk.Treeview): Widget de tabla donde se mostrarán los registros.
    """
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
        num_patients = int(entry_patients.get()) # Obtiene el número de pacientes ingresado por el usuario 
        if(num_patients <= 0):  
            print("Ingrese un valor mayor a 0")
        # Llama a la función de simulación del hospital y asigna los resultados a variables globales
        server_1_log, server_2_log, server_3_log, server_4_log, queue_1 = simulate_hospital(
            num_patients, arrival_rate, service_rate_1, service_rate_2, service_rate_3, service_rate_4)
    except ValueError:
        print("El número de pacientes debe ser un entero.")  
    except Exception as e:
        print(f"Error inesperado: {e}")  

def start_simulation():
    try:
        for row in table.get_children():
            table.delete(row)  
        global server_1_log, server_2_log, server_3_log, server_4_log, current_server_log
        server_1_log, server_2_log, server_3_log, server_4_log = [], [], [], []  
        current_server_log = []
        queue_1 = []
        
        # Limpia el widget de texto antes de redirigir la salida
        message_box.configure(state=tk.NORMAL)
        message_box.delete(1.0, tk.END)
        message_box.configure(state=tk.DISABLED)
        
        sys.stdout = PrintRedirector(message_box)  # Redirige la salida estándar al widget de texto
        # Crea un hilo para ejecutar la simulación en segundo plano
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

def show_bar_chart():
    # Calcula los promedios de tiempos de atención por servidor y tiempo de llegadas al primer servidor
    avg_service_time_server_1 = sum(log_entry[3] for log_entry in server_1_log) / len(server_1_log) if server_1_log else 0
    avg_service_time_server_2 = sum(log_entry[3] for log_entry in server_2_log) / len(server_2_log) if server_2_log else 0
    avg_service_time_server_3 = sum(log_entry[3] for log_entry in server_3_log) / len(server_3_log) if server_3_log else 0
    avg_service_time_server_4 = sum(log_entry[3] for log_entry in server_4_log) / len(server_4_log) if server_4_log else 0
    avg_arrival_time_first_server = sum(patient.interarrival_time for patient in queue_1) / len(queue_1) if queue_1 else 0
    
    labels = ['IAT Servidor 1','Servidor 1', 'Servidor 2', 'Servidor 3', 'Servidor 4']
    values = [avg_arrival_time_first_server, avg_service_time_server_1, avg_service_time_server_2, avg_service_time_server_3,
              avg_service_time_server_4]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=['blue', 'orange', 'green', 'red', 'purple'])
    plt.xlabel('Promedio de Tiempos de servicio y llegada')
    plt.ylabel('Tiempo Promedio')
    plt.title('Promedio de Tiempos de Atención por Servidor y Tiempo entre llegadas 1er Servidor')
    plt.xticks(rotation=45, ha='right')

    # Agrega los valores encima de las barras
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, value, f'{value:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    arrival_rate = 10  # tasa de llegada (lambda) 5
    service_rate_1 = 6  # tasa de servicio del primer servidor (miu) 
    service_rate_2 = 4  # tasa de servicio del segundo servidor (miu)2
    service_rate_3 = 4  # tasa de servicio del tercer servidor (miu)2
    service_rate_4 = 6  # tasa de servicio del cuarto servidor (miu)7
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

    btn_frame = tk.Frame(root, bg="#f0f0f0")
    btn_frame.pack(pady=5)

    btn_server_1 = tk.Button(btn_frame, text="Servidor 1", command=show_server_1, bg="#2196f3", fg="white")
    btn_server_1.pack(side="left", padx=5)

    btn_server_2 = tk.Button(btn_frame, text="Servidor 2", command=show_server_2, bg="#2196f3", fg="white")
    btn_server_2.pack(side="left", padx=5)

    btn_server_3 = tk.Button(btn_frame, text="Servidor 3", command=show_server_3, bg="#2196f3", fg="white")
    btn_server_3.pack(side="left", padx=5)

    btn_server_4 = tk.Button(btn_frame, text="Servidor 4", command=show_server_4, bg="#2196f3", fg="white")
    btn_server_4.pack(side="left", padx=5)

    btn_graph = tk.Button(btn_frame, text="Tiempos Total servicio", command=show_graph, bg="#ff9800", fg="white")
    btn_graph.pack(side="left", padx=5)

    btn_scatter = tk.Button(btn_frame, text="Promedio tiempos", command=show_bar_chart, bg="#ff9800", fg="white")
    btn_scatter.pack(side="left", padx=5)

    message_box = tk.Text(root, height=10, width=140, state=tk.DISABLED)
    message_box.pack(pady=10)

    root.after(1000, update_table)
    root.mainloop()
