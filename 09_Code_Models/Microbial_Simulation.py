import numpy as np

class MicrobialHypercycleSimulation:
    """
    Minimal ecological hypercycle model:
    - P: plant biomass
    - M: microbial biomass
    - N: available nutrients
    """

    def __init__(self, p0=1.0, m0=0.5, n0=1.0):
        self.P = p0
        self.M = m0
        self.N = n0

    def step(self, dt=0.1,
             plant_growth_rate=0.5,
             micro_growth_rate=0.7,
             nutrient_recycling_rate=0.6,
             external_input=0.0):
        # Plant growth depends on nutrients and microbial facilitation
        plant_growth = plant_growth_rate * self.P * (self.N / (1.0 + self.N)) * (1.0 + 0.3 * self.M)
        # Microbial growth depends on plant exudates (proportional to P)
        micro_growth = micro_growth_rate * self.M * (self.P / (1.0 + self.P))
        # Nutrient recycling from microbial activity
        nutrient_recycling = nutrient_recycling_rate * self.M

        # Update
        self.P += dt * plant_growth
        self.M += dt * micro_growth
        self.N += dt * (nutrient_recycling + external_input - plant_growth * 0.4)

        # Avoid negatives
        self.P = max(self.P, 0.0)
        self.M = max(self.M, 0.0)
        self.N = max(self.N, 0.0)

        return self.P, self.M, self.N

    def run(self, steps=100, dt=0.1, **kwargs):
        history = {"P": [], "M": [], "N": []}
        for _ in range(steps):
            P, M, N = self.step(dt=dt, **kwargs)
            history["P"].append(P)
            history["M"].append(M)
            history["N"].append(N)
        return history
