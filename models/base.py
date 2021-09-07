from enum import Enum
from abc import ABC
from abc import abstractclassmethod

import numpy as np


class OPTION_TYPE(Enum):
    CALL_OPTION = 'call'
    PUT_OPTION = 'put'


class OptionPricingModel(ABC):
    """Abstract class defining interface for option pricing models."""

    def price(self, option_type, *args, **kwargs):
        """Calculates call/put option price according to the specified parameter."""
        if option_type == OPTION_TYPE.CALL_OPTION.value:
            return self._calculate_call_option_price(*args, **kwargs)
        elif option_type == OPTION_TYPE.PUT_OPTION.value:
            return self._calculate_put_option_price(*args, **kwargs)
        else:
            raise Exception("Wrong option type")

    @abstractclassmethod
    def _calculate_call_option_price(self, S, K, T, r, sigma):
        """Calculates option price for call option."""
        raise NotImplementedError()

    def _calculate_put_option_price(self, S, K, T, r, sigma):
        """
        Calculates option price for put option.
        Put option price is calculated from call price based on the Put-Call property.
        https://www.investopedia.com/terms/p/putcallparity.asp


        Formula:    C + PV(x) = P + S
        =============================
        C           price of the European call option
        PV(x)       the present value of the strike price (x),
        P           price of the European put
        S           spot price or the current market value of the underlying asset
        """
        c = self._calculate_call_option_price(S, K, T, r, sigma)
        pv_strike = np.exp(-r * T) * K
        put_price = c + pv_strike - S

        return put_price
