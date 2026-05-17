import numpy as np

class SoilCarbonModel:
    """
    Simple SOC model with:
    - plant input
    - microbial necromass
    - decomposition
    """

    def __init__(self, soc_initial_tC_per_ha: float):
        self.soc = soc_initial_tC_per_ha

    def step(self,
             plant_input_tC_per_ha: float,
             mbt_factor: float = 1.0,
             decomposition_rate: float = 0.02):
        """
        mbt_factor > 1.0 increases necromass formation and stabilization.
        """
        necromass = plant_input_tC_per_ha * 0.3 * mbt_factor
        loss = self.soc * decomposition_rate / mbt_factor
        self.soc += necromass - loss
        return self.soc

    def run(self, years: int, plant_input_series, mbt_factor_series):
        history = []
        for t in range(years):
            soc_val = self.step(
                plant_input_tC_per_ha=plant_input_series[t],
                mbt_factor=mbt_factor_series[t]
            )
            history.append(soc_val)
        return history
