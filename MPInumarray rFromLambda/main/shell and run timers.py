import KuramotoSystem as cls
import configparser
config = configparser.ConfigParser()
import numpy as np
import math





#'kuramoto_config.ini'
def load_kuramotosystem_from_config(filename, oscillators_number, lambd4r = None):
    config.read(filename)
    lambd = float(config['visible']['lambd'])
    omega_vector = string_to_intvector(config['invisible']['omega_vector'])
    Aij = string_to_intvector(config['invisible']['Aij'])  #boundings Aij
    Aijarray = np.array(Aij)
    Aijarray = np.reshape(Aijarray, [len(omega_vector),len(omega_vector)])
    phase_vector = string_to_intvector(config['invisible']['phase_vector'])

    omega_vector = omega_vector[0:oscillators_number]
    Aijarray = Aijarray[0:oscillators_number][0:oscillators_number]
    phase_vector = phase_vector[0:oscillators_number]

    t0 = int(config['invisible']['t0'])
    tf = int(config['invisible']['tf'])
    N = int(config['invisible']['N'])   #h = (t0 - tf) / N  time discretisation  coefficient, NOT THE OSCILLATORS NUMBER
    if lambd4r != None:
        lambd = lambd4r
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
    lambd = float(config['visible']['lambd'])

    # TODO write programm processing timer
    """
    #-----------testing from 1 oscillator system to "oscillators_number" oscillators system--------
    for i in range(oscillators_number):
        #loading
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config_filename, oscillators_number = i+1)

        #calculate
        pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution_iterator() #system with 1~10 pendulums

        #write in file
        with open("test_txt//test"+str(i)+".txt", "w") as myfile:
            myfile.write(str(pendulum_time_output_array)[1:-1]+"\n"+ str(pendulum_phase_output_array)[1:-1]+"\n")
    """
    #------------calculating r(lambd)-------------
    #TODO plot r(lambda)  lambda~~all_coupling_map
    lambdamin = 0
    lamdamax = lambd
    step = 0.005

    myfile = open("test_txt//test" + str(0) + ".txt", "w")  #opening file
    for i in range(round(lamdamax/step)+1):
        #loading
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config_filename, oscillators_number, lambd4r = i*step) #system with 10 pendulums, ONLY 10!

        #calculate tetas
        pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution_iterator()

        with open("test_txt//test sys side" + str(oscillators_number) + ".txt", "w") as mfile:
            for j in range(0, (len(pendulum_time_output_array))):
                mfile.write(str(pendulum_time_output_array[j]) + " " + ( str(pendulum_phase_output_array[j * (oscillators_number):(j + 1) * (oscillators_number)])[1:-1]).replace(",", " ") + "\n")

        # calculating r(lambd)
        summcos = 0
        summsin = 0
        for teta in pendulum_phase_output_array[-(oscillators_number+1):-1]: #last step calculation result
            summcos += math.cos(teta)
            summsin += math.sin(teta)
        x = (summcos/oscillators_number)**2
        y = (summsin/oscillators_number)**2
        r = (x + y)**0.5

        #write string to file
        myfile.write(str(i*step) + " " + str(r) + "\n")
    #------------write to file------------


#unknown Loopies
