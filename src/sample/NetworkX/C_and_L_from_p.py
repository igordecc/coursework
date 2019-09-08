import networkx
import networkx as nx
import numpy as np
import pandas as pd

from matplotlib import pyplot
from matplotlib import pyplot as plt


def make_graph(i,
               osc_number=1000,
               neighbours = 10,
               connectionProb = 1.,
               ):
    graph = [
        networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb),
        nx.barabasi_albert_graph(200,3),
        networkx.fast_gnp_random_graph(osc_number, connectionProb),
        networkx.fast_gnp_random_graph(osc_number, p=1)
    ]
    return graph[i]


def compute_C_and_L_for_p(connectionProb = 0):
    G = make_graph(0, connectionProb=connectionProb)
    C = nx.average_clustering(G)
    L = nx.average_shortest_path_length(G)
    # nx.draw(G)
    # plt.show()
    print(connectionProb)
    return C, L


def make_probability_list(
        number_of_dots_on_the_plot = 10,
        lower_border = -4,
        hight_border = 0):
    # lets create p= 10**-4 -> 10^0
    dpower = abs(lower_border / number_of_dots_on_the_plot)
    power_list = np.arange(lower_border, hight_border + dpower, dpower)
    p_probability_list = 10**power_list
    return p_probability_list


if __name__ == '__main__':
    prob_list = make_probability_list()
    C_and_L_list = list(map(compute_C_and_L_for_p, prob_list))
    C_and_L_for_normalisation = compute_C_and_L_for_p(0)
    C_and_L_list_normalised = [ (i[0]/C_and_L_for_normalisation[0], i[1]/C_and_L_for_normalisation[1]) for i in C_and_L_list]

    C_and_L = np.array(C_and_L_list_normalised).T

    plt.plot(prob_list, C_and_L[0], ".-", label="С(p)/C(0)")
    plt.plot(prob_list, C_and_L[1], ".-", label="L(p)/L(0)")
    plt.xscale("log")
    plt.xlabel("p")
    plt.grid()
    plt.legend()
    plt.show()

    # print(C_and_L_list_normalised)





