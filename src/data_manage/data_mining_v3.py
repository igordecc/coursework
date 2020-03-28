# main imports
import numpy as np
import math
from time import perf_counter
from main.OCL import compute_time_series_for_system_ocl
import matplotlib.pyplot as plt
import pickle
import os
import pandas as pd


from config.config_creator import create_config
DEFAULT_CONFIG_PARAMETERS_DICT = create_config.__kwdefaults__


def compute_last_r(osc_phase_series):
    """
    Compute r([phase1,..., phase_n]), where [phase1,..., phase_n] is last iteration tn.
    :param osc_phase_series: 2d array [t0:[phase1,..., phase_n],...,tn:[phase1,..., phase_n]]
    :return: real
    """
    sum_sin = 0
    sum_cos = 0
    for oscillator_phase in osc_phase_series[-1]:
        sum_cos += math.cos(oscillator_phase)
        sum_sin += math.sin(oscillator_phase)

    oscillators_number = len(osc_phase_series[-1])
    x = sum_cos / oscillators_number
    y = sum_sin / oscillators_number

    try:
        r = (x ** 2 + y ** 2) ** 0.5
    except:
        r = None
        print("CALCULATE R EXCEPTION")
    return r


def r_from_lambda(lambda_vector, **kwargs):
    """
    calulates r(lambda) sequence
    :param lambda_vector: [lamb0,...,lambd_n]
    :param kwargs: dictionary with topology parameters. Watch "config_creator.py" to get more info.
    :return: [r0,r1,r2,r3,r4,r5,..,r_n]
    """
    LOCAL_START_TIME = perf_counter()
    r_series = []
    local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()

    for kwarg in kwargs.keys():
        if kwarg in local_config_dict.keys():
            local_config_dict[kwarg] = kwargs[kwarg]

    for kwarg_name in kwargs.keys():
        if kwarg_name in local_config_dict.keys():
            local_config_dict[kwarg_name] = kwargs[kwarg_name]
        # else:
        #   raise  ValueError("Wrong config kwarg_name: {}".format(kwarg_name))

    config = create_config(**local_config_dict)
    for lambd in lambda_vector:
        oscillators_number = config['oscillators_number']
        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']
        pendulum_phase, _ = compute_time_series_for_system_ocl(
            omega_vector=np.array(config['omega_vector'], dtype=np.float32),
            lambda_c=lambd,
            A=np.array(config['Aij'], dtype=np.float32),
            phase_vector=phase_vector,
            a=config['t0'],
            b=config['tf'],
            oscillators_number=config['oscillators_number'],
            N_parts=config['N']
        )
        r_series.append(compute_last_r(pendulum_phase))

    print(str(config['oscillators_number'])+ " oscillators computed in "+str(perf_counter()-LOCAL_START_TIME))
    return r_series


# ====================================
def read_file(path):
    import pickle
    with open(path, "rb") as file:
        return pickle.load(file)


def r_from_lambda_mean(files:list, lambda_vector, **kwargs):
    """
    Calculate N different units of r(lambda) sequence, then take mean from every iteration to create r_mean(lambda).
    :param ic: directory with initial conditions for osc systems: phase_vector, omega_vector, Aij
    :param lambda_vector: [lamb0,...,lambd_n]
    :param kwargs: dictionary with topology parameters. Watch "config_creator.py" to get more info.
    :return: [r0,r1,r2,r3,r4,r5,..,r_n]
    """
    LOCAL_START_TIME = perf_counter()
    r_vectors = []
    for file in files:
        time_one_system = perf_counter()
        Aij, phase_vector, omega_vector = read_file(file)
        kwargs['Aij'], kwargs['phase_vector'], kwargs['omega_vector'] = Aij, phase_vector, omega_vector
        r_vectors.append( r_from_lambda(lambda_vector, **kwargs))
        print(" unit system: {:.2f} sec".format(perf_counter() - time_one_system))

    r_mean_vector =np.array(r_vectors).mean(axis=0)
    print(r_mean_vector)
    print("all systems and mean: {:.2f} sec".format(perf_counter() - LOCAL_START_TIME))
    return r_mean_vector


# =====================
def create_dir(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(dir)
    else:
        print("dir '{}' already exist".format(dir))


def experiment(topology="freescaling", n_sys=10, osc_n=100, min_l=0, max_l=10, dl=1):
    """
    Find mean line for n different realisations. Saves log and img in corresponding folders. Returns paths to log and
    img.
    :param topology: system topology
    :param n_sys: n different system realisations
    :param osc_n: oscillators number
    :param min_l: minimal lambda
    :param max_l: maximal lambda
    :param dl: delta lambda
    :return: img_path, log_path
    """
    kwarg_dict = {}
    kwarg_dict["oscillators_number"] = osc_n
    kwarg_dict["lambda_vector"] = np.arange(min_l, max_l, dl)
    kwarg_dict["topology"] = topology.lower()   # do not touch .lower()  !!!
    kwarg_dict["files"] = ["ic\\{0}{1}_{2}".format(kwarg_dict["topology"], kwarg_dict["oscillators_number"], i) for i in range(n_sys)]

    r_mean = r_from_lambda_mean(**kwarg_dict)

    plt.plot(kwarg_dict["lambda_vector"], r_mean, ".")
    plt.grid()
    img_path = "{2}\\{1}\\r_from_lambd_mean_{0}".format(kwarg_dict["oscillators_number"], kwarg_dict["topology"], "img")
    log_path = "{2}\\{1}\\r_from_lambd_mean_{0}".format(kwarg_dict["oscillators_number"], kwarg_dict["topology"], "log")

    create_dir(img_path)
    create_dir(log_path)
    plt.savefig(img_path)
    plt.close()

    with open(log_path, "wb") as file:
        pickle.dump((kwarg_dict["lambda_vector"], r_mean), file)

    return img_path, log_path

# ----------------
def experiment_pattern():
    experiment(topology="random_sw",      n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)
    experiment(topology="smallWorld",     n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)
    experiment(topology="regular_sw",     n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)

    experiment(topology="freescaling",    n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)
    experiment(topology="random",         n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)
    experiment(topology="fullyConnected", n_sys =10, osc_n=100, min_l=0, max_l=10, dl=1)


def experiment_sw1():
    for i in [100]:
        experiment(topology="random_sw",  n_sys=20, osc_n=i, min_l=0, max_l=40, dl=1)
        experiment(topology="smallWorld", n_sys=20, osc_n=i, min_l=0, max_l=40, dl=1)
        experiment(topology="regular_sw", n_sys=20, osc_n=i, min_l=0, max_l=40, dl=1)


if __name__ == '__main__':

    experiment_sw1()


