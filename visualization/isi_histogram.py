import matplotlib.pyplot as plt
import numpy as np

def plot_isi_histogram(all_isi, ch, sigma):
    """
    Plots the probability density function (PDF) of the Inter-Spike Intervals.
    """
    if not all_isi:
        print("No spikes detected. Cannot plot ISI histogram.")
        return

    # Convert timestep counts into actual time (milliseconds)
    dt = 0.01
    isi_ms = np.array(all_isi) * dt

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # density=True converts the Y-axis from "raw count" to "probability density"
    # bins=50 groups the data into 50 distinct columns
    ax.hist(isi_ms, bins=50, density=True, alpha=0.7, color='purple', edgecolor='black')

    # Formatting
    model_names = {1: "Deterministic FHN", 2: "Additive FHN", 3: "Multiplicative FHN", 4: "LIF", 5: "Radial OU"}
    model_name = model_names.get(ch, "Unknown Model")

    ax.set_title(f'ISI Distribution: {model_name} ($\sigma$ = {sigma})')
    ax.set_xlabel('Inter-Spike Interval (ms)')
    ax.set_ylabel('Probability Density')
    ax.grid(axis='y', alpha=0.5, linestyle='--')
    
    plt.show()