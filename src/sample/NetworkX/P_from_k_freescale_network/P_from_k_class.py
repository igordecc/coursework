import networkx
import networkx as nx
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt


# this section search standart diagram

def compute_rank_diagram(Aij_2d_adjacency_matrix):
    """
    1. count for all nods number of dependencies (1- CONNECTION 0 - NO CONNECTION)
    2. with pandas count number of nods with each rank

    :param Aij_2d_adjacency_matrix: insert Adjacency matrix Aij
    :return: diagram data
    """
    """
    why?
    we need the plot "chance to meet the node from number of the node neighbours"
    """

    def function_counts_connections_number_for_one_node_for_every_node(Aij_2d_adjacency_matrix):
        counted_neighbours_list = []
        for i in range(Aij_2d_adjacency_matrix.shape[0]):
            node_neighbours_number_counter = 0
            for j in range(Aij_2d_adjacency_matrix.shape[1]):
                if Aij_2d_adjacency_matrix[i][j]:
                    node_neighbours_number_counter += 1
            counted_neighbours_list.append(node_neighbours_number_counter)
        counted_neighbours_list = np.array(counted_neighbours_list)  # to numpy array
        return counted_neighbours_list

    list_of_node_neighbours_number = function_counts_connections_number_for_one_node_for_every_node(Aij_2d_adjacency_matrix)

    # Compute a histogram of the counts of non-null values.
    nodRankSeries = pd.value_counts(list_of_node_neighbours_number).sort_index().reset_index()

    return tuple(nodRankSeries.values.T)

# next we make it log sclae and ordinat-normalized

def make_graph(graph_number_to_choose,
               osc_number=1000,
               neighbours=100,
               reconnection_prob=0.1,
               ):
    graph = [
        networkx.watts_strogatz_graph(osc_number, neighbours, reconnection_prob),
        nx.barabasi_albert_graph(osc_number, neighbours),
        networkx.fast_gnp_random_graph(osc_number, reconnection_prob),
        networkx.fast_gnp_random_graph(osc_number, p=1)
    ]
    return graph[graph_number_to_choose]


def linear_function(x, coefficients):
    y = x * coefficients[0] + coefficients[1]
    return y


def linear_approximate(x, y):
    poloinomial_coeffitients = np.polyfit(x, y, 1)

    polyfit_function = np.poly1d(poloinomial_coeffitients)
    funced_y = polyfit_function(x)

    print(poloinomial_coeffitients)
    new_y = linear_function(x,poloinomial_coeffitients)
    # plt.plot(x, new_y, "m-")
    plt.plot(x, funced_y, "r-")


def quadratic_approximate(x, y):
    poloinomial_coeffitients = np.polyfit(x, y, 2)

    polyfit_function = np.poly1d(poloinomial_coeffitients)
    funced_y = polyfit_function(x)

    print(poloinomial_coeffitients)
    new_y = linear_function(x,poloinomial_coeffitients)
    # plt.plot(x, new_y, "m-")
    plt.plot(x, funced_y, "r-")


def cubic_approximate(x, y):
    poloinomial_coeffitients = np.polyfit(x, y, 3)

    polyfit_function = np.poly1d(poloinomial_coeffitients)
    funced_y = polyfit_function(x)

    print(poloinomial_coeffitients)
    new_y = linear_function(x,poloinomial_coeffitients)
    # plt.plot(x, new_y, "m-")
    plt.plot(x, funced_y, "r-")


def compute_percentage_diagram_in_log_scale(data):
    x = np.log10(data[0])
    y = np.log10(data[1]/np.sum(data[1]))
    new_data = x, y
    return new_data

def compute_percentage_diagram(data):
    x = data[0]
    y = data[1]/np.sum(data[1])
    new_data = x, y
    return new_data




class RankDiagram():
#=============== init part
    def __init__(self, adjacency_matrix, ):
        self.adjacency_matrix = adjacency_matrix

        self.compute_rank_diagram(self.adjacency_matrix)     # self.diagram_data =

        self.diagram_data_for_approximation = np.copy(self.diagram_data)

    def compute_rank_diagram(self, Aij_2d_adjacency_matrix):
        """
        1. count for all nods number of dependencies (1- CONNECTION 0 - NO CONNECTION)
        2. with pandas count number of nods with each rank

        :param Aij_2d_adjacency_matrix: insert Adjacency matrix Aij
        :return: diagram data
        """
        """
        why?
        we need the plot "chance to meet the node from number of the node neighbours"
        """

        def function_counts_connections_number_for_one_node_for_every_node(Aij_2d_adjacency_matrix):
            counted_neighbours_list = []
            for i in range(Aij_2d_adjacency_matrix.shape[0]):
                node_neighbours_number_counter = 0
                for j in range(Aij_2d_adjacency_matrix.shape[1]):
                    if Aij_2d_adjacency_matrix[i][j]:
                        node_neighbours_number_counter += 1
                counted_neighbours_list.append(node_neighbours_number_counter)
            counted_neighbours_list = np.array(counted_neighbours_list)  # to numpy array
            return counted_neighbours_list

        list_of_node_neighbours_number = function_counts_connections_number_for_one_node_for_every_node(Aij_2d_adjacency_matrix)

        # Compute a histogram of the counts of non-null values.
        nodRankSeries = pd.value_counts(list_of_node_neighbours_number).sort_index().reset_index()

        self.diagram_data = tuple(nodRankSeries.values.T)   # return tuple(nodRankSeries.values.T)

    def compute_percentage_diagram_in_log_scale(self, data):
        x = np.log10(data[0])
        y = np.log10(data[1] / np.sum(data[1]))
        new_data = x, y
        self.percent_diagram_data = new_data     # return new_data

    def compute_percentage_diagram(self, data):
        x = data[0]
        y = data[1] / np.sum(data[1])
        new_data = x, y
        self.percent_diagram_data = new_data     # return new_data

#================ plot part
    def plot(self, scalling=None, approximation=None, grid=True, plot_view="-"):
        """

        :param approximation: default - None
        linear - linear approximation
        quadratic - quadratic approximation
        cubic - cubic approximation
        :return:
        """
        # choose one
        if scalling == None:
            self.compute_percentage_diagram(self.diagram_data_for_approximation)  # self.percent_diagram_data
        elif scalling == "loglog":
            self.compute_percentage_diagram_in_log_scale(self.diagram_data_for_approximation)     # self.percent_diagram_data


        # choose one
        if approximation:
            if   approximation == "linear":
                self.linear_approximate(*np.copy(self.percent_diagram_data))
            elif approximation == "quadratic":
                self.quadratic_approximate(*np.copy(self.percent_diagram_data))
            elif approximation == "cubic":
                self.cubic_approximate(*np.copy(self.percent_diagram_data))

        plt.plot(*np.copy(self.percent_diagram_data), plot_view)

        if grid:
            plt.grid()

        plt.xlabel("k")
        plt.ylabel("P(k)")
        plt.show()

    def linear_approximate(self, x, y):
        poloinomial_coeffitients = np.polyfit(x, y, 1)

        polyfit_function = np.poly1d(poloinomial_coeffitients)
        funced_y = polyfit_function(x)

        # print(poloinomial_coeffitients)
        plt.plot(x, funced_y, "r-")


    def quadratic_approximate(self, x, y):
        poloinomial_coeffitients = np.polyfit(x, y, 2)

        polyfit_function = np.poly1d(poloinomial_coeffitients)
        funced_y = polyfit_function(x)

        # print(poloinomial_coeffitients)
        plt.plot(x, funced_y, "r-")


    def cubic_approximate(self, x, y):
        poloinomial_coeffitients = np.polyfit(x, y, 3)

        polyfit_function = np.poly1d(poloinomial_coeffitients)
        funced_y = polyfit_function(x)

        # print(poloinomial_coeffitients)
        plt.plot(x, funced_y, "r-")


if __name__ == '__main__':
    G = make_graph(1)
    Aij = nx.to_numpy_array(G)

    # made from Adjacency matrix
    diagram = RankDiagram(Aij)
    diagram.plot(approximation="linear", scalling="loglog", plot_view=".")



