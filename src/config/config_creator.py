import random
import configparser
import networkx


def create_config(lambd=0.7, oscillators_number=10, filename='kuramoto_config.ini', topology="fullyConnected"):
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
        "fullyConnected".lower(): lambda: networkx.fast_gnp_random_graph(oscillators_number, p=1),
        "random".lower(): lambda: networkx.fast_gnp_random_graph(oscillators_number, connectionProbability),
        "freeScaling".lower(): lambda: networkx.scale_free_graph(oscillators_number),
        "smallWorld".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, connectionProbability),
    }
    config['topology'] = topologydict[topology.lower()]()
    config['Aij'] = networkx.to_numpy_array(config['topology'])
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

if __name__=="__main__":
    oscillators_number = 112
    create_config(oscillators_number)