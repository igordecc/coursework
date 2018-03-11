import KuramotoSystem as cls
import configparser
import numpy as np
import math
import time
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
def load_kuramotosystem_from_config(filename, oscillators_number, lambd=None):
    config.read(filename)
    if lambd == None:
        lambd = float(config['visible']['lambd'])
    omega_vector = string_to_intvector(config['invisible']['omega_vector'])
    Aij = string_to_intvector(config['invisible']['Aij'])  # boundings Aij
    Aijarray = np.array(Aij)
    Aijarray = np.reshape(Aijarray, [len(omega_vector), len(omega_vector)])
    phase_vector = string_to_intvector(config['invisible']['phase_vector'])

    #omega_vector = omega_vector[0:oscillators_number]
    #Aijarray = Aijarray[0:oscillators_number][0:oscillators_number]
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
    intvector = [float(i) for i in strvector]
    #print(intvector)
    return intvector

def get_r(time_output_array_length, p_array, oscillators_number):
    """
    camculate parametr r
    :param time_output_array_length:
    :param p_array:
    :param oscillators_number:
    :return:
    """
    r = np.zeros(time_output_array_length)
    for i in range(time_output_array_length):
        sum_cos = 0
        sum_sin = 0
        k = 0
        for j in p_array[i]:
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

    lambdamin = 0.05
    lamdamax = 2.5
    step = 0.05
    kuramotosystem_class_exemplar = []
    r_array4lambd = []
    r_accuracy = 5 #will get 5 r elements from r_array, instead of one
    lambd_array = []
    for i in np.arange(lambdamin, lamdamax+step , step):
        # loading
        kuramotosystem_class_exemplar.append(load_kuramotosystem_from_config(config_filename, oscillators_number, lambd = i))
        # calculate
        t_array, p_array = kuramotosystem_class_exemplar[-1].get_solution_iterator()
        
        # transformations
        t_array_len = len(t_array)
        p_array = np.array(p_array).reshape((t_array_len, oscillators_number))
        p_array = p_array % (2 * math.pi)
        p_array = np.array([[math.sin(i) for i in e] for e in p_array])

        #r calculating
        r_array = get_r(t_array_len, p_array, oscillators_number)
        
        # recording
        r_array4lambd.append( r_array[-( r_accuracy + 1 ):-1] )
        lambd_array.append(i)

    lambd_array_len = len(lambd_array)

    # transformation r_array - found everage in each [r,r,r] in r_array4lambd = [[r,r,r], [r,r,r], [r,r,r]]
    r_array4lambd = [np.average(i) for i in r_array4lambd]

    if rank == 0:
        with open("test_txt//testlr5.txt", "w") as myfile:
            for i in range(lambd_array_len):
                myfile.write(str(lambd_array[i])+" "+ str(r_array4lambd[i])+'\n')#" ".join(str(x) for x in r_array4lambd[i])+'\n')


#unknown Loopies
