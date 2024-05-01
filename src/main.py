from models.Server import Server
from models.Patient import Patient
from models.Doctor import Doctor
from models.WaitQueue import WaitQueue

def simulation():
    sala_espera = WaitQueue()
    sala_consulta = WaitQueue()
    medicos = [Doctor("Dr. García", "Pediatra"), Doctor("Dra. López", "Cardióloga")]

    # Simular llegada de pacientes y asignación de médicos
    paciente1 = Patient("Juan", "Fiebre", 2)
    paciente2 = Patient("María", "Dolor de cabeza", 1)

    sala_espera.addPatient(paciente1)
    sala_espera.addPatient(paciente2)
    pacientes_en_espera = list(sala_espera.patients)

    for paciente in pacientes_en_espera:
        print(paciente.name)
        for medico in medicos:
            if medico.available:
                sala_espera.movePatient(sala_espera.patients.index(paciente), sala_consulta)
                medico.available = False
                print(paciente.name + medico.nameDoctor)
                break
            
        

    # Simular consulta y liberación de médicos
    for paciente in sala_consulta.patients:
        for medico in medicos:
            if medico.nameDoctor == "Dr. García":  # Simular consulta solo con Dr. García
                medico.available = True
                
                sala_consulta.movePatient(sala_consulta.patients.index(paciente), sala_espera)

    print("Simulación completa.")

if __name__ == "__main__":
    simulation()
