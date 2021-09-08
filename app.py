from enum import Enum
from datetime import datetime
from datetime import timedelta
import streamlit as st

from options import Option
from options import Ticker


class OPTION_PRICING_MODEL(Enum):
    BSM = 'BSM'
    BSM_FT_NUM = 'BSM via Furier Transform (Lewis)'
    BSM_FFT = 'BSM via FFT (Lewis)'


@st.cache
def get_historical_data(ticker):
    """Getting historical data for speified ticker and caching it with streamlit app."""
    return Ticker.get_historical_data(ticker)


###################
##Streamlit config#
###################

st.title('Option pricing')

# User selected model from sidebar
pricing_method = st.sidebar.radio('Please select option pricing method', options=[model.value for model in OPTION_PRICING_MODEL])  # noqa

# Displaying specified model
st.subheader(f'Pricing method: {pricing_method}')

# Model parameters
# Parameters for Black-Scholes model
ticker = st.text_input('Ticker symbol', 'AAPL')
strike_price = st.number_input('Strike price')
risk_free_rate = st.slider('Risk-free rate (%)', 0, 100, 10)
sigma = st.slider('Sigma (%)', 0, 100, 20)
exercise_date = st.date_input('Exercise date', min_value=datetime.today() + timedelta(days=1), value=datetime.today() + timedelta(days=365))  # noqa


if st.button(f'Calculate option price for {ticker}'):
    # Getting data for selected ticker
    data = get_historical_data(ticker)
    print(data)
    st.write(data.tail())
    ticker_plot_pbj = Ticker.plot_data(data, ticker, 'Adj Close')
    st.pyplot(ticker_plot_pbj)

    # Formating selected model parameters
    spot_price = Ticker.get_last_price(data, 'Adj Close')
    risk_free_rate = risk_free_rate / 100
    sigma = sigma / 100
    days_to_maturity = (exercise_date - datetime.now().date()).days

    # Option object
    option = Option(spot_price, strike_price, days_to_maturity/365, risk_free_rate, sigma)  # noqa

    # Calculating option price
    call_price = None
    if pricing_method == OPTION_PRICING_MODEL.BSM.value:
        call_price = option.price('call', 'BSM')
    elif pricing_method == OPTION_PRICING_MODEL.BSM_FFT.value:
        call_price = option.price('call', 'BSM_FFT')
    elif pricing_method == OPTION_PRICING_MODEL.BSM_FT_NUM.value:
        call_price = option.price('call', 'BSM_FT_NUM')

    # Displaying call/put option price
    st.subheader(f'Call option price: {call_price}')
