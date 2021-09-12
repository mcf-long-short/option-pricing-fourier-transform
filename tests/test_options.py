import pytest
from options import Option


S = 100.00
K = 100.00
T = 1.
r = 0.05
sigma = 0.2
lamb = 1.0
mu = -0.2
delta = 0.1


def test_option_instance_creation():
    Option(S, K, T, r, sigma)


def test_option_pricing_models():
    option = Option(S, K, T, r, sigma)

    option.price('call', 'BSM')
    option.price('call', 'BSM_FFT')
    option.price('call', 'BSM_FT_NUM')
    option.price('call', 'MERTON_FT_NUM', lamb, mu, delta)

    with pytest.raises(Exception):
        option.price('call', 'NotExistingModel')


def test_option_pricing_models_accuraccy():
    option = Option(S, K, T, r, sigma)

    bsm_call = option.price('call', 'BSM')
    bsm_fft_call = option.price('call', 'BSM_FFT')
    bsm_ft_num_call = option.price('call', 'BSM_FT_NUM')

    # BSM model is the reference value
    assert round(bsm_call, 2) == round(bsm_fft_call, 2)
    assert round(bsm_call, 2) == round(bsm_ft_num_call, 2)
