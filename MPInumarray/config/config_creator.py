import random
import configparser
import networkx


def create_config(lambd=0.7, oscillators_number=10, filename='kuramoto_config.ini', topology="smallWorld"):
    """

    :param topology:
    :param lambd:
    :param oscillators_number:
    :param filename:
    :param topology: fullyConnected, random, freeScaling, smallWorld.
    :return: config dictionary
    """
    config = {}
    config['oscillators_number'] = oscillators_number
    config['lambd'] = lambd
    config['omega_vector'] = [round(random.uniform(0.05, 0.2), 2) for i in range(oscillators_number)]

    connectionProbability = 0.6     # probability of random connections
    neighbours = 4
    topologydict = {
        "fullyConnected": [[(1 if i != j else 0) for j in range(oscillators_number)] for i in range(oscillators_number)],
        "random": [[1 if (random.random() < connectionProbability) and (i != j) else 0 for j in range(oscillators_number)] for i in range(oscillators_number)],
        "freeScaling": [networkx.to_numpy_array(networkx.scale_free_graph(oscillators_number))],
        "smallWorld": [networkx.to_numpy_array(networkx.watts_strogatz_graph(oscillators_number, neighbours, connectionProbability))],
    }
    config['Aij'] = [[(1 if i != j else 0) for j in range(oscillators_number)] for i in range(oscillators_number)] #topologydict[topology]
    config['phase_vector'] = [round(random.uniform(0, 12), 2) for i in range(oscillators_number)]
    config['t0'] = 0
    config['tf'] = 100
    config['N'] = 200  #iteration count
    config['h'] = (config['tf']-config['t0'])/config['N']

    if filename is not None:
        config_root = configparser.ConfigParser()
        config_root['config'] = config
        with open(filename, 'w') as myfile:
            config_root.write(myfile)

    return config

#
# def create_config(oscillators_number):
#
#     kuramoto_config = open('kuramoto_config.ini', 'w')
#
#     kuramoto_config.write("""[DEFAULT]\n\n[visible]\n\n""")
#     #-----------------------------
#     #oscillators_number = 112
#     #----------------------------
#     kuramoto_config.write("oscillators_number = " + str(oscillators_number) + "\n")    #N ~~ oscillators_number
#     kuramoto_config.write("lambd = " + "0.05" + "\n")    #lambd ~~ lambd ~~ all coupling map
#     kuramoto_config.write("""\n[invisible]\n""")
#     #----------omega_vector----------------
#     omega_vector = ''
#     for i in range(oscillators_number):
#         omega_vector += ' ' + str(round(random.uniform(0.05, 0.2), 2)) #DONT TOCH
#
#     kuramoto_config.write("omega_vector = " + omega_vector + "\n") #omega_i ~~ omega_wector[i]
#     #--------------------------
#     #-----------Aij---------------
#     Aij = ''
#     for i in range(oscillators_number):
#         #Aij += "\n"
#         for j in range(oscillators_number):
#             #Aij += ' ' + str(1)
#             if i!=j:
#                 Aij += ' ' + str(1)
#             else:
#                 Aij += ' ' + str(0) #str(round(random.uniform(0,1), 2))
#     kuramoto_config.write("Aij = " + Aij + "\n") #A_ij ~~ oscillators_number^2   NOW enabled
#     #--------------------------
#
#     #-----------phase_vector---------------
#     phase_vector = ''
#     for i in range(oscillators_number):
#         phase_vector += ' ' + str(round(random.uniform(0, 12), 2)) #str((i+1) * 0.1)#
#     kuramoto_config.write("phase_vector = " + phase_vector + "\n") #teta_i ~~ phase_vector[i]
#     #--------------------------
#
#     kuramoto_config.write("""t0 = 0\ntf = 100\nN = 1000""")
#     """
#     5 oscillators = 0.3196
#     10 = 0.4721
#     50 = 4.1638
#     75 = 8.4893
#     100 oscillators = 14.8766
#     112 = 19.0881
#     """
#     kuramoto_config.close()

if __name__=="__main__":
    oscillators_number = 112
    create_config(oscillators_number)