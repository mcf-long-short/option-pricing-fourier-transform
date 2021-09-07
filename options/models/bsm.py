import numpy as np
from scipy import stats

from .base import OptionPricingModel


class BSM(OptionPricingModel):
    """Black-Scholes-Merton Model(1973)

    Class implementing calculation for European option price using Black-Scholes Formula.
    It provides analytical formula for calculating option prce.
    """

    def _calculate_call_option_price(self, S, K, T, r, sigma):
        """ Valuation of European call option in BSM Model.

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

        Returns
        =======
        call_value: float
            European call option present value
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))  # noqa
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))  # noqa
        BS_C = (S * stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))    # noqa
        return BS_C
