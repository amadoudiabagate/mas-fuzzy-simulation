""" Maintains electronic medical records and updates them safely. """

from mesa import Agent
import random

class MedicalRecordAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.agent_type = "MedicalRecordAgent"
        self.has_event_this_step = False
        self.charge = 0
        self.etat = "Actif"
        self.journal_audit = []

    def step(self):
        # Find patients who have recently been taken care of or treated
        patients_a_mettre_a_jour = [
            a for a in self.model.schedule.agents
            if 'patient' in type(a).__name__.lower() and getattr(a, 'etat', '') in ["Pris en charge", "Traité"]
        ]

        for patient in patients_a_mettre_a_jour:
            self.mettre_a_jour_dossier(patient)

        # Status update
        self.charge = min(1.0, self.charge + len(patients_a_mettre_a_jour) * 0.03)
        self.etat = "Actif" if self.charge < 0.85 else "Occupé"
        self.has_event_this_step = True

    def mettre_a_jour_dossier(self, patient):
        # Adding a simulated attribute 'medical_file'
        if not hasattr(patient, "dossier_medical"):
            patient.dossier_medical = []

        entree = {
            "step": self.model.schedule.time,
            "donnee": random.choice([
                "Consultation terminée",
                "outcome(s) labo ajouté",
                "Traitement prescrit",
                "Observation clinique ajoutée"
            ]),
            "confidentiel": True
        }

        patient.dossier_medical.append(entree)

        # Internal Audit Journal
        self.journal_audit.append({
            "patient_id": getattr(patient, 'patient_id', 'N/A'),
            "action": entree["donnee"],
            "step": self.model.schedule.time
        })

        print(f"MedicalRecordAgent → Patient file {getattr(patient, 'patient_id', 'N/A')} updated : {entree['donnee']}")
