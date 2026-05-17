import numpy as np

class PriceStabilityModel:
    """
    Simple model linking supply stability (via MBT55) to price volatility.
    """

    def __init__(self, base_sigma: float):
        self.base_sigma = base_sigma

    def supply_stability(self, yield_cv_before: float, yield_cv_after: float) -> float:
        """
        Coefficient of variation (CV) of yield.
        """
        if yield_cv_before == 0:
            return 0.0
        return 1.0 - (yield_cv_after / yield_cv_before)

    def price_sigma(self, stability: float) -> float:
        """
        Higher stability → lower sigma.
        """
        factor = 1.0 - 0.7 * stability
        return max(self.base_sigma * factor, 0.01)
