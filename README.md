# Option pricing via Fourier transform methods

Stramlit app: https://share.streamlit.io/mcf-long-short/option-pricing-fourier-transform/main/app.py

## Introduction

`Fourier Transform` and `Fast Fourier transforms (FFT)` represent popular approaches to option pricing. They provide a semi-closed form expressions for `European` and `American option prices`. Most importantly, calculation using these methods is fast and accurate, very useful when we need to bring the model to data (to calibrate it). A number of methods have been proposed in the literature. The goal of this project is to implement these algorithms for `Black–Scholes` and `Merton model`. Brief introduction to the methods as well as implementation of various models in Python can be found in `Hilpisch (2015)`. A really nicely written intro to the Fourier transform and their applications in option pricing can be found in `Schmeltze (2010)`.

This repository contains implementation of various Fourier transform methods for pricing options: Black–Scholes and Merton model via FT and FFT.

Key implementation references:

- Hilpisch, Y. (2015) Derivatives Analytics with Python, John Wiley
- Schmeltze (2010) Fourier Pricing. Full title: Option Pricing formulae using Fourier Transform: Theory and Applications

This repository represents group project work for course in `Derivatives` for advanced degree [Masters in Computational Finance, Union University](http://mcf.raf.edu.rs/).

## Demo

https://user-images.githubusercontent.com/30963594/132988185-6e9852a1-0392-4008-91f9-554d60b6c3b1.mp4

## How to run the code?

### Running in docker container

Build image and run docker container:

```
docker build -t option-pricing-fourier:latest .
docker run -p 8080:8080 option-pricing-fourier:latest
```

Streamlit app should be at: `http://localhost:8080/`

### Running locally

Create python venv and install requirements

```
# Create virtual env
python3 -m venv venv

#Activate venv (Unix/MaxOS)
source venv/bin/activate

#Activate venv (Windows)
venv\Scripts\activate.bat

# Install requirements
python -m pip install -r requirements.txt
```

To run streamlit app: `streamlit run app.py`
