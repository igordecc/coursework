import os
import pickle
import time

import numpy
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import perf_counter

from main.OCL_r import KuramotoSystem
from config.config_creator import create_config, NetworkConfig


def plot_and_save(path, x, y, fmt="."):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    plt.plot(x, y, fmt)
    plt.grid()
    plt.savefig(path)
    plt.close()


def save_data(path, x, y):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as file:
        pickle.dump((x, y), file)


def r_mean_experiment(
        working_dir: str,
        solver: KuramotoSystem,
        network_properties: dict,
        step: float = 0.1,
        iterations: int = 1000,
        n_networks: int = 10,
        min_lambda: float = 0,
        max_lambda: float = 10,
        step_lambda: float = 1,
        # 
        n_sys_start: int = 0,
        save_network_config=True
):
    dl_power = abs(int(numpy.log10(step_lambda)))
    lambdas = numpy.arange(min_lambda, max_lambda, step_lambda, dtype=numpy.float32)

    if "adjacency_matrix" not in network_properties.keys():
        topology = network_properties["topology"]
        n_oscillators = network_properties["n"]
    else:
        adjacency_matrix = network_properties["adjacency_matrix"]
        assert isinstance(adjacency_matrix, numpy.ndarray)
        assert len(adjacency_matrix.shape) == 2
        assert adjacency_matrix.shape[0] == adjacency_matrix.shape[1]

        topology = "None"
        n_oscillators = adjacency_matrix.shape[0]

    networks_path = os.path.join(working_dir, "networks")
    os.makedirs(networks_path, exist_ok=True)

    rs = []

    for network_id in tqdm(range(n_sys_start, n_networks)):
        path = os.path.join(networks_path, f"{topology}_{n_oscillators}_{network_id}.pickle")
        if save_network_config:
            config = NetworkConfig.create_or_load(path, **network_properties)
        else:
            config = NetworkConfig(**network_properties)
        start = perf_counter()
        r_series, timings = solver.solve_multiple(
            step,
            iterations,
            phase=config.phase,
            omega=config.omega,
            adjacency=config.adjacency,
            lambdas=lambdas
        )
        stop = perf_counter() - start
        timings["solver.solve_multiple run in"] = stop
        print(f"\n  solver.solve_multiple run in {stop} \n")
        del config

        rs.append(r_series)

    r_mean = numpy.array(rs).mean(axis=0)

    def make_path(output_type):
        return os.path.join(working_dir, output_type, topology, f"r_from_lambd_mean_{n_oscillators}_{dl_power}")

    # plot_path = make_path("plots")
    # print(f"Saving plot into {plot_path}")
    # plot_and_save(plot_path, lambdas, r_mean)
    #
    # log_path = make_path("data")
    # print(f"Saving data into {log_path}")
    # save_data(log_path, lambdas, r_mean)

    return timings


def main():
    working_dir = "experiment"
    solver = KuramotoSystem()
    osc_n_list = list(range(100, 500 + 1, 50))

    calc_time = []

    for i in osc_n_list:
        calc_time.append(
        r_mean_experiment(
            working_dir, solver,
            network_properties=dict(topology="fully_connected", n=i, ),
            min_lambda=0, max_lambda=2, step_lambda=0.01,
            n_networks=20
        )
        )
        print(f"time: {calc_time}")


if __name__ == '__main__':
    main()
