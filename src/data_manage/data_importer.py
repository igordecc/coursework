"""
import csv data to initial conditions
"""
import sys
sys.path.append("..")

import pandas
import argparse
from data_mining import r_mean_experiment
from config.config_creator import NetworkConfig
from main.OCL_r import KuramotoSystem


def main():
    parser = argparse.ArgumentParser("Drag and drop data to the data_importer.py file")

    parser.add_argument("file_list", type=str, nargs="+")
    args = parser.parse_args()

    working_dir = "export_graphs"
    solver = KuramotoSystem()
    for file in args.file_list:

        with open(file) as csv_input_file:
            adjacency_matrix = pandas.read_csv(csv_input_file, header=None).values

        r_mean_experiment(
            working_dir, solver,
            network_properties=dict(adjacency_matrix=adjacency_matrix),
            min_lambda=0, max_lambda=100, step_lambda=.1,
            n_networks=20
        )

    input()


if __name__ == '__main__':
    try:
        main()
    except:
        input()
