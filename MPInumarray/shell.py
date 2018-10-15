from config.config_creator import create_config
import numpy as np
import math
import time
import matplotlib.pyplot as pp
try:
    from main.OCL_v2 import ad
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


def load_kuramotosystem_from_config(config):
    return cls.KuramotoSystem(config['omega_vector'], config['lambd'], config['Aij'], config['phase_vector'], config['t0'], config['tf'], config['N'], config['oscillators_number'])


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


def computeSystemOCL(osc_min=1, osc_max=101, osc_step=10):

    for oscillators_number in np.arange(osc_min, osc_max, osc_step):
        config = create_config(oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)
        timer = Timer().start()
        pendulum_phase_output_array, pendulum_time_output_array = ad(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']

        return pendulum_phase_output_array, pendulum_time_output_array, time_output_array_length

def plotComputed(pendulum_phase_output_array, pendulum_time_output_array):
    pp.plot(pendulum_phase_output_array, pendulum_time_output_array)

def computeRLSystemOCL(lmb_min=0, lmb_max=2.5, lmb_step=0.1, oscillators_number=10):
    r_out = []
    lambd_out = np.arange(lmb_min, lmb_max, lmb_step)

    for _lambda in lambd_out:
        config = create_config(lambd=_lambda, oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)

        pendulum_phase_output_array, pendulum_time_output_array = ad(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']
        r_array = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)
        n = 1000
        r_out.append( sum(r_array[-n:])/n)


if __name__ == '__main__':
    pendulum_phase_output_array, pendulum_time_output_array, time_output_array_length = computeSystemOCL(osc_min=1000, osc_max=1001, osc_step=20)

    print(pendulum_time_output_array)
    print(pendulum_phase_output_array)
    print(time_output_array_length)
    pp.plot(pendulum_time_output_array, np.linspace(0, len(pendulum_time_output_array)))


#TODO plot pendulum_phase_output_array somehow

#TODO import shell.py  functions in UI.py. Run them, if button clicked.

#TODO make new coments after all