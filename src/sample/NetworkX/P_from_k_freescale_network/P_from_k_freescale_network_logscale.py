import networkx
import networkx as nx
import numpy as np
import pandas as pd

from matplotlib import pyplot
from matplotlib import pyplot as plt


# this section search standart diagram

def find_rank_diagram_series(Aij_2d_adjacency_matrix):
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

    def count_all_elements_with_the_same_value_in_1d_matrix(matrix_of_1d):
        nodRankSeries = pd.value_counts(matrix_of_1d).sort_index().reset_index()
        values_list, number_of_encountering_list = tuple(nodRankSeries.values.T)
        return values_list, number_of_encountering_list

    # Compute a histogram of the counts of non-null values.
    nodRankSeries = pd.value_counts(list_of_node_neighbours_number).sort_index().reset_index()

    return tuple(nodRankSeries.values.T)

# next we make it log sclae and ordinat-normalized

def make_graph(graph_number_to_choose,
               osc_number=1000,
               neighbours = 10,
               connectionProb = 1.,
               ):
    graph = [
        networkx.watts_strogatz_graph(osc_number, neighbours, connectionProb),
        nx.barabasi_albert_graph(osc_number, neighbours),
        networkx.fast_gnp_random_graph(osc_number, connectionProb),
        networkx.fast_gnp_random_graph(osc_number, p=1)
    ]
    return graph[graph_number_to_choose]

def linear_aproximate(x,y):
    poloinomial_coeffitients = np.polyfit(x, y, 1)
    print(poloinomial_coeffitients)
    poly_function = np.poly1d(poloinomial_coeffitients)


    def linear_function(x):
        y = x*poloinomial_coeffitients[0] + poloinomial_coeffitients[1]
        return y
    x1 = np.min(x)
    y1 = linear_function(x1)
    x2 = np.max(x)
    y2 = linear_function(x2)

    print(x,y)
    line = poly_function(x)

    plt.plot([x1,x2], [y1, y2], 'r-')


if __name__ == '__main__':
    G = make_graph(1)
    Aij = nx.to_numpy_array(G)
    diagram_data = (find_rank_diagram_series(Aij))

    def compute_x_and_y_from(data):
        x = (data[0])                         ###########!!!!!!!!
        y = (data[1])/(max(data[1])) #########!!!!!!!!!!
        new_data = x, y
        return new_data

    new_diagram_data = compute_x_and_y_from(diagram_data)

    # def do_linear_aproximation_plot(diagram_data): #########!!!!!!!!!!!!!! sma plot but with OK axes
    #     linear_aproximate(*diagram_data) ###!!!!!!!!


    def draw_main_plot(diagram_data):
        plt.plot(*diagram_data, ".")


    # do_linear_aproximation_plot(np.copy(new_diagram_data)) #!!!!!!!!!!!
    draw_main_plot(np.copy(new_diagram_data))

    plt.grid()
    plt.xscale("log") #!!!!!!!!!!!!!!!!!
    plt.yscale("log") #!!!!!!!!!!!!!
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.show()