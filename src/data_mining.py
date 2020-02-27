# main imports
import numpy as np
import math
from main.OCL import compute_time_series_for_system_ocl

# config preparation
from config.config_creator import create_config
DEFAULT_CONFIG_PARAMETERS_DICT = create_config.__kwdefaults__


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


def calculate_r_from_parameter(parameter_name, parameter_series):
    r_series = []
    local_config_dict = DEFAULT_CONFIG_PARAMETERS_DICT.copy()
    local_config_dict['topology'] = 'smallworld'
    local_config_dict['lambd'] = 2.
    local_config_dict['reconnectionProbability'] = 0.15
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
    parameter_series = np.array(parameter_series)
    r_series = np.array([i for j in r_series for i in j], dtype=np.float)
    return parameter_series, r_series

# Evaluation time note: osc numbers [100,1000,1]    154 sec for average r   and  129 sec with last r (-20 sec!)
# ---- application functions
def filewrite(parameter_name:str, x, y):
    file = './log/r_from_' + parameter_name + '.txt'
    with open(file, "w") as myfile:
        for i in range(len(x)):
            myfile.write(str(x[i]) + " " + str(y[i]) + "\n")


def calculate_r_from_oscillators_number():

    oscillators_number = np.arange(100, 1000, 1)

    parameter_name = "oscillators_number"
    x,y = calculate_r_from_parameter(parameter_name, oscillators_number)
    filewrite(parameter_name, x, y)


def calculate_r_from_topology():

    topology = [
        'smallWorld',
        'freeScaling',
        'regular',
        'random'
    ]

    parameter_name = "topology"
    x,y = calculate_r_from_parameter(parameter_name, topology)
    filewrite(parameter_name, x, y)


def calculate_r_from_reconnection_probability():

    reconnection_probability = np.arange(0, 1, 10**-3)

    parameter_name = "reconnectionProbability"
    x,y = calculate_r_from_parameter(parameter_name, reconnection_probability)
    filewrite(parameter_name, x, y)


def calculate_r_from_lambda():

    _lambda = np.arange(0.1, 5, 0.01)

    parameter_name = "lambd"
    x, y = calculate_r_from_parameter(parameter_name, _lambda)
    filewrite(parameter_name, x, y)


if __name__ == '__main__':
    # calculate_r_from_oscillators_number()
    # calculate_r_from_reconnection_probability()
    # calculate_r_from_topology()
    calculate_r_from_lambda()
