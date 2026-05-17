import numpy as np

class OneHealthModel:
    """
    Integrates:
    - livestock infection
    - antibiotic use
    - zoonotic risk proxy
    """

    def __init__(self,
                 infection_rate_before: float,
                 antibiotic_use_before_kg: float):
        self.infection_rate_before = infection_rate_before
        self.antibiotic_use_before = antibiotic_use_before_kg

    def mbt_effect(self, mbt_coverage: float) -> float:
        """
        mbt_coverage: 0–1
        """
        return np.clip(1.0 - 0.6 * mbt_coverage, 0.2, 1.0)

    def infection_after(self, mbt_coverage: float) -> float:
        factor = self.mbt_effect(mbt_coverage)
        return np.clip(self.infection_rate_before * factor, 0.0, 1.0)

    def antibiotic_after(self, mbt_coverage: float) -> float:
        factor = self.mbt_effect(mbt_coverage)
        return max(self.antibiotic_use_before * factor, 0.0)

    def zoonotic_risk_index(self, infection_rate: float, antibiotic_use_kg: float) -> float:
        """
        Simple proxy: higher infection + higher antibiotic → higher risk.
        """
        return np.clip(0.5 * infection_rate + 0.5 * (antibiotic_use_kg / (self.antibiotic_use_before + 1e-6)), 0.0, 1.0)
