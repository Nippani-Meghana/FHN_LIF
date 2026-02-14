import simulation
from Models.FHN import FHN
import matplotlib.pyplot as plt
import numpy as np

def timeseries(ch, sigma):
    # 1. Run the correct simulation based on choice
    if(int(ch) == 1):
        results = simulation.deterministic(-1.00125,-0.46)

    elif(int(ch) == 2):
        results = simulation.additive_noise(-1.00125,-0.4,sigma)

    elif(int(ch) == 3):
        results = simulation.multiplicative_noise(-1.00125,-0.4,sigma)

    # 2. Extract data (Assuming all return v, w as the first two elements)
    v_data = results[0]
    w_data = results[1]
    dt = 0.01 
    t = np.arange(len(v_data)) * dt

    print("Plotting Vt vs T...")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, v_data, color='red', linewidth=0.8)
    ax.set_ylim([-2.2, 2.2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.set_xlabel('T (ms) ')
    ax.set_ylabel('Vt (membrane potential)')
    ax.set_title(f'Additive Noise: sigma = {sigma}')

    plt.show()

    print("Plotting Wt vs T...")
    tw = np.arange(len(w_data)) * dt
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(tw,w_data,color='blue', linewidth=0.8)
    ax.set_ylim([-1.2,1.7])
    ax.set_yticks([-1.0,-0.5,0,0.5,1,1.5])
    ax.set_xlabel('T (ms)')
    ax.set_ylabel('Wt (recovery variable)')
    ax.set_title(f'Additive Noise: sigma = {sigma}')
    plt.show()





        



    
