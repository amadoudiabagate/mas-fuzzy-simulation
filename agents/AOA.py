""" Admits patients and orients them to the right service or time slot. """

from mesa import Agent
import random

class AdmissionOrientationAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.agent_type = "AdmissionOrientationAgent"
        self.has_event_this_step = False
        self.charge = 0
        self.etat = "Actif"

        # Simulated list of services with simulated availability
        self.services = {
            "Consultation": 0.0,
            "Urgences": 0.0,
            "laboratory": 0.0,
            "Hospitalisation": 0.0
        }

    def step(self):
        # Find the waiting patients who have not yet been referred.
        patients = [a for a in self.model.schedule.agents
                    if 'patient' in type(a).__name__ and getattr(a, 'etat', '') == 'En waiting']

        for patient in patients:
            self.orienter_patient(patient)

        # Update status and load
        self.charge = min(1.0, self.charge + len(patients) * 0.05)
        self.etat = "Actif" if self.charge < 0.9 else "Occupé"
        self.has_event_this_step = True

    def orienter_patient(self, patient):
        # Selection of the available service (load < 0.8)
        service_disponible = [s for s, c in self.services.items() if c < 0.8]
        if not service_disponible:
            service = random.choice(list(self.services.keys()))
        else:
            service = random.choice(service_disponible)

        # Patient update
        patient.service_attribue = service
        patient.etat = "Orienté"

        # Initialization if necessary
        if not hasattr(patient, 'temps_attente'):
            patient.temps_attente = 0

        # Service load update
        self.services[service] += random.uniform(0.05, 0.15)
        self.services[service] = min(self.services[service], 1.0)

        print(f"AdmissionOrientationAgent → patient {patient.patient_id} orienté vers {service} (Charge {self.services[service]:.2f})")

