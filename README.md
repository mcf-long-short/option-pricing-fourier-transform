# Option pricing via Fourier transform methods

## Introduction

`Fourier Transform` and `Fast Fourier transforms (FFT)` represent popular approaches to option pricing. They provide a semi-closed form expressions for `European` and `American option prices`. Most importantly, calculation using these methods is fast and accurate, very useful when we need to bring the model to data (to calibrate it). A number of methods have been proposed in the literature. The goal of this project is to implement these algorithms for `Black–Scholes and Merton model`. Hilpisch (2015) contains both brief introduction to the methods as well as implementation of various models in Python 2. A really nicely written intro to the Fourier transform and their applications in option pricing can be found in Schmeltze (2010). 

Project goals: 
* Describing different Fourier transform methods.
* Implementing the algorithms for these methods. 
* Providing a numerical examples for Black–Scholes and Merton model. 
* Designing numerical experiments to study the rate of convergence for these algorithms. 
* Summarizing the results and findings and drawing conclusions, both theoretically and empirically.

Key References: 
* Hilpisch, Y. (2015) Derivatives Analytics with Python, John Wiley 
* Schmeltze (2010) Fourier Pricing. Full title: Option Pricing formulae using Fourier Transform: Theory and Applications 
* Kienitz, J., & Wetterau, D. (2013). Financial modelling: Theory, implementation and practice with MATLAB source. John Wiley & Sons. 
* Rouah, F. D. (2013). The Heston model and its extensions in Matlab and C#. John Wiley & Sons. 

Other References: 
* Carr, P., & Madan, D. (1999). Option valuation using the fast Fourier transform. Journal of Compu tational Finance, 2(4), 61–73. 
* Fang, F., & Oosterlee, C. W. (2008). A novel pricing method for European options based on Fourier cosine series expansions. SIAM Journal on Scientific Computing, 31(2), 826–848. 
* Fang, F., & Oosterlee, C. W. (2009). Pricing early-exercise and discrete barrier options by Fourier cosine series expansions. Numerische Mathematik, 114(1), 27–62. 
* Fang, F., & Oosterlee, C. W. (2011). A Fourier-based valuation method for Bermudan and barrier options under Heston’s model. SIAM Journal on Financial Mathematics, 2(1), 439–463. 
* Jackson, K. R., Jaimungal, S., & Surkov, V. (2008). Fourier space time-stepping for option pricing with L´evy models. Journal of Computational Finance, 12(2), 1–29. 
* Lord, R., Fang, F., Bervoets, F., & Oosterlee, C. W. (2008). A fast and accurate FFT-based method for pricing early-exercise options under L´evy processes. SIAM Journal on Scientific Computing, 30(4), 1678–1705. 

This repository represents group project work for course in `Derivatives` for advanced degree [Masters in Computational Finance, Union University](http://mcf.raf.edu.rs/).
