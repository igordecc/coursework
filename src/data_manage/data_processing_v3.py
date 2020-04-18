import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

def file_read(path):
    dir = os.path.dirname(path)
    if os.path.exists(path):
        with open(path, "rb") as file:
            return pickle.load(file)

def log_to_data(osc_n, topology, dl):
    path = "{2}\\{1}\\r_from_lambd_mean_{0}_{3}".format(osc_n, topology, "log", dl)
    return file_read(path)

def read_systems(topology="regular_sw", dl=1, list_osc_n= range(100, 501, 100)):
    x = log_to_data(list_osc_n[0], topology, dl)[0] #lambda_vector
    y = [log_to_data(osc_n, topology, dl)[1] for osc_n in list_osc_n] # r_mean_multiple
    return x, y


#====================
def cut_the_end(x,y, start_from_l=5):
    x = x[x<start_from_l]
    y = [yi[:len(x)] for yi in y]
    return x,y




def r_l_multi(topology="smallworld", dl=1, fmt=".", max_l=None):
    x,y = read_systems(topology=topology, dl=1,list_osc_n= range(100, 501, 50))
    if max_l:
        x, y = cut_the_end(x,y,start_from_l=max_l)

    for yi in y:
        plt.plot(x,yi, fmt)
    plt.grid()
    img_path = "{0}\\{1}\\r_from_lambd_multi_osc_{1}".format("img", topology)
    plt.xlabel("lambda")
    plt.ylabel("r")
    plt.savefig(img_path)
    plt.close()

if __name__ == '__main__':
    r_l_multi(topology="smallworld", dl=1, fmt="-", max_l=30)
    # experiment_multigraph(topology="fullyconnected", dl=1, fmt="-", max_l=3)
    # experiment_multigraph(topology="random",         dl=1, fmt="-", max_l=3)
