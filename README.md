# Option pricing via Fourier transform methods

## Introduction

`Fourier Transform` and `Fast Fourier transforms (FFT)` represent popular approaches to option pricing. They provide a semi-closed form expressions for `European` and `American option prices`. Most importantly, calculation using these methods is fast and accurate, very useful when we need to bring the model to data (to calibrate it). A number of methods have been proposed in the literature. The goal of this project is to implement these algorithms for `Black–Scholes and Merton model`. `Hilpisch (2015)` contains both brief introduction to the methods as well as implementation of various models in Python. A really nicely written intro to the Fourier transform and their applications in option pricing can be found in `Schmeltze (2010)`.

Project goals:

- Describing different Fourier transform methods.
- Implementing the algorithms for these methods.
- Providing a numerical examples for Black–Scholes and Merton model.
- Designing numerical experiments to study the rate of convergence for these algorithms.
- Summarizing the results and findings and drawing conclusions, both theoretically and empirically.

Key implementation references:

- Hilpisch, Y. (2015) Derivatives Analytics with Python, John Wiley
- Schmeltze (2010) Fourier Pricing. Full title: Option Pricing formulae using Fourier Transform: Theory and Applications

This repository represents group project work for course in `Derivatives` for advanced degree [Masters in Computational Finance, Union University](http://mcf.raf.edu.rs/).
