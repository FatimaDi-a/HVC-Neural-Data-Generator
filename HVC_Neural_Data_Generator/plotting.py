import matplotlib.pyplot as plt
import numpy as np

def plot_neuron_raster(data, title, color, filename):
    plt.figure(figsize=(18, 12))

    for t in range(data.shape[1]):
        for n in range(data.shape[0]):
            if data[n, t] != 0:
                plt.scatter(t, data.shape[0] - n, color=color, marker='|', s=15)

    plt.title(title, fontsize=14)
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron")
    plt.xlim(-1, data.shape[1])

    plt.savefig(filename + ".png", dpi=600, bbox_inches="tight")
    plt.savefig(filename + ".pdf", dpi=300, bbox_inches="tight")
    plt.close()

def sort_neurons_by_bursts(data):
    burst_order = []
    for neuron in data:
        times = np.where(neuron != 0)[0]
        burst_order.append((neuron, times))
    burst_order.sort(key=lambda x: x[1][0] if len(x[1]) > 0 else np.inf)
    return np.array([n for n, _ in burst_order])
