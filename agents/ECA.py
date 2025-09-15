""" Handles communication with external partners and institutions. """

from mesa import Agent
import random

class ExternalCommunicationAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.agent_type = "ExternalCommunicationAgent"
        self.has_event_this_step = False
        self.charge = 0
        self.etat = "Actif"
        self.partenaires = ["CNAM", "Mutuelle privée", "Ministère de la Santé", "ONG santé", "pharmacy partenaire"]
        self.historique_requetes = []

    def step(self):
        # At certain time steps, simulate an exchange.
        if self.model.schedule.time % 6 == 0:
            self.envoyer_requete_externe()

        # Status Update
        self.charge = min(1.0, self.charge + random.uniform(0.01, 0.05))
        self.etat = "Actif" if self.charge < 0.85 else "Occupé"
        self.has_event_this_step = True

    def envoyer_requete_externe(self):
        partenaire = random.choice(self.partenaires)
        type_requete = random.choice([
            "Validation de prise en charge",
            "Transmission de rapport",
            "Demande de remboursement",
            "Signalement d’anomalie",
            "Mise à jour des droits"
        ])
        delai = random.randint(1, 3)  # Simulated response time

        self.historique_requetes.append({
            "step": self.model.schedule.time,
            "partenaire": partenaire,
            "type": type_requete,
            "delai": delai
        })

        print(f"ExternalCommunicationAgent → request to {partenaire} : '{type_requete}' (expected response by {delai} steps)")

