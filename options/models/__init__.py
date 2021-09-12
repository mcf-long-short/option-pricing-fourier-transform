from .bsm import BSM
from .bsm_fourier import BSM_FT_NUM, BSM_FFT
from .merton_fourier import MERTON_FT_NUM, MERTON_FFT


def option_model_factory(model):
    """Returns instance of selected option pricing model"""
    if model == BSM.__name__:
        return BSM()
    elif model == BSM_FFT.__name__:
        return BSM_FFT()
    elif model == BSM_FT_NUM.__name__:
        return BSM_FT_NUM()
    elif model == MERTON_FT_NUM.__name__:
        return MERTON_FT_NUM()
    elif model == MERTON_FFT.__name__:
        return MERTON_FFT()
    else:
        raise Exception(
            "Wrong option pricing model. Specified model doesn't exist"
        )
