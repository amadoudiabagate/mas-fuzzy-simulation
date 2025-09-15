""" Lightweight container for patient attributes used by the model. """


from mesa import Agent

class patient(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.etat = "en_attente"

    def step(self):
        self.etat = "traité" if self.random.random() < 0.5 else "en_attente"
        print(f"patient {self.unique_id} is {self.etat}")
