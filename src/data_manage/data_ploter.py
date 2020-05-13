"""
import csv data to initial conditions
"""
import sys
sys.path.append("..")

import pandas
import argparse
import numpy

import networkx
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser("Drag and drop data to the data_importer.py file")

    parser.add_argument("file_list", type=str, nargs="+")
    args = parser.parse_args()

    working_dir = "export_graphs"
    for file in args.file_list:
        try:
            with open(file) as csv_input_file:
                adjacency_matrix = pandas.read_csv(csv_input_file, header=None).values

                numpy.set_printoptions(threshold=sys.maxsize)
                print(adjacency_matrix)

                graph_obj = networkx.Graph(adjacency_matrix)
                pos = networkx.drawing.fruchterman_reingold_layout(graph_obj.to_undirected())
                networkx.draw_networkx(graph_obj.to_undirected(), pos)
                plt.show()
        except:
            print(f"unexpected error {sys.exc_info()[0]}")


if __name__ == '__main__':
    main()