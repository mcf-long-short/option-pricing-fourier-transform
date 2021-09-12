import math
import numpy as np
from scipy.integrate import quad
from numpy.fft import fft

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
    def merton_characteristic_function(u, T, r, sigma, lamb, mu, delta, X0=0):
        """
        Valuation of European call option in M76 model via Lewis (2001)
        Fourier-based approach: characteristic function.
        """
        omega = X0 / T + r - 0.5 * sigma ** 2 - lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)  # noqa
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


class MERTON_FFT(MertonFourierTransformPricing):
    """Fourier option pricing - Carr-Madan approach (1999)

    Class implementing calculation for European option price using Forier Transform
    via Lewis Approach (FFT - Fast Fourier Transform).

    Reference: Dr. Yves J. Hilpisch, Derivatives Analytics with Python
    """

    def _calculate_call_option_price(self, S, K, T, r, sigma, lamb, mu, delta):
        """ Valuation of European call option in Merton model via Carr-Madan (1999)
        Fourier-based approach.

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
        k = math.log(K / S)
        x0 = math.log(S / S)
        g = 2  # factor to increase accuracy
        N = g * 4096
        eps = (g * 150.) ** -1
        eta = 2 * math.pi / (N * eps)
        b = 0.5 * N * eps - k
        u = np.arange(1, N + 1, 1)
        vo = eta * (u - 1)
        # Modificatons to Ensure Integrability
        if S >= 0.95 * K:  # ITM case
            alpha = 1.5
            v = vo - (alpha + 1) * 1j
            mod_char_fun = math.exp(-r * T) * self.merton_characteristic_function(
                v, T, r, sigma, lamb, mu, delta, x0) \
                / (alpha ** 2 + alpha - vo ** 2 + 1j * (2 * alpha + 1) * vo)
        else:  # OTM case
            alpha = 1.1
            v = (vo - 1j * alpha) - 1j
            mod_char_fun_1 = math.exp(-r * T) * (1 / (1 + 1j * (vo - 1j * alpha))
                                                 - math.exp(r * T) /
                                                 (1j * (vo - 1j * alpha))
                                                 - self.merton_characteristic_function(
                v, T, r, sigma, lamb, mu, delta, x0)
                / ((vo - 1j * alpha) ** 2 - 1j * (vo - 1j * alpha)))
            v = (vo + 1j * alpha) - 1j
            mod_char_fun_2 = math.exp(-r * T) * (1 / (1 + 1j * (vo + 1j * alpha))
                                                 - math.exp(r * T) /
                                                 (1j * (vo + 1j * alpha))
                                                 - self.merton_characteristic_function(
                v, T, r, sigma, lamb, mu, delta, x0)
                / ((vo + 1j * alpha) ** 2 - 1j * (vo + 1j * alpha)))

        # Numerical FFT Routine
        delt = np.zeros(N, dtype=float)
        delt[0] = 1
        j = np.arange(1, N + 1, 1)
        SimpsonW = (3 + (-1) ** j - delt) / 3
        if S >= 0.95 * K:
            fft_func = np.exp(1j * b * vo) * mod_char_fun * eta * SimpsonW
            payoff = (fft(fft_func)).real
            call_value_m = np.exp(-alpha * k) / math.pi * payoff
        else:
            fft_func = (np.exp(1j * b * vo)
                        * (mod_char_fun_1 - mod_char_fun_2)
                        * 0.5 * eta * SimpsonW)
            payoff = (fft(fft_func)).real
            call_value_m = payoff / (np.sinh(alpha * k) * math.pi)
        pos = int((k + b) / eps)
        call_value = call_value_m[pos]
        return call_value * S
