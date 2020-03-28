# main imports
import numpy as np
import math
from main.OCL import compute_time_series_for_system_ocl
import os

# config preparation
from config.config_creator import create_config
DEFAULT_CONFIG_PARAMETERS_DICT = create_config.__kwdefaults__

FOLDER = "/sf"
TOPOLOGY = "freeScaling"

# --------- smallest unit for data mining
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



# ----- compute loops -- and -- post processing
def compute_last_r(osc_phase_series):
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

def test_compute_last_r(f):
    assert f([0,0,0,0,0,0,0]) == 1
    assert f([0, 1, 0, 1, 0, 1, 0]) != 0
    return True



def calculate_r_from_lambda(parameter_name, parameter_series, **kwargs):
    LOCAL_START_TIME = perf_counter()
    r_series = []
    local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
    local_config_dict['topology'] = TOPOLOGY
    local_config_dict['lambd'] = 2.
    local_config_dict['reconnectionProbability'] = 0.15
    local_config_dict['oscillators_number'] = 100
    if parameter_name not in local_config_dict.keys():
        raise ValueError("Wrong parameter_name: {}".format(parameter_name))

    for kwarg_name in kwargs.keys():
        if kwarg_name in local_config_dict.keys():
            local_config_dict[kwarg_name] = kwargs[kwarg_name]
        else:
            raise ValueError("Wrong config kwarg_name: {}".format(kwarg_name))


    config = create_config(**local_config_dict)
    for lambd in parameter_series:
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
    # global r_from_parameter_config
    # r_from_parameter_config = config
    if START_TIME:

        print(str(config['oscillators_number'])+ " oscillators computed in "+str(perf_counter()-LOCAL_START_TIME)+" sec, total run is "
              +str(perf_counter()-START_TIME))


    return r_series

# precompute functions

def calculate_r_from_lambda_for_oscillators_number(_lambda = np.arange(0.1, 50, 0.2), **kwargs):
    """
    specialised wrapper function for universal r(lambd) function
    """
    parameter_name = "lambd"
    oscillators_number_values = [100,300,500] #np.arange(100, 301, 100)
    r_list_c = [calculate_r_from_lambda(parameter_name, _lambda, oscillators_number=oscillators_number) for oscillators_number in oscillators_number_values]
    r_list = np.transpose(r_list_c)
    x, y = _lambda, r_list

    second_parameters_name = "oscillators_number"
    filewrite_multi_series(parameter_name, x, y, second_parameters_name, oscillators_number_values, **kwargs)


def calculate_r_from_lambda_for_several_oscillators(_lambda = np.arange(0.1, 50, 0.2),
                                                    oscillators_number=100,
                                                    how_many_osc=10,
                                                    **kwargs):
    """
        specialised wrapper function for r(lambd) function with same number of oscillators but different internal
         topology.
    """
    parameter_name = "lambd"
    if "oscillators_number_values" in kwargs.keys():
        oscillators_number_values = kwargs["oscillators_number_values"]
    else:
        oscillators_number_values = [oscillators_number for i in range(how_many_osc)]
        r_list_c = [calculate_r_from_lambda(parameter_name,
                                        _lambda,
                                        oscillators_number=oscillators_number
                                        ) for oscillators_number in oscillators_number_values]
    r_list_tr = np.transpose(r_list_c)

    y_mean = [[np.mean(itteration),] for itteration in r_list_tr]
    r_list_tr_plus = y_mean #np.concatenate([y_mean, r_list_tr ], axis=1)

    print(r_list_tr_plus)
    x, y = _lambda, r_list_tr_plus

    second_parameters_name = "several_oscillators"
    filewrite_multi_series(parameter_name, x, y, second_parameters_name, oscillators_number_values, **kwargs)
    return x, y


# file write function

def filewrite_multi_series(parameter_name:str, x, y, second_parameters_name:str, second_parameters_values, filename = None):
    """
    Writes multiple series to file
    """

    if filename is None:
        filename = "r_from_" + parameter_name + "_for_" + second_parameters_name + '.txt'
    path = os.path.join('log', FOLDER, filename)
    with open(path, "w") as f:
        f.write(second_parameters_name + " " + " ".join([str(column) for column in second_parameters_values]) + "\n")
        for i in range(len(x)):
            f.write(str(x[i]) + " " + " ".join([str(column) for column in y[i]]) + "\n")


if __name__ == '__main__':
    # """
    #  "fullyConnected".lower():
    #     "random".lower():
    #     "freeScaling".lower():
    #     "smallWorld".lower():
    #     "regular".lower():
    #     "barbell".lower():
    # """
    from time import perf_counter

    START_TIME = perf_counter()

    FOLDER = "regular"
    TOPOLOGY = "regular"
    x,y = calculate_r_from_lambda_for_several_oscillators(_lambda=np.arange(0.1, 20, 1), filename="r_from_lambd_mean.txt")
    print("calcs done in " + str(perf_counter() - START_TIME))

    from data_processing import read_plot_save
    read_plot_save("r_from_lambd_mean.txt", FOLDER, FOLDER)

