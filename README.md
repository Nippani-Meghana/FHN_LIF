# FHN_LIF

## Project Overview

This project implements deterministic and stochastic versions of the FitzHugh–Nagumo (FHN) neuron model in the excitable regime, with the goal of replicating and exploring the results presented in:

Marius E. Yamakou, Tat Dat Tran, Luu Hoang Duc, Jürgen Jost
"The stochastic FitzHugh–Nagumo neuron model in the excitable regime embeds a leaky integrate-and-fire model"

The repository provides:

* A clean object-oriented implementation of the FHN model
* Deterministic and stochastic simulation modules
* Additive and multiplicative noise implementations
* Phase plane visualization tools
* Ensemble-based spike statistics analysis
* Centralized configuration management

The structure is modular to allow extension toward more advanced stochastic analysis, LIF embedding comparisons, and parameter exploration.

---

## Scientific Context

The FitzHugh–Nagumo model is a two-dimensional reduction of the Hodgkin–Huxley equations:

* v: fast membrane potential variable
* w: slow recovery (adaptation) variable

In the excitable regime, the system has a stable equilibrium. However, sufficiently large perturbations (or noise) can drive the system through a large excursion resembling an action potential.

The referenced paper demonstrates that in this regime, the stochastic FHN model effectively embeds a leaky integrate-and-fire (LIF) model. This project provides numerical infrastructure to:

* Simulate deterministic baseline dynamics
* Add additive noise (Euler–Maruyama)
* Add multiplicative noise (Stochastic Runge–Kutta / Heun)
* Detect spikes via threshold crossing
* Perform ensemble spike statistics

---

## Project Structure

```
FHN_LIF
│
├── Models
│   ├── __init__.py
│   └── FHN.py
│
├── simulation
│   ├── __init__.py
│   ├── deterministic.py
│   ├── additive_noise.py
│   ├── multiplicative_noise.py
│   └── path_calling.py
│
├── visualization
│   ├── phase_portrait.py
│   └── timeseries.py
│
├── analysis
│   ├── __init__.py
│   └── ensemble_stats.py
│
├── config
│   └── fhn_params.json
│
└── main.py
```

---

## Core Components

### 1. Models/FHN.py

Defines the FitzHugh–Nagumo system:

Equations:

```
dv/dt = v − v^3/3 − w + I_ext
dw/dt = (1/τ)(v + a − b w)
```

Features:

* Drift functions f(v, w) and g(v, w)
* Numerical equilibrium computation using `fsolve`
* Symbolic Jacobian computation using SymPy
* Stability analysis via eigenvalues

This class is the core dynamical engine used by all simulation modules.

---

### 2. simulation/

All time evolution routines are separated from model definition.

#### deterministic.py

* Standard Euler method for ODE integration
* Provides baseline excitable regime trajectory
* Returns:

  * v(t), w(t)
  * equilibrium point
  * Jacobian evaluated at equilibrium

Used for verifying fixed-point stability and deterministic threshold behavior.

---

#### additive_noise.py

Implements Euler–Maruyama method for SDEs:

```
w(t+dt) = w(t) + g(v,w) dt + σ dW
```

Where:

* dW ~ N(0, sqrt(dt))
* Noise is independent of state

Purpose:

* Study noise-induced spiking
* Examine escape from stable fixed point
* Compare spike variability to LIF behavior

---

#### multiplicative_noise.py

Implements second-order Stochastic Runge–Kutta (Heun method):

* Noise term scales with state variable w
* Predictor-corrector structure
* Increased numerical stability for state-dependent noise

Used to study more realistic stochastic modulation of recovery dynamics.

---

#### path_calling.py

Centralized configuration loader.

Reads model parameters from:

```
config/fhn_params.json
```

Ensures all simulations use consistent parameter values.

---

### 3. visualization/

#### phase_portrait.py

Generates:

* Phase plane trajectories
* v-nullcline (cubic)
* w-nullcline (linear)
* Equilibrium point

Allows reproduction of excitable vs subthreshold trajectories similar to Figure 1 of the referenced paper.

Noise-driven phase portraits illustrate the stochastic deformation of trajectories.

---

### 4. analysis/

#### ensemble_stats.py

Performs ensemble-based statistical analysis:

* Runs 100 independent trials
* Spike detection via upward threshold crossing
* Returns:

  * Spike count per trial
  * Spike timing indices per trial

Spike detection rule:

```
v[i-1] < v_threshold and v[i] >= v_threshold
```

This provides:

* Inter-spike interval extraction
* Spike count variability
* Statistical comparison across deterministic and stochastic regimes

---

### 5. config/fhn_params.json

Central parameter file:

```
{
  "fhn_parameters": {
    "I_ext": 0.265,
    "a": 0.7,
    "b": 0.75,
    "tau": 12.5
  }
}
```

Encourages reproducibility and easy parameter sweeps.

---

## How to Run

### Run ensemble statistics

From project root:

```
python main.py
```

You will be prompted to choose:

1. Deterministic FHN
2. Stochastic Additive FHN
3. Stochastic Multiplicative FHN

The program will execute 100 trials and output spike counts.

---

### Run phase portrait visualization

Execute:

```
python visualization/phase_portrait.py
```

You will be prompted to select the simulation type.

A phase plane plot with nullclines and equilibrium will be displayed.

---

## Numerical Methods Summary

| Model Type     | Method Used          |
| -------------- | -------------------- |
| Deterministic  | Euler method         |
| Additive Noise | Euler–Maruyama       |
| Multiplicative | Stochastic RK (Heun) |

Time step:

```
dt = 0.01
```

Total simulation time:

```
T = 1000
```

---

## Relation to LIF Embedding

In the excitable regime:

* The deterministic FHN model has a stable fixed point.
* Noise triggers large excursions.
* The inter-spike intervals resemble those of a leaky integrate-and-fire model.

This implementation allows:

* Empirical verification of spike timing variability
* Exploration of escape dynamics
* Study of noise scaling effects

Future work may include:

* Direct LIF model implementation for comparison
* First passage time analysis
* Reduced 1D projection near fixed point
* Fokker–Planck approximation

---

## Design Philosophy

The repository separates:

* Mathematical model definition
* Numerical integration schemes
* Visualization
* Statistical analysis
* Configuration

This modularity enables:

* Easy substitution of integrators
* Parameter sweeps
* Extension to other neuron models
* Testing stochastic numerical stability

---

## Suggested Extensions

1. Add reproducible random seeds
2. Implement ISI histogram plotting
3. Add coefficient of variation (CV) calculation
4. Compare to analytical LIF statistics

---

## Dependencies

* numpy
* scipy
* sympy
* matplotlib
* json
* pathlib

Install with:

```
pip install numpy scipy sympy matplotlib
```

---

## Final Notes

This codebase is designed not just to simulate the FHN model, but to serve as a controlled computational framework for investigating how stochastic excitable systems reduce to simpler integrate-and-fire descriptions.

Careful numerical method choice is essential, especially for multiplicative noise. The separation of deterministic and stochastic solvers allows direct methodological comparison.

