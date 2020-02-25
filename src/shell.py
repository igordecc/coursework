import math
import time

import numpy as np
import pandas as pd
from networkx import nx
import matplotlib.pyplot as plt

from config.config_creator import create_config
from main.OCL import compute_time_series_for_system_ocl


class Timer:
    def __init__(self):
        self.t = 0

    def start(self):
        self.t = time.perf_counter()
        return self

    def stop(self):
        self.t = time.perf_counter()-self.t
        return self.t


# create_config.__defaults__ #default args
DEFAULT_CONFIG_PARAMETERS_DICT = create_config.__kwdefaults__      # default kwargs
#print(create_config(**DEFAULT_CONFIG_DICT))

def compute_r(time_output_array_length, pendulum_phase_output_array, oscillators_number):
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

# calculate last r
def compute_last_r(series):
    last_iteration = series[-1]
    oscillators_number = len(last_iteration)
    r = compute_r(1, [last_iteration, ], oscillators_number)
    return r


def compute_average_r(series):
    # time 154.44 sec
    oscillators_number = len(series[0])
    N = len(series)  # iterations number
    stable_series = series[N // 2:-1]
    n = len(stable_series)
    r_array = compute_r(n, stable_series, oscillators_number)
    r_average = sum(r_array) / n
    return r_average


def update_dict_with_new_entries(_dict, new_dict):
    old_keys = _dict.keys()
    for key in new_dict:
        if key in old_keys:
            _dict[key] = new_dict[key]


def compute_system_ocl(*args, osc_min=5, osc_max=6, osc_step=10):

    #local_config_dict.update(compute_system_ocl.__kwdefaults__)
    for oscillators_number in np.arange(osc_min, osc_max, osc_step):
        local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
        local_config_dict.update({"oscillators_number": oscillators_number})
        config = create_config(**local_config_dict)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)

        pendulum_phase_output_array, pendulum_time_output_array = compute_time_series_for_system_ocl(omega_vector,
                                                                                                     config['lambd'],
                                                                                                     Aij,
                                                                                                     phase_vector,
                                                                                                     a=config['t0'],
                                                                                                     b=config['tf'],
                                                                                                     oscillators_number=config['oscillators_number'],
                                                                                                     N_parts=config['N'])
        pendulum_phase_output_array = np.transpose(np.array(pendulum_phase_output_array))
        return pendulum_phase_output_array

def compute_system_ocl_for_server(oscillators_number=55, community_number_to_detect = 4):
    config = create_config(oscillators_number=oscillators_number, filename=None, topology="barbell", community_number_to_detect=community_number_to_detect)
    # fullyConnected +
    # random +
    # freeScaling -
    # smallWorld + ok 55 or higher
    # barbell +
    phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
    phase_vector[0] = config['phase_vector']

    omega_vector = np.array(config['omega_vector'], dtype=np.float32)
    Aij = np.array(config['Aij'], dtype=np.float32)
    pendulum_phase_output_array, pendulum_time_output_array = compute_time_series_for_system_ocl(omega_vector,
                                                                                                 config['lambd'],
                                                                                                 Aij,
                                                                                                 phase_vector,
                                                                                                 a=config['t0'],
                                                                                                 b=config['tf'],
                                                                                                 oscillators_number=config['oscillators_number'],
                                                                                                 N_parts=config['N'])
    pendulum_phase_output_array = pendulum_phase_output_array
    return pendulum_phase_output_array, config

def compute_r_for_multiple_lambda_ocl(*args, lmb_min=0, lmb_max=2.5, lmb_step=0.1, oscillators_number=10, topology="smallWorld", **kwargs):
    """

    :param lmb_min:
    :param lmb_max:
    :param lmb_step:
    :param oscillators_number:
    :param topology:
        "fullyConnected"
        "random"
        "freeScaling"
        "smallWorld"
        "barbell"
    :return:
    """

    r_out = []
    lambd_out = np.arange(lmb_min, lmb_max, lmb_step)

    for _lambda in lambd_out:
        local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
        local_config_dict["lambd"] = _lambda
        update_dict_with_new_entries(local_config_dict, locals())
        config = create_config(**local_config_dict)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)

        pendulum_phase_output_array, pendulum_time_output_array = compute_time_series_for_system_ocl(omega_vector,
                                                                                                     config['lambd'],
                                                                                                     Aij,
                                                                                                     phase_vector,
                                                                                                     a=config['t0'],
                                                                                                     b=config['tf'],
                                                                                                     oscillators_number=config['oscillators_number'],
                                                                                                     N_parts=config['N'])
        # wats going on there?
        iterations_number = config['N']
        r_array = compute_r(iterations_number, pendulum_phase_output_array, oscillators_number)
        n = int(iterations_number/2)
        r_out.append(sum(r_array[-n:])/n)
    r_out = np.array(r_out)
    return lambd_out, r_out


def compute_graph_properties_for_system(*args,
                                        oscillators_number=100,
                                        topology="smallWorld",
                                        reconnectionProbability = 0.01,
                                        neighbours=10
                                        ):
    local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
    local_config_dict.update(compute_graph_properties_for_system.__kwdefaults__)

    config = create_config(**local_config_dict)
    Aij = np.array(config["Aij"])

    # cut in, because cant insert itself into ap, there are only plots possible
    G = config["topology"]  # G means graph

    centrality = nx.degree_centrality(G).values()
    #print("graph degree_centrality, max: ", max(centrality), " ; min: ",min(centrality))
    #print("graph degree_histogram: ", G.degree())
    ## print("graph diameter: ",nx.diameter(G))
    ## print("graph clustering coefficient: ", nx.average_clustering(G))


    def find_rank_diagram_series(Aij):
        """
        1. count for all nods number of dependencies (1- CONNECTION 0 - NO CONNECTION)
        2. with pandas count number of nods with each rank

        :param Aij: insert Adjacency matrix Aij
        :return: diagram data
        """

        listNum = []
        for i in range(Aij.shape[0]):
            conNumNode = 0
            for j in range(Aij.shape[1]):
                if Aij[i][j]:
                    conNumNode += 1
            listNum.append(conNumNode)
        listNum = np.array(listNum)     # to numpy array

        # Compute a histogram of the counts of non-null values.
        nodRankSeries = pd.value_counts(listNum).sort_index().reset_index()
        return tuple(nodRankSeries.values.T)

    diagram_data = find_rank_diagram_series(Aij)
    return diagram_data


def calculate_r_from_parameter(parameter_name, parameter_series):
    r_series = []
    local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
    local_config_dict['topology'] = 'smallworld'
    local_config_dict['lambd'] = 2.
    local_config_dict['oscillators_number'] = 100
    if parameter_name not in local_config_dict.keys():
        raise ValueError("Wrong parameter_name: {}".format(parameter_name))
    for parameter in parameter_series:
        local_config_dict[parameter_name] = parameter
        config = create_config(**local_config_dict)
        oscillators_number = config['oscillators_number']
        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']
        pendulum_phase, _ = compute_time_series_for_system_ocl(
            omega_vector=np.array(config['omega_vector'], dtype=np.float32),
            lambda_c=config['lambd'],
            A=np.array(config['Aij'], dtype=np.float32),
            phase_vector=phase_vector,
            a=config['t0'],
            b=config['tf'],
            oscillators_number=config['oscillators_number'],
            N_parts=config['N']
        )
        r_series.append(compute_last_r(pendulum_phase))
    global r_from_parameter_config
    r_from_parameter_config = config
    parameter_series = np.array(parameter_series, dtype=np.float)
    r_series = np.array([i for j in r_series for i in j], dtype=np.float)
    return parameter_series, r_series


def plot_series(x_series, y_series):
    plt.plot(x_series, y_series, "b.")
    plt.grid()
    plt.show()


def extended_plot(x, y, x_label, y_label, printable_info):
    """
    plot with legend and all that stuff
    :return:
    """

    start_time = time.perf_counter()
    print("time : " + str(time.perf_counter() - start_time))

    import scipy
    from scipy.optimize import curve_fit
    coeffs = scipy.polyfit(x,y, 3)
    smooth_curve = scipy.polyval(coeffs, x)
    plt.plot(x, y, "b.")
    # plt.plot(x, smooth_curve,"r")
    f0 = lambda t, a, b, c: a*np.exp(-t*b) + c
    print(x)
    print(y)
    optimised_curve, _ = curve_fit(f0,  x,  y, p0=(0.01,1, 0.7))
    print("optimised_curve", optimised_curve)

    plt.plot(x, f0(x, *optimised_curve), "m")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # print(printable_info)
    plt.grid()
    plt.show()

if __name__ == '__main__':

    oscillators_number = np.arange(200, 1000, 10) # 154 sec for [100,1000,1] # 129 sec with last r (-20 sec!)

    oscillators_number = np.concatenate((np.arange(101, 200, 1), oscillators_number, ))

    x,y = calculate_r_from_parameter("oscillators_number", oscillators_number)
    x = oscillators_number / 1000

    extended_plot(x,y, "oscillators_number", "r", r_from_parameter_config)
    # reconnectionProbability = [i for i in np.arange(0, 1, 0.01)]
    # data = calculate_r_from_parameter("reconnectionProbability", reconnectionProbability)




    # DONE write optimized r(parameter) plot function
    # DONE replace r-finder program (which calculate many r), with analog (with just pick last r)
    # # because there is still inconsistency with avarage r's - better just do more calcs.



    #print(compute_system_ocl_for_server())
