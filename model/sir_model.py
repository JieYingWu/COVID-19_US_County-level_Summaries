# Lightly modified from from https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
# Goal is to learn the beta and gamma parameters from socio-economic facotrs

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SIRmodel():
    def __init__(self, N=1000, I0=1, R0=1):
        # Total population, N.
        self.N = N
        # Initial number of infected and recovered individuals, I0 and R0.
        self.I0 = I0
        self.R0 = R0
        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = N - I0 - R0

        # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
        # These should be learned
        self.beta = 0.2
        self.gamma = 1./10

        
    # The SIR model differential equations.
    def deriv(self, y, t, N, beta, gamma):
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt


    # Learn parameters and update them here
    def update_param(self, beta, gamma):
        self.beta = beta
        self.gamma = gamma


    def plot(self, t):
        # Initial conditions vector
        y0 = self.S0, self.I0, self.R0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(self.deriv, y0, t, args=(self.N, self.beta, self.gamma))
        S, I, R = ret.T

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, axisbelow=True)
        ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
        ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number (1000s)')
        ax.set_ylim(0,1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
            plt.show()

if __name__ == "__main__":
    # A grid of time points (in days)
    t = np.linspace(0, 160, 160)
    model = SIRmodel()
    model.plot(t)
