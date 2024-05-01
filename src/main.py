from models.Server import Server
from models.Patient import Patient
from models.Doctor import Doctor
from models.WaitQueue import WaitQueue

def simulation():
    activationservice = WaitQueue()
    attentionservice = WaitQueue()
    activationServer = Server("Modulo de Activación de Citas")
    
    attentionServers = [Server("Modulo 1 - Atención"), 
                        Server("Modulo 2 - Atención"), 
                        Server("Modulo 3 - Atención"), 
                        Server("Modulo 4 - Atención"), 
                        Server("Modulo 5 - Atención")]
    

    # Simular llegada de pacientes y asignación de médicos
    paciente1 = Patient("Juan", 2)
    paciente2 = Patient("María", 1)

    activationservice.addPatient(paciente1)
    activationservice.addPatient(paciente2)
    pacientes_en_espera = list(activationservice.patients)

    for paciente in pacientes_en_espera:
        print(paciente.name)
        for medico in medicos:
            if medico.available:
                activationservice.movePatient(activationservice.patients.index(paciente), attentionservice)
                medico.available = False
                print(paciente.name + medico.nameDoctor)
                break
            
        

    # Simular consulta y liberación de médicos
    for paciente in attentionservice.patients:
        for medico in medicos:
            if medico.nameDoctor == "Dr. García":  # Simular consulta solo con Dr. García
                medico.available = True
                
                attentionservice.movePatient(attentionservice.patients.index(paciente), activationservice)

    print("Simulación completa.")

if __name__ == "__main__":
    simulation()
