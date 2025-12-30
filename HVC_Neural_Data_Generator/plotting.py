import matplotlib.pyplot as plt
import numpy as np

def plot_neuron_raster(data, title, color,save=True, filename=None):
    plt.figure(figsize=(18, 12))

    neurons, times = np.where(data != 0)

    plt.scatter(
        times,
        neurons,
        color = color,
        marker="|",
        s=10,
        linewidths=1
    )

    plt.gca().invert_yaxis()

    plt.title(f"{title} Raster Plot", fontsize=14)
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron")

    if save:
        if filename is None:
            filename = f"{title.replace(' ', '_')}_raster.png"

        plt.savefig(filename, dpi=600, bbox_inches="tight")
        plt.savefig(filename.replace(".png", ".pdf"), bbox_inches="tight")

    plt.show()

def sort_neurons_by_bursts(data):
    burst_order = []
    for neuron in data:
        times = np.where(neuron != 0)[0]
        burst_order.append((neuron, times))
    burst_order.sort(key=lambda x: x[1][0] if len(x[1]) > 0 else np.inf)
    return np.array([n for n, _ in burst_order])
