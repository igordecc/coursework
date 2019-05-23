from config.config_creator import create_config
import numpy as np
import math
import time
import pandas as pd
from networkx import nx
try:
    from main.OCL import compute_time_series_for_system
except:
    import sys
    print("shell running without opencl", file=sys.stderr)


class Timer:
    def __init__(self):
        self.t = 0

    def start(self):
        self.t = time.perf_counter()
        return self

    def stop(self):
        self.t = time.perf_counter()-self.t
        return self.t


def get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number):
    r = np.zeros(time_output_array_length)
    for i in range(time_output_array_length):
        sum_cos = 0
        sum_sin = 0
        for j in pendulum_phase_output_array[i]:
            sum_cos += math.cos(j)
            sum_sin += math.sin(j)

        x = sum_cos/oscillators_number
        y = sum_sin/oscillators_number
        try:
            r[i] = (x**2 + y**2)**0.5
        except:
            r[i] = None
            print("CALCULATE R EXCEPTION")

    return r


def computeSystemOCL(osc_min=5, osc_max=6, osc_step=10):

    for oscillators_number in np.arange(osc_min, osc_max, osc_step):
        config = create_config(oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)
        timer = Timer().start()
        pendulum_phase_output_array, pendulum_time_output_array = compute_time_series_for_system(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']
        pendulum_phase_output_array = np.transpose(np.array(pendulum_phase_output_array))
        #print(pendulum_phase_output_array)
        return pendulum_phase_output_array

def computeRLSystemOCL(lmb_min=0, lmb_max=2.5, lmb_step=0.1, oscillators_number=10):
    r_out = []
    lambd_out = np.arange(lmb_min, lmb_max, lmb_step)

    for _lambda in lambd_out:
        config = create_config(lambd=_lambda, oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)

        pendulum_phase_output_array, pendulum_time_output_array = compute_time_series_for_system(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']
        r_array = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)
        n = int(time_output_array_length/2)
        r_out.append( sum(r_array[-n:])/n)
    r_out = np.array(r_out)
    ln = len(r_out)
    lin_out = np.linspace(0, ln, ln)
    return (lin_out, r_out)

def KAnalis(lambd=0.1, oscillators_number=1000, topology="smallWorld"):
    config = create_config(lambd=lambd, oscillators_number=oscillators_number, topology=topology, filename=None)
    Aij = np.array(config["Aij"])

    # cut in, because cant insert itself into ap, there are only plots possible
    G = config["topology"]  # G means graph

    centrality = nx.degree_centrality(G).values()
    print("graph degree_centrality, max: ", max(centrality), " ; min: ",min(centrality))
    print("graph degree_histogram: ",G.degree())
    print("graph diameter: ",nx.diameter(G))
    print("graph clustering coefficient: ", nx.average_clustering(G))


    listNum = []
    for i in range(Aij.shape[0]):
        conNumNode = 0
        for j in range(Aij.shape[1]):
            conNumNode += Aij[i][j]
        listNum.append(conNumNode)
    listNum = np.array(listNum)

    nodRankSeries = pd.value_counts(listNum).sort_index().reset_index()
    return tuple(nodRankSeries.values.T)


if __name__ == '__main__':
    ...
    KAnalis(.1, 100,"smallWorld")

#TODO make new coments after all