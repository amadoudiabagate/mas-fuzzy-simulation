# model.py
from agents import (
    AdmissionOrientationAgent,
    ExternalCommunicationAgent,
    LaboratoryRadiologyAgent,
    MedicalIntelligenceAgent,
    MedicalRecordAgent,
    MedicationProductManagementAgent,
    PatientSatisfactionEvaluationAgent,
    PlanningAgent,
    PrescriptionConsultationAgent,
    SecurityAccessAgent,
    ServiceCoordinationAgent,
    UserInterfaceAgent,
    patient
)

import os
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import pandas as pd
from datetime import datetime
import random

# Function to calculate average satisfaction
def satisfaction_mean(model):
    return model.total_satisfaction / model.num_steps if model.num_steps else 0

class CustomDataCollector:
    def __init__(self):
        self.records = []
        self.simulation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def collect(self, model):
        current_step = model.schedule.time
        for agent in model.schedule.agents:
            if hasattr(agent, 'has_event_this_step') and agent.has_event_this_step:
                record = {
                    "step": current_step,
                    "patient_id": getattr(agent, 'patient_id', getattr(agent, 'unique_id', 'N/A')),
                    "etat": getattr(agent, 'etat', 'Actif'),
                    "temps_attente": getattr(agent, 'temps_attente', 'N/A'),
                    "satisfaction": getattr(agent, 'satisfaction', 'N/A'),
                    "agent_id": getattr(agent, 'agent_id', getattr(agent, 'unique_id', 'N/A')),
                    "agent_type": getattr(agent, 'agent_type', type(agent).__name__),
                    "charge": getattr(agent, 'charge', 'N/A'),
                }
                self.records.append(record)
                agent.has_event_this_step = False

    def save(self, path):
        try:
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            if self.records:
                df = pd.DataFrame(self.records)
                df.sort_values(by=['step', 'agent_type', 'agent_id'], inplace=True)
                df.to_csv(path, index=False, encoding='utf-8', sep=',')
                print(f"✓ Fichier sauvegardé: {path} ({len(self.records)} enregistrements)")
                return True
            else:
                print("✗ Aucun enregistrement à sauvegarder")
                return False
        except Exception as e:
            print(f"✗ Erreur sauvegarde: {e}")
            return False

class CliniqueModel(Model):
    def __init__(self, width=10, height=10, num_agents=12):
        super().__init__()
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.total_satisfaction = 0.0
        self.num_steps = 0
        self.simulation_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.agent_classes = [
            patient,
            UserInterfaceAgent,
            PrescriptionConsultationAgent,
            MedicalRecordAgent,
            MedicationProductManagementAgent,
            LaboratoryRadiologyAgent,
            AdmissionOrientationAgent,
            ServiceCoordinationAgent,
            PatientSatisfactionEvaluationAgent,
            SecurityAccessAgent,
            MedicalIntelligenceAgent,
            ExternalCommunicationAgent,
            PlanningAgent
        ]

        for i in range(self.num_agents):
            agent_class = self.agent_classes[i % len(self.agent_classes)]
            agent = agent_class(i, self)

            # Initialization of attributes
            agent.agent_type = getattr(agent, 'agent_type', type(agent).__name__)
            agent.has_event_this_step = getattr(agent, 'has_event_this_step', False)
            agent.etat = getattr(agent, 'etat', 'Actif')
            agent.temps_attente = getattr(agent, 'temps_attente', 0)
            agent.satisfaction = getattr(agent, 'satisfaction', 0.5)
            agent.charge = getattr(agent, 'charge', 0)
            if 'patient' in type(agent).__name__.lower():
                agent.patient_id = getattr(agent, 'patient_id', agent.unique_id)
            agent.agent_id = getattr(agent, 'agent_id', agent.unique_id)

            self.schedule.add(agent)
            x, y = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"satisfaction_moyenne": satisfaction_mean},
            agent_reporters={
                "Type": lambda a: getattr(a, 'agent_type', 'Inconnu'),
                "satisfaction": lambda a: getattr(a, 'satisfaction', None),
                "Charge": lambda a: getattr(a, 'charge', None)
            }
        )
        self.custom_datacollector = CustomDataCollector()

    def step(self):
        self.num_steps += 1
        self._simulate_random_events()
        self.custom_datacollector.collect(self)
        self.schedule.step()
        self.datacollector.collect(self)

    def _simulate_random_events(self):
        for agent in self.schedule.agents:
            if random.random() < 0.3:
                agent.has_event_this_step = True
                if hasattr(agent, 'temps_attente'):
                    agent.temps_attente = max(0, agent.temps_attente + random.uniform(-0.5, 1.0))
                if hasattr(agent, 'satisfaction') and 'patient' in type(agent).__name__.lower():
                    agent.satisfaction = max(0, min(1, agent.satisfaction + random.uniform(-0.1, 0.1)))
                if hasattr(agent, 'charge') and 'patient' not in type(agent).__name__.lower():
                    agent.charge = max(0, min(1, agent.charge + random.uniform(-0.2, 0.2)))
                if random.random() < 0.2:
                    if 'patient' in type(agent).__name__.lower():
                        agent.etat = random.choice(['Abandon', 'En waiting', 'Pris en charge', 'Traité'])
                    else:
                        agent.etat = 'Actif' if agent.etat != 'Actif' else 'Occupé'

    def save_results(self):
        out_dir = os.path.join('outputs', 'data')
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(out_dir, f'resultats_simulation_{timestamp}.csv')
        success = self.custom_datacollector.save(filename)
        if success:
            df = pd.DataFrame(self.custom_datacollector.records)
            print(f" outcome(s) saved in {filename}")
            print(f" {len(df)} collected events")
            if not df.empty:
                print(f" Steps: from {df['step'].min()} to {df['step'].max()}")
                print(f"Types of agent: {df['agent_type'].value_counts().to_dict()}")
                print(f"\n Overview of the first lines:")
                print(df[['step', 'patient_id', 'etat', 'agent_type']].head(10).to_string())
            return filename
        else:
            print(" Backup failed")
            return None

if __name__ == "__main__":
    print("=== START OF THE SCRIPT ===")
    model = CliniqueModel(num_agents=12)
    print(f"✓ Model created with {len(model.schedule.agents)} agent")
    for i in range(50):
        model.step()
        if (i+1) % 10 == 0:
            print(f"step {i+1}/50 finished - Events: {len(model.custom_datacollector.records)}")
    print("\n=== SAFEGUARDING OF outcome(s) ===")
    model.save_results()
    print("\n=== simulation COMPLETED ===")
    input("Press Enter to close...")
