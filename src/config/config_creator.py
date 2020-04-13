import configparser
import os
import random
import pickle

import numpy

import networkx
import networkx.algorithms.community as community

from matplotlib import pyplot


def create_config(
        lambd=0.7,
        oscillators_number=10,
        start_time=0,
        final_time=100,
        iteration_number=200,
        filename=None,
        topology="fullyConnected",
        reconnectionProbability=0.15,
        ageCreationProb = 0.3,
        neighbours=10,
        community_number_to_detect=None
):
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
    # config['omega_vector'] = numpy.array(
    #     [round(random.uniform(0.05, 0.2), 2) for i in range(oscillators_number)],
    #     dtype=numpy.float32
    # )
    config['omega_vector'] = numpy.array(
        [round(random.normalvariate(0, 1), 2) for i in range(oscillators_number)],
        dtype=numpy.float32
    )

    m2 = 2 # must be even
    # precalculations for barbell_graph
    m1 = oscillators_number// 2- m2//2


    topologydict = {
        "fullyConnected".lower(): lambda: networkx.complete_graph(oscillators_number),
        "random".lower(): lambda: networkx.fast_gnp_random_graph(oscillators_number, ageCreationProb),
        "freeScaling".lower(): lambda: networkx.scale_free_graph(oscillators_number),
        "random_sw".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, 1),
        "smallWorld".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, reconnectionProbability),
        "regular_sw".lower(): lambda: networkx.watts_strogatz_graph(oscillators_number, neighbours, 0),
        "barbell".lower(): lambda: networkx.barbell_graph(m1, m2)
    }
    config['topology'] = topologydict[topology.lower()]()
    config['Aij'] = networkx.to_numpy_array(config['topology'], dtype=numpy.float32)
    config['phase_vector'] = numpy.array(
        [round(random.uniform(0, 12), 2) for i in range(oscillators_number)],
        dtype=numpy.float32
    )
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


TOPOLOGIES = {
    "fully_connected": networkx.complete_graph,
    "random": networkx.fast_gnp_random_graph,
    "free_scaling": networkx.scale_free_graph,
    "random_sw": lambda **kwargs: networkx.watts_strogatz_graph(p=1.0, **kwargs),
    "regular_sw": lambda **kwargs: networkx.watts_strogatz_graph(p=0.0, **kwargs),
    "small_world": networkx.watts_strogatz_graph,
    "barbell": lambda **kwargs: networkx.barbell_graph(m1=kwargs["n"] // 2 - 1, m2=2)
}


def create_topology(topology, **kwargs):
    generator = TOPOLOGIES.get(topology)
    if generator is None:
        raise ValueError(f"Topology '{topology}' is not recognized")
    return generator(**kwargs)


class NetworkConfig:

    def __init__(self, **properties):
        self._properties = properties.copy()

        self.topology = properties.pop("topology")

        self.adjacency = networkx.to_numpy_array(
            create_topology(self.topology, **properties), 
            dtype=numpy.float32
        )

        self.omega = numpy.array([
            round(random.uniform(0.05, 0.2), 2)
            for i in range(properties['n'])
        ], dtype=numpy.float32)

        self.phase = numpy.array([
            round(random.uniform(0, 12), 2) 
            for i in range(properties['n'])
        ], dtype=numpy.float32)

    def properties(self):
        return self._properties

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            instance = pickle.load(f)
            if not isinstance(instance, NetworkConfig):
                raise TypeError(f"Wrong type loaded from pickle! Loaded {type(instance)} expected {NetworkConfig}")
            return instance

    @staticmethod
    def create_or_load(path, **properties):
        if os.path.exists(path):
            if os.path.isdir(path):
                raise ValueError(f"{path} is a directory!")
            config = NetworkConfig.load(path)

            if config.properties() != properties:
                raise ValueError(
                    f"Loaded NetworkConfig with different state! Requested: {properties}, got: {config.properties()}"
                )
        else:
            config = NetworkConfig(**properties)
            config.save(path)
        
        return config


if __name__=="__main__":
    oscillators_number = 10
    community_number_to_detect = 3
    config = create_config(oscillators_number=oscillators_number, topology="smallWorld", reconnectionProbability=0.1, neighbours=5)


    pos = networkx.drawing.fruchterman_reingold_layout(config['topology'])
    networkx.draw_networkx(config['topology'], pos)
    pyplot.show()



