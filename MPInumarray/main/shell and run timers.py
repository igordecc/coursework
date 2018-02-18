import KuramotoSystem as cls
import configparser
import numpy as np
import math
import time
import matplotlib.pyplot as pp
from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()  # количество узлов
rank = comm.Get_rank()  # номер узла


class Timer:
    def __init__(self):
        self.t = 0

    def start(self):
        self.t = time.perf_counter()
        return self

    def stop(self):
        self.t = time.perf_counter()-self.t
        return self.t



#'kuramoto_config.ini'
def load_kuramotosystem_from_config(filename, oscillators_number):
    config.read(filename)
    lambd = float(config['visible']['lambd'])
    omega_vector = string_to_intvector(config['invisible']['omega_vector'])
    Aij = string_to_intvector(config['invisible']['Aij'])  # boundings Aij
    Aijarray = np.array(Aij)
    Aijarray = np.reshape(Aijarray, [len(omega_vector), len(omega_vector)])
    phase_vector = string_to_intvector(config['invisible']['phase_vector'])

    #omega_vector = omega_vector[0:oscillators_number]
    Aijarray = Aijarray[0:oscillators_number][0:oscillators_number]
    #phase_vector = phase_vector[0:oscillators_number]

    t0 = int(config['invisible']['t0'])
    tf = int(config['invisible']['tf'])
    N = int(config['invisible']['N'])  # h = (t0 - tf) / N  time discretisation  coefficient, NOT THE OSCILLATORS NUMBER
    #print('rank :' + str(rank),' shell', str(phase_vector))
    return cls.KuramotoSystem(omega_vector, lambd, Aijarray, phase_vector, t0, tf, N, oscillators_number)

def string_to_intvector(string):
    """
    please write numbers in config with ' ' SPLIT
    :param string:
    :return: intvector
    """
    strvector = string.split(' ')
    intvector = [float(strvector[i]) for i in range(len(strvector))]
    #print(intvector)
    return intvector

def get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number):
    """
    camculate parametr r
    :param time_output_array_length:
    :param pendulum_phase_output_array:
    :param oscillators_number:
    :return:
    """
    r = np.zeros(time_output_array_length)
    for i in range(time_output_array_length):
        sum_cos = 0
        sum_sin = 0
        k = 0
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

        k +=1

    return r

if __name__ == '__main__':
    #-----------greeting---------
    #print("""program name\n programm version\n authors\n data realise \n""")

    #-----------input-------------
    config_filename = 'kuramoto_config.ini' #input("general_config_filename.ini\n")    # kuramoto_config.ini
    #minor_config_filename = input("minor_config_filename.ini\n")

    #-----------config_interations--------
    config = configparser.ConfigParser()
    config.read(config_filename)                                #loading from config section
    oscillators_number = int(config['visible']['oscillators_number'])

    #-----------testing for oscillators_number oscillator system--------
    #loading
    kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config_filename, oscillators_number) #= i+1)

    #calculate
    if rank == 0:
        timer = Timer().start()

    pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution_iterator() #system with 1~10 pendulums

    #write in file
    time_output_array_length = len(pendulum_time_output_array)
    pendulum_phase_output_array = np.array(pendulum_phase_output_array).reshape((time_output_array_length, oscillators_number))
    pendulum_phase_output_array = pendulum_phase_output_array % (2*math.pi)
    pendulum_phase_output_array = np.array([[math.sin(i) for i in e] for e in pendulum_phase_output_array])     ###### cut this string out for radian graph

    if rank==0 :
        print("Calculate time", timer.stop())       ####### dont delete
        print("oscillators_number ",oscillators_number)
        with open("test_txt//test"+str(oscillators_number)+".txt", "w") as myfile:
            for i in range(time_output_array_length):
                myfile.write(str(pendulum_time_output_array[i])+" "+str( pendulum_phase_output_array[i] )+"\n")

    # ------------calculating r(lambd)-------------
    r = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)
    if rank==0 :
        with open("test_txt//test_r"+str(oscillators_number)+".txt", "w") as myfile:
            for i in range(time_output_array_length):
                myfile.write(str(pendulum_time_output_array[i])+" "+str( r[i] ).replace("," , " ").replace("[" , " ").replace("]" , "" )+"\n")

    pp.plot(pendulum_time_output_array, r)
    pp.show()
    '''----------its another progect----------#TODO plot r(lambda)  lambda~~all_coupling_map
    lambdamin = 0
    lamdamax = 2.5
    step = 0.05
    for i in range(lambdamin,lamdamax, step):
        #loading
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config_filename, oscillators_number) #system with 10 pendulums, ONLY 10!

        #calculate

    '''

#unknown Loopies
