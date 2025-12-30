from .plotting import plot_neuron_raster
from .plotting import sort_neurons_by_bursts

def plot_all(data, outdir="results"):
    plot_neuron_raster(
        data["Ra"],
        "HVC_RA Neuron Burst",
        color="#bc272d",
        filename=f"{outdir}/RA_raster.png"
    )

    plot_neuron_raster(
        sort_neurons_by_bursts(data["X"]),
        "HVC_X Neuron Burst",
        color="#50ad9f",
        filename=f"{outdir}/X_raster.png"
    )

    plot_neuron_raster(
        data["interneurons"],
        "HVC Interneuron Burst",
        color="#0000a2",
        filename=f"{outdir}/INT_raster.png"
    )