import random
import configparser
import networkx
from matplotlib import pyplot
import networkx.algorithms.community as community


def create_config(*args,
                  lambd=0.7,
                  oscillators_number=10,
                  start_time=0,
                  final_time=100,
                  iteration_number=200,
                  filename=None,
                  topology="fullyConnected",
                  reconnectionProbability=0.15,
                  neighbours=10,
                  community_number_to_detect=None):
    """
    create config of the graph
    :param lambd: special parameter
    :param oscillators_number: number of nods is graph
    :param filename: writing in a file `filename` (optional)
    :param topology: graph topology to create
    :param reconnectionProbability:  probability of random connections
    :param neighbours: optional parameter for certain type of graphs
    :param community_number_to_detect: optional parameter for certain type of graphs
    :return: config dictionary
    """
    config = {}
    config['oscillators_number'] = oscillators_number
    config['lambd'] = lambd
    config['omega_vector'] = [round(random.uniform(0.05, 0.2), 2) for i in range(oscillators_number)]

    m2 = 2 # must be even
    # precalculations for barbell_graph
    m1 = oscillators_number// 2- m2//2


    topologydict = {
        "fullyConnected".lower(): lambda: networkx.complete_graph(oscillators_number),
        "random".lower(): lambda: networkx.fast_gnp_random_graph(oscillators_number, reconnectionProbability),
        "freeScaling".lower(): lambda: networkx.scale_free_graph(oscillators_number),
        "smallWorld".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, reconnectionProbability),
        "regular".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, 0),
        "barbell".lower(): lambda: networkx.barbell_graph(m1, m2)
    }
    config['topology'] = topologydict[topology.lower()]()
    config['Aij'] = networkx.to_numpy_array(config['topology'])
    config['phase_vector'] = [round(random.uniform(0, 12), 2) for i in range(oscillators_number)]
    config['t0'] = start_time
    config['tf'] = final_time
    config['N'] = iteration_number  #iteration count
    config['h'] = (config['tf']-config['t0'])/config['N']

    # community detection
    if community_number_to_detect is not None:
        communities_generator = community.girvan_newman(config['topology'])
        for i in range(community_number_to_detect - 1):
            next_level_communities = next(communities_generator)
        config['community_list'] = sorted(map(sorted, next_level_communities))

    # write config in file
    if filename is not None:
        config_root = configparser.ConfigParser()
        config_root['config'] = config
        with open(filename, 'w') as myfile:
            config_root.write(myfile)

    return config

if __name__=="__main__":
    oscillators_number = 10
    community_number_to_detect = 3
    config = create_config(oscillators_number=oscillators_number, topology="smallWorld", reconnectionProbability=0.1, neighbours=5)


    pos = networkx.drawing.fruchterman_reingold_layout(config['topology'])
    networkx.draw_networkx(config['topology'], pos)
    pyplot.show()



