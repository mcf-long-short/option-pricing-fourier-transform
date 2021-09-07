from enum import Enum
from options import models

from .models import option_model_factory


class Option:
    def __init__(self, S, K, T, r, sigma):
        """Creates option instance

        Parameters
        ==========
        S: float
            initial stock/index level
        K: float
            strike price
        T: float
            time-to-maturity (for t=0)
        r: float
            constant risk-free short rate
        sigma: float
            volatility factor in diffusion term
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def price(self, option_type, model):
        """Calculates call/put option theoretical price based on the selected pricing method."""
        pricing_model = option_model_factory(model=model)
        return pricing_model.price(option_type, self.S, self.K, self.T, self.r, self.sigma)
