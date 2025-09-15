""" Handles the patient-facing interface: collects inputs and passes them to the system. """

from mesa import Agent
import random

# Import correction: make sure the path is correct
from agents.Patient import patient


class UserInterfaceAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.agent_type = "UserInterfaceAgent"
        self.has_event_this_step = False
        self.charge = 0  # simulated workload
        self.etat = "Actif"

    def step(self):
        # simulation of registering new patients at regular intervals
        if self.model.schedule.time % 5 == 0:
            self.enregistrer_patient()

        # Possible update of its status
        self.charge = min(1.0, self.charge + random.uniform(0, 0.1))
        self.etat = "Actif" if self.charge < 0.8 else "Surchargé"
        self.has_event_this_step = True

    def enregistrer_patient(self):
        # Correction: use 'agents' in the plural
        existing_patients = [a for a in self.model.schedule.agents if isinstance(a, patient)]
        patient_id = len(existing_patients) + 1000
        categorie = random.choice(['Urgence', 'Consultation', 'Suivi', 'Hospitalisation'])

        # Create the patient agent
        nouveau_patient = patient(patient_id, self.model)
        nouveau_patient.categorie_patient = categorie
        nouveau_patient.patient_id = patient_id
        nouveau_patient.etat = "en_attente"
        nouveau_patient.has_event_this_step = True

        # Add to the grid and the planner
        self.model.schedule.add(nouveau_patient)
        x, y = self.random.randrange(self.model.grid.width), self.random.randrange(self.model.grid.height)
        self.model.grid.place_agent(nouveau_patient, (x, y))

        # Recording of the event
        print(f"UserInterfaceAgent → New patient created: ID={patient_id}, Category={categorie}")
