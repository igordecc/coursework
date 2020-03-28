import os
import pickle
def file_read(path):
    dir = os.path.dirname(path)
    if os.path.exists(path):
        with open(path, "rb") as file:
            return pickle.load(file)


def log_to_data(osc_n, topology):
    path = "{2}\\{1}\\r_from_lambd_mean_{0}".format(osc_n, topology, "log")
    return file_read(path)


def experiment_1():
    r_critical = 0.95
    topology = "random_sw"
    # topology = "regular_sw"
    # topology = "smallworld"

    lambd_critical = []
    list_osc_n = range(100, 501, 100)
    for osc_n in list_osc_n:
        lamd_vector, r_mean = log_to_data(osc_n, topology)
        lambd_critical.append([lamd_vector[i] for i in range(len(r_mean)) if r_mean[i] >= r_critical][0])
    print(lambd_critical)


if __name__ == '__main__':
    experiment_1()

