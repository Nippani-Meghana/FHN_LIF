import numpy as np
from scipy.optimize import fsolve
import sympy as sp

class FHN:
    def __init__(self, a,b,tau,I_ext):
        self.a = a
        self.b = b
        self.tau = tau
        self.I_ext = I_ext

    # v: sodium-driven spike upswing (fast)
    # w: potassium / recovery / adaptation (slow)
    # ε controls how quickly the neuron recovers (ε = 1/τ)

    # Small ε:
    # sharp spikes
    # long refractory effects
    # strong excitability

    # Larger ε:
    # smoother dynamics
    # weaker separation
    # less neuron-like  

    v = sp.symbols('v')
    w = sp.symbols('w') 
    a = sp.symbols('a')
    b = sp.symbols('b')
    I = sp.symbols('I')
    dv = v - (v**3/3) -  w + I
    dw = v + a - (b*w)

    def f(vt,wt):
        global I_ext
        dvt = vt - (vt**3/3) - wt + I_ext
        return dvt
    
    def g(vt,wt):
        global tau,a,b
        dwt = (1/tau)*(vt + a - (b*wt))
        return dwt


    #An equilibrium point is any point that makes all rates 0 simultaneously

    def get_equilibrium():
        global dv,dw
        v_e = fsolve(dv,(1,1))
        w_e = fsolve(dw,[1,1])
        return v_e, w_e
    
    J = []
    
    def jacobian(v,w):
        global J,a,b,I,dv,dw
        J[0][0] = np.diff(dv,v)
        J[0][1] = np.diff(dv,w)
        J[1][0] = np.diff((1/tau)*dw,v)
        J[1][1] = np.diff((1/tau)*dw,w)
        return J
