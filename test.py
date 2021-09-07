# Valuation of European Call Options in BSM Model
# Comparison of Analytical, int_valueegral and FFT Approach
# 11_cal/BSM_option_valuation_FOU.py
#
# (c) Dr. Yves J. Hilpisch
# Derivatives Analytics with Python
#
import math
import numpy as np
import matplotlib.pyplot as plt

from options.models.bsm import BSM
from options.models.bsm_fourier import BSM_FT_NUM
from options.models.bsm_fourier import BSM_FFT


# conda activate base

#
# Model Parameters
#
S0 = 100.00  # initial index level
K = 100.00  # strike level
T = 1.  # call option maturity
r = 0.05  # constant short rate
sigma = 0.2  # constant volatility of diffusion


def plot_val_differences(vtype='int'):
    k_list = np.linspace(S0 * 0.6, S0 * 1.4, 50)
    ana_values = BSM().price('call', S0, k_list, T, r, sigma)
    plt.figure(figsize=(8, 6))
    plt.subplot(311)
    plt.plot(k_list, ana_values, 'b', label='analytical', lw=1.5)
    if vtype == 'int':
        int_values = np.array([BSM_FT_NUM().price('call', S0, K, T, r, sigma)
                               for K in k_list])
        plt.plot(k_list, int_values, 'r-.', label='Fourier (integral)', lw=1.5)
        diffs = int_values - ana_values
        rdiffs = (int_values - ana_values) / ana_values
    else:
        fft_values = np.array([BSM_FFT().price('call', S0, K, T, r, sigma)
                               for K in k_list])
        plt.plot(k_list, fft_values, 'r-.', label='Fourier (FFT)', lw=1.5)
        diffs = fft_values - ana_values
        rdiffs = (fft_values - ana_values) / ana_values
    plt.legend()
    plt.grid()
    plt.subplot(312)
    plt.plot(k_list, diffs, 'g', label='abs. difference', lw=1.5)
    plt.legend(loc=0)
    plt.grid()
    plt.subplot(313)
    plt.plot(k_list, rdiffs, 'r', label='rel. difference', lw=1.5)
    plt.legend(loc=0)
    plt.xlabel('strike')
    plt.grid()
    plt.tight_layout()
    plt.show()


plot_val_differences()
