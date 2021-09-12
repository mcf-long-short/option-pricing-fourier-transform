import math
import numpy as np
from scipy.integrate import quad

from .base import OptionPricingModel


class MertonFourierTransformPricing(OptionPricingModel):

    @staticmethod
    def merton_integration_function(u, S, K, T, r, sigma, lamb, mu, delta):
        """ 
        Valuation of European call option in M76 model via Lewis (2001)
        Fourier-based approach: integration function.
        """
        JDCF = MertonFourierTransformPricing.merton_characteristic_function(u - 0.5 * 1j, T, r, sigma, lamb, mu, delta)  # noqa
        value = 1 / (u ** 2 + 0.25) * (np.exp(1j * u * math.log(S / K)) * JDCF).real  # noqa
        return value

    @staticmethod
    def merton_characteristic_function(u, T, r, sigma, lamb, mu, delta):
        """
        Valuation of European call option in M76 model via Lewis (2001)
        Fourier-based approach: characteristic function.
        """
        omega = r - 0.5 * sigma ** 2 - lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)  # noqa
        value = np.exp((1j * u * omega - 0.5 * u ** 2 * sigma ** 2 + lamb * (np.exp(1j * u * mu - u ** 2 * delta ** 2 * 0.5) - 1)) * T)  # noqa
        return value


class MERTON_FT_NUM(MertonFourierTransformPricing):
    """Fourier option pricing - Lewis Approach (2001)

    Class implementing calculation for European option price using Forier Transform
    via Lewis Approach (numberical integration).

    Reference: Dr. Yves J. Hilpisch, Derivatives Analytics with Python
    """

    def _calculate_call_option_price(self, S, K, T, r, sigma, lamb, mu, delta):
        """ Valuation of European call option in Merton model via Lewis (2001)

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
        lamb: float
            jump intensity
        mu: float
            expected jump size
        delta: float
            standard deviation of jump

        Returns
        =======
        call_value: float
            European call option present value
        """

        int_value = quad(lambda u: self.merton_integration_function(u, S, K, T, r, sigma, lamb, mu, delta), 0, 50, limit=250)[0]  # noqa
        call_value = S - np.exp(-r * T) * math.sqrt(S * K) / math.pi * int_value  # noqa
        return call_value
