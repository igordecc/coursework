# main imports
import numpy as np
import math
from time import perf_counter
from main.OCL import compute_time_series_for_system_ocl
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
    with open(path) as file:
        return pickle.load(file)

def r_from_lambda_mean(lambda_vector, **kwargs):
    """
    Calculate N different units of r(lambda) sequence, then take mean from every iteration to create r_mean(lambda).
    :param ic: directory with initial conditions for osc systems: phase_vector, omega_vector, Aij
    :param lambda_vector: [lamb0,...,lambd_n]
    :param kwargs: dictionary with topology parameters. Watch "config_creator.py" to get more info.
    :return: [r0,r1,r2,r3,r4,r5,..,r_n]
    """
    LOCAL_START_TIME = perf_counter()
    file_list = os.listdir("ic")
    print(file_list)
    r_vectors = []
    for file in file_list:
        Aij, phase_vector, omega_vector = read_file(file)
        kwargs['Aij'], kwargs['phase_vector'], kwargs['omega_vector'] = Aij, phase_vector, omega_vector
        r_vectors.append( r_from_lambda(lambda_vector, **kwargs))

    r_mean_vector =np.array(r_vectors).mean(axis=0)
    print(r_mean_vector)
    print(" systems computed in " + str(perf_counter() - LOCAL_START_TIME))
    return r_mean_vector


# =====================
def experiment_1():
    kwarg_dict = {}
    kwarg_dict["oscillators_number"] = 100
    kwarg_dict["lambda_vector"] = np.arange(0, 10, 1)
    kwarg_dict["topology"] = "random"
    kwarg_dict["ic"] = "D:\\work\\course work\\src\\data_manage\\ic"

    import matplotlib.pyplot as plt

    r_mean = r_from_lambda_mean(**kwarg_dict)

    plt.plot(kwarg_dict["lambda_vector"], r_mean )
    plt.show()




if __name__ == '__main__':
    experiment_1()