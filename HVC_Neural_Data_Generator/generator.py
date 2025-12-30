import numpy as np
import random
from math import exp
import os
from .plotting import plot_neuron_raster, sort_neurons_by_bursts


def generate_Ra(RAdim, time):
    available_indices = list(np.arange(time - 5))
    Ra_data = np.zeros((RAdim, time))
    for i in range(RAdim):
        start_idx = np.random.choice(available_indices)
        available_indices.remove(start_idx)
        Ra_data[i, start_idx:start_idx + 5] = 1
    return Ra_data

def generate_list(nbr_gaps, total_sum):
    randm = [random.randint(2,100) for i in range(nbr_gaps)]
    total = sum(randm)
    normalized = [int(x/total * total_sum) for x in randm]
    diff = total_sum - sum(normalized)
    while diff != 0:
        for i in range(abs(diff)):
            index = random.randint(0,nbr_gaps-1)
            if diff > 0:
                normalized[index] += 1
            elif diff < 0:
                normalized[index] -= 1
            diff = total_sum - sum(normalized)
    random.shuffle(normalized)
    return normalized

# Generate list for bursting gaps (the bursts length should be between 2-6 that is 10-30ms)
def generate_list_bursts(nbr_gaps, total_sum):
    normalized = [random.randint(1,5) for i in range(nbr_gaps)]
    #normalized = [5]* nbr_gaps
    total = sum(normalized)
    #normalized = [int(x/total * total_sum) for x in randm]
    diff = total_sum - sum(normalized)
    while diff != 0:
        for i in range(abs(diff)):
            index = random.randint(0,nbr_gaps-1)
            if diff > 0:
                if normalized[index] <6:
                    normalized[index] += 1
            elif diff < 0:
                if normalized[index] > 2:
                    normalized[index] -= 1
            diff = total_sum - sum(normalized)
    random.shuffle(normalized)
    return normalized
    
# Generate the interneuron's burst pattern based on silent period and burst blocks
def generate_interneuron_pattern(silent_periods, burst_blocks):
    result = []
    p = random.uniform(0,1)
    if p> 0.5: #Start with silence
        for i in range(len(silent_periods)):
            result.extend([0] * silent_periods[i])  # Add zeros for the silent period
            result.extend([1] * burst_blocks[i])  # Add ones for the burst period
    else: #Start with a burst
        for i in range(len(silent_periods)):
            result.extend([1] * burst_blocks[i])  # Add ones for the burst period
            result.extend([0] * silent_periods[i])  # Add zeros for the silent period
    return result

# Get the bursting pattern for each interneuron
def create_interneuron_dataset(dim, time, nbr_gaps, intensity_min = 8, intensity_max =20):
    interneuron_dataset = np.zeros((dim,time))
    for i in range(dim):
        intensity = np.random.randint(intensity_min, intensity_max + 1)
        silence = int(100 - intensity)
        silent_periods_durations = generate_list(nbr_gaps, int(time*silence/100))
        burst_blocks_durations = generate_list_bursts(nbr_gaps, int(time*intensity/100))
        interneuron_dataset[i] = generate_interneuron_pattern(silent_periods_durations, burst_blocks_durations)
    return interneuron_dataset


def generate_X(dim, time, min_bursts=2, max_bursts=4, min_gap=6):
    X_data1 = np.zeros((dim, time), dtype=int)
    burst_length = 5

    for neuron_idx in range(dim):
        num_bursts = np.random.randint(min_bursts, max_bursts + 1)
        burst_times = []

        # Generate bursts ensuring the minimum gap
        available_times = set(range(6,time))
        for _ in range(num_bursts):
            possible_times = [t for t in available_times if all(abs(t - bt) >= min_gap for bt in burst_times)]
            chosen_time = np.random.choice(possible_times)
            burst_times.append(chosen_time)
            # Remove times that violate the gap constraint
            available_times -= set(range(chosen_time - min_gap + 1, chosen_time + min_gap))

        # Mark the bursts in the matrix
        for burst_time in burst_times:
            X_data1[neuron_idx, burst_time:burst_time+5] = 1
    return X_data1



class GeneratorConfig:
    def __init__(self, time=500, dim=247, RAdim=495, nbr_gaps=20):
        self.time = time
        self.dim = dim
        self.RAdim = RAdim
        self.nbr_gaps = nbr_gaps
        
class DataGenerator:
    def __init__(self, config: GeneratorConfig, seed=None):
        self.config = config
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

    def generate_all(self):
        Ra = generate_Ra(self.config.RAdim, self.config.time)
        X = generate_X(self.config.dim, self.config.time)
        INT = create_interneuron_dataset(
            self.config.dim, self.config.time, self.config.nbr_gaps
        )
        return {
        "Ra": Ra,
        "X": X,
        "interneurons": INT
    }



    def run_and_save(self, outdir="results"):
        os.makedirs(outdir, exist_ok=True)
    
        data = self.generate_all()
    
        np.savez(os.path.join(outdir, "data.npz"), **data)

        return data


