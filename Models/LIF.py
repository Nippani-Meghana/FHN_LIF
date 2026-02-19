import numpy as np
from simulation.path_calling import path_calling_lif


class LIF:
    def __init__(self, I_ext, R, V_r, tau):
        self.R = R
        self.V_r = V_r
        self.tau = tau
        self.I_ext = I_ext

    def leaky_integrate_and_fire_model(self, vt):
        dvt = (1/self.tau)*(-(vt - self.V_r) + (self.R*self.I_ext))
        return dvt