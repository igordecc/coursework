import KuramotoSystem as cls
import configparser
config = configparser.ConfigParser()
import numpy as np
import time

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

    omega_vector = omega_vector[0:oscillators_number]
    Aijarray = Aijarray[0:oscillators_number][0:oscillators_number]
    phase_vector = phase_vector[0:oscillators_number]

    t0 = int(config['invisible']['t0'])
    tf = int(config['invisible']['tf'])
    N = int(config['invisible']['N'])  # h = (t0 - tf) / N  time discretisation  coefficient, NOT THE OSCILLATORS NUMBER
    return cls.KuramotoSystem(omega_vector, lambd, Aijarray, phase_vector, t0, tf, N)

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
"""XXX
for i in range(oscillators_number):
    new_system = cls.KuramotoSystem(omega_vector, Aij, phase_vector, t0, tf, N)
"""

with open("test_txt//time.txt", "w") as myfile:
    myfile.write('')

if __name__ == '__main__':
    #-----------greeting---------
    print("""program name
    programm version
    authors
    data realise \n""")

    #-----------input-------------
    config_filename = 'kuramoto_config.ini' #input("general_config_filename.ini\n")    # kuramoto_config.ini
    #minor_config_filename = input("minor_config_filename.ini\n")

    #-----------config_interations--------
    config.read(config_filename)                                #loading from config section
    oscillators_number = int(config['visible']['oscillators_number'])

    # TODO write programm processing timer
    #-----------testing from 1 oscillator system to "oscillators_number" oscillators system--------
    for i in range(oscillators_number):
        #loading
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config_filename, oscillators_number = i+1)

        timer = Timer().start()

        #calculate
        pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution_iterator() #system with 1~10 pendulums

        #write in file
        with open("test_txt//test"+str(i)+".txt", "w") as myfile:
            for j in range(0, (len(pendulum_time_output_array))):
                myfile.write(str(pendulum_time_output_array[j])+" "+ ( str( pendulum_phase_output_array[j*(i+1):(j+1)*(i+1)] )[1:-1] ).replace("," , " ")+"\n")

        timer = timer.stop()

        with open("test_txt//time.txt", "a") as myfile:
            myfile.write(str(timer) + "\n")
#print v2.0            for j in range( 1, (len(pendulum_time_output_array)-1) ):
#                myfile.write(str(pendulum_time_output_array)[j]+" "+ str(pendulum_phase_output_array)[j]+"\n")

#print v1.0            myfile.write(str(pendulum_time_output_array)[1:-1]+"\n"+ str(pendulum_phase_output_array)[1:-1]+"\n")
