from numpy.fft import fft
from scipy.integrate import quad
import numpy as np

from .base import OptionPricingModel


class ForierTransformPricing(OptionPricingModel):

    @staticmethod
    def BSM_integral_function(u, S0, K, T, r, sigma):
        """ 
        Valuation of European call option in BSM model via Lewis (2001)
        Fourier-based approach: integral function. 
        """
        cf_value = ForierTransformPricing.BSM_characteristic_function(u - 1j * 0.5, 0.0, T, r, sigma)  # noqa
        int_value = 1 / (u ** 2 + 0.25) * (np.exp(1j * u * np.log(S0 / K)) * cf_value).real  # noqa
        return int_value

    @staticmethod
    def BSM_characteristic_function(v, x0, T, r, sigma):
        """
        Valuation of European call option in BSM model via Lewis (2001) and Carr-Madan (1999)
        Fourier-based approach: charcteristic function. 
        """
        cf_value = np.exp(((x0 / T + r - 0.5 * sigma ** 2) * 1j * v - 0.5 * sigma ** 2 * v ** 2) * T)  # noqa
        return cf_value


class BSM_FT_NUM(ForierTransformPricing):
    """Fourier option pricing - Lewis Approach (2001)

    Class implementing calculation for European option price using Forier Transform
    via Lewis Approach (numberical integration).

    Reference: Dr. Yves J. Hilpisch, Derivatives Analytics with Python
    """

    def _calculate_call_option_price(self, S, K, T, r, sigma):
        """ Valuation of European call option in BSM model via Lewis (2001)

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
        int_value = quad(lambda u: self.BSM_integral_function(u, S, K, T, r, sigma), 0, 100)[0]  # noqa
        call_value = max(0, S - np.exp(-r * T) * np.sqrt(S * K) / np.pi * int_value)  # noqa
        return call_value


class BSM_FFT(ForierTransformPricing):
    """Fourier option pricing - Lewis Approach (2001)

    Class implementing calculation for European option price using Forier Transform
    via Lewis Approach (FFT - Fast Forier Transform).

    Reference: Dr. Yves J. Hilpisch, Derivatives Analytics with Python
    """

    def _calculate_call_option_price(self, S, K, T, r, sigma):
        ''' Valuation of European call option in BSM model via Lewis (2001)
        --> Fourier-based approach (integral).

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

        '''
        k = np.log(K / S)
        x0 = np.log(S / S)
        g = 1  # factor to increase accuracy
        N = g * 4096
        eps = (g * 150.) ** -1
        eta = 2 * np.pi / (N * eps)
        b = 0.5 * N * eps - k
        u = np.arange(1, N + 1, 1)
        vo = eta * (u - 1)
        # Modificatons to Ensure int_valueegrability
        if S >= 0.95 * K:  # ITM case
            alpha = 1.5
            v = vo - (alpha + 1) * 1j
            modcharFunc = np.exp(-r * T) * (self.BSM_characteristic_function(
                v, x0, T, r, sigma) /
                (alpha ** 2 + alpha
                 - vo ** 2 + 1j * (2 * alpha + 1) * vo))
        else:        # OTM case
            alpha = 1.1
            v = (vo - 1j * alpha) - 1j
            modcharFunc1 = np.exp(-r * T) * (1 / (1 + 1j * (vo - 1j * alpha))
                                             - np.exp(r * T) /
                                             (1j * (vo - 1j * alpha))
                                             - self.BSM_characteristic_function(
                v, x0, T, r, sigma) /
                ((vo - 1j * alpha) ** 2
                 - 1j * (vo - 1j * alpha)))
            v = (vo + 1j * alpha) - 1j
            modcharFunc2 = np.exp(-r * T) * (1 / (1 + 1j * (vo + 1j * alpha))
                                             - np.exp(r * T) /
                                             (1j * (vo + 1j * alpha))
                                             - self.BSM_characteristic_function(
                v, x0, T, r, sigma) /
                ((vo + 1j * alpha) ** 2
                 - 1j * (vo + 1j * alpha)))
        # Numerical FFT Routine
        delt = np.zeros(N, dtype=np.float)
        delt[0] = 1
        j = np.arange(1, N + 1, 1)
        SimpsonW = (3 + (-1) ** j - delt) / 3
        if S >= 0.95 * K:
            FFTFunc = np.exp(1j * b * vo) * modcharFunc * eta * SimpsonW
            payoff = (fft(FFTFunc)).real
            CallValueM = np.exp(-alpha * k) / np.pi * payoff
        else:
            FFTFunc = (np.exp(1j * b * vo)
                       * (modcharFunc1 - modcharFunc2)
                       * 0.5 * eta * SimpsonW)
            payoff = (fft(FFTFunc)).real
            CallValueM = payoff / (np.sinh(alpha * k) * np.pi)
        pos = int((k + b) / eps)
        CallValue = CallValueM[pos] * S
        # klist = np.exp((np.arange(0, N, 1) - 1) * eps - b) * S0
        return CallValue  # , klist[pos - 50:pos + 50]
