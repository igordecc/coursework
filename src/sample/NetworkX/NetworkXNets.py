"""
Visualiser fro graph statistic
Probe version
need:
    - statistic for 100 same graph at once
    - statistic "like in a book" - with article parameters - for comparison

"""


import networkx
import networkx as nx
import numpy as np
import pandas as pd

from matplotlib import pyplot
from matplotlib import pyplot as plt

osc_number = 50
neighbours = 5
connectionProb = 1.


####______func section_____

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
    listNum = np.array(listNum)     # to numpy array

    # Compute a histogram of the counts of non-null values.
    nodRankSeries = pd.value_counts(listNum).sort_index().reset_index()
    return tuple(nodRankSeries.values.T)


def find_rank_diagram_series_for_Graph(Graph):
    """
    1. count for all nods number of dependencies (1- CONNECTION 0 - NO CONNECTION)
    2. with pandas count number of nods with each rank

    :param Aij: insert Adjacency matrix Aij
    :return: diagram data
    """
    Aij = nx.to_numpy_array(Graph)

    listNum = []
    for i in range(Aij.shape[0]):
        conNumNode = 0
        for j in range(Aij.shape[1]):
            if Aij[i][j]:
                conNumNode += 1
        listNum.append(conNumNode)
    listNum = np.array(listNum)     # to numpy array

    # Compute a histogram of the counts of non-null values.
    nodRankSeries = pd.value_counts(listNum).sort_index().reset_index()

    # Compute hand-writen
    summed_1d_Aij = np.sum(Aij, 0)
    print(np.unique(summed_1d_Aij))

    return tuple(nodRankSeries.values.T)





#-------------------------


###______variant_1___________
"""
1. define all functions
2. make function list to fast call them
"""
def smallworld_stats():
    Graph = networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb)
    centrality = nx.degree_centrality(Graph).values()
    print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
    print("graph degree_histogram: ", Graph.degree())
    print("graph diameter: ",nx.diameter(Graph))
    print("graph clustering coefficient: ", nx.average_clustering(Graph))
    # networkx.draw(a)
    # pyplot.show()
    print("Numpy Aij matrix ")
    print(networkx.to_numpy_array(Graph))


def freescaling_stats():
    bb = nx.barabasi_albert_graph(200,3)
    networkx.draw(bb)
    pyplot.show()
    centrality = nx.degree_centrality(bb).values()
    print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
    print("graph degree_histogram: ", bb.degree())
    print("graph diameter: ",nx.diameter(bb))
    print("graph clustering coefficient: ", nx.average_clustering(bb)) #### EROR


def randomnet_stats():
    c = networkx.fast_gnp_random_graph(osc_number, connectionProb)
    # networkx.draw(c)
    # pyplot.show()
    centrality = nx.degree_centrality(c).values()
    print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
    print("graph degree_histogram: ", c.degree())
    print("graph diameter: ",nx.diameter(c))
    print("graph clustering coefficient: ", nx.average_clustering(c))
    # print(networkx.to_numpy_array(c))


def fullyconected_stats():
    d = networkx.fast_gnp_random_graph(osc_number, p=1)
    # networkx.draw(d)
    # pyplot.show()
    centrality = nx.degree_centrality(d).values()
    print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
    print("graph degree_histogram: ", d.degree())
    print("graph diameter: ",nx.diameter(d))
    print("graph clustering coefficient: ", nx.average_clustering(d))
    # print(networkx.to_numpy_array(d))


stats = [smallworld_stats,
         freescaling_stats,
         randomnet_stats,
         fullyconected_stats]

#######__variant_two_________________
"""
1. define all graph
2. make one universal statistic "display_stat" function - for fast changing properties of showing stats
"""
graph = [
    networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb),
    nx.barabasi_albert_graph(200,3),
    networkx.fast_gnp_random_graph(osc_number, connectionProb),
    networkx.fast_gnp_random_graph(osc_number, p=1)
]

def display_stats(Graph):
    # centrality = nx.degree_centrality(Graph).values()
    # print("graph degree_centrality, max: ", max(centrality), " ; min: ", min(centrality))
    # print("graph degree_histogram: ", Graph.degree())
    # print("graph diameter: ", nx.diameter(Graph))
    # print("graph clustering coefficient: ", nx.average_clustering(Graph))


    # networkx.draw(Graph)
    # pyplot.show()
    # pyplot.clf()

    fig, ax = plt.subplots(1,1)

    position_list, data = find_rank_diagram_series_for_Graph(Graph)

    def do_data_series(data_size):
        data_2d_array = []
        for i in range(data_size):
            position, data = find_rank_diagram_series_for_Graph(Graph)
            data_2d_array.append(data)
        multidata_per_position = np.array(data_2d_array)
        return multidata_per_position


    data = do_data_series(data_size=100)
    ax.violinplot(data)


    # pyplot.plot(*find_rank_diagram_series_for_Graph(Graph), ".")
    pyplot.show()
##_______________________

if __name__ == '__main__':
    # display_stats(graph[0])
    nx.draw(graph[0])
    plt.show()