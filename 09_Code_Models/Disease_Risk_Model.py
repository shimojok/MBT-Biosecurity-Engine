import numpy as np

class DiseaseRiskModel:
    """
    Simple disease risk model driven by:
    - baseline infection pressure
    - climate factors (humidity, temperature)
    - MBT55 coverage (priority effect + antagonism)
    """

    def __init__(self, baseline_risk: float):
        self.baseline_risk = baseline_risk  # 0–1

    def climate_factor(self, humidity: float, temperature: float) -> float:
        """
        humidity: 0–1
        temperature: °C
        """
        h_factor = np.clip(humidity, 0, 1)
        t_opt = 22.0
        t_sigma = 6.0
        t_factor = np.exp(-((temperature - t_opt) ** 2) / (2 * t_sigma ** 2))
        return 0.5 * h_factor + 0.5 * t_factor

    def mbt55_protection(self, coverage_pct: float, dose_factor: float = 1.0) -> float:
        """
        coverage_pct: 0–100
        dose_factor: 0.5–2.0 (relative)
        Returns protection factor 0–1 (1 = full protection)
        """
        c = np.clip(coverage_pct / 100.0, 0, 1)
        base = 1.0 - np.exp(-3.0 * c * dose_factor)
        return np.clip(base, 0, 1)

    def risk(self, humidity: float, temperature: float, coverage_pct: float) -> float:
        cf = self.climate_factor(humidity, temperature)
        prot = self.mbt55_protection(coverage_pct)
        risk = self.baseline_risk * cf * (1.0 - prot)
        return np.clip(risk, 0, 1)
