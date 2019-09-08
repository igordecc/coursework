import networkx
import networkx as nx
import numpy as np
import pandas as pd

from matplotlib import pyplot
from matplotlib import pyplot as plt


# this section search standart diagram

def find_rank_diagram_series(Aij):
    """
    1. count for all nods number of dependencies (1- CONNECTION 0 - NO CONNECTION)
    2. with pandas count number of nods with each rank

    :param Aij: insert Adjacency matrix Aij
    :return: diagram data
    """

    listNum = []
    for i in range(Aij.shape[0]):
        conNumNode = 0
        for j in range(Aij.shape[1]):
            if Aij[i][j]:
                conNumNode += 1
        listNum.append(conNumNode)
    listNum = np.array(listNum)  # to numpy array

    # Compute a histogram of the counts of non-null values.
    nodRankSeries = pd.value_counts(listNum).sort_index().reset_index()
    return tuple(nodRankSeries.values.T)

# next we make it log sclae and ordinat-normalized

def make_graph(i,
               osc_number=1000,
               neighbours = 5,
               connectionProb = 1.,
               ):
    graph = [
        networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb),
        nx.barabasi_albert_graph(osc_number, neighbours),
        networkx.fast_gnp_random_graph(osc_number, connectionProb),
        networkx.fast_gnp_random_graph(osc_number, p=1)
    ]
    return graph[i]


if __name__ == '__main__':
    G = make_graph(1)
    Aij = nx.to_numpy_array(G)
    diagram_data = find_rank_diagram_series(Aij)

    diagram_data = (diagram_data[0] , diagram_data[1]/max(diagram_data[1]))    # y normalisation
    print(*diagram_data)
    plt.plot(*diagram_data)
    plt.grid()
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.show()