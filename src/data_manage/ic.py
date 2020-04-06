"""
Initial conditions creator.
"""
import pandas as pd
from config_creator import create_config
import os
from time import perf_counter

def write_ic(config, path):
    ic_data = [
    config['Aij'],
    config['phase_vector'],
    config['omega_vector'],
    ]
    import pickle
    with open(path, "wb") as file:
        pickle.dump(ic_data, file)


def write_n_topological_ic(n:int, osc:int, topology:str):
    start = perf_counter()
    for i in range(n):
        local = perf_counter()
        config = create_config(oscillators_number=osc, topology=topology)
        directory = "ic\\"
        name = "{0}{1}_{2}".format(topology, osc, i)
        path = os.path.join(directory, name)
        write_ic(config, path)
        print(" osc:{2}, iteration:{0}, time: {1} sec".format(i, perf_counter()-local, osc))

    print("complete osc: {1},  time: {0} sec".format(perf_counter()-start, osc))

def creation_template():
    n_sys = 100
    for osc in range(100, 1001, 100):
        write_n_topological_ic(n_sys, osc=osc, topology="freescaling")
        write_n_topological_ic(n_sys, osc=osc, topology="random")
        write_n_topological_ic(n_sys, osc=osc, topology="fullyConnected")


if __name__ == '__main__':
    n_sys = 20
    for osc in range(10000, 10001, 100):
        # write_n_topological_ic(n_sys, osc=osc, topology="freescaling")
        write_n_topological_ic(n_sys, osc=osc, topology="random")
        write_n_topological_ic(n_sys, osc=osc, topology="fullyConnected")
        write_n_topological_ic(n_sys, osc=osc, topology="smallworld")
        write_n_topological_ic(n_sys, osc=osc, topology="random_sw")
        write_n_topological_ic(n_sys, osc=osc, topology="regular_sw")


