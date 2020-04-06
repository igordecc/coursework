import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
def file_read(path):
    dir = os.path.dirname(path)
    if os.path.exists(path):
        with open(path, "rb") as file:
            return pickle.load(file)


def log_to_data(osc_n, topology):
    path = "{2}\\{1}\\r_from_lambd_mean_{0}".format(osc_n, topology, "log")
    return file_read(path)

def read_systems(topology="regular_sw", list_osc_n= range(100, 501, 100)):
    x = log_to_data(list_osc_n[0], topology)[0] #lambda_vector
    print(x)
    y = [log_to_data(osc_n, topology)[1] for osc_n in list_osc_n] # r_mean_multiple
    return x, y

#====================
def critical_r(r_critical= 0.80, topology= "regular_sw", list_osc_n= range(100, 501, 100)):
    lambd_critical = np.empty(len(list_osc_n))
    i = 0
    for osc_n in list_osc_n:
        lamd_vector, r_mean = log_to_data(osc_n, topology)
        lambd_higher_cr = [lamd_vector[i] for i in range(len(r_mean)) if r_mean[i] >= r_critical]
        if len(lambd_higher_cr) > 0:
            lambd_critical[i] = [lamd_vector[i] for i in range(len(r_mean)) if r_mean[i] >= r_critical][0]
        else:
            lambd_critical[i] = None
        i += 1

    print("topology: {1}, critical r: {0}".format(lambd_critical, topology))
    return  list_osc_n, lambd_critical


def experiment_crit_lambd():
    pl1 = critical_r(r_critical=0.95, topology="regular_sw", list_osc_n=range(100, 501, 50))
    pl2 = critical_r(r_critical=0.95, topology="smallworld", list_osc_n=range(100, 501, 50))
    pl3 = critical_r(r_critical=0.95, topology="random_sw", list_osc_n=range(100, 501, 50))
    plt.plot(*pl1, ".-")
    plt.plot(*pl2, ".-")
    plt.plot(*pl3, ".-")
    plt.xlabel("oscillator number")
    plt.ylabel("lambda critical")
    plt.grid()
    img_path = "{0}\\lambd_crit_from_osc_1".format("img")
    plt.savefig(img_path)


def experiment_r_l_multi(topology="smallworld", fmt="."):
    x,y = read_systems(topology=topology, list_osc_n= range(100, 501, 50))
    for yi in y:
        plt.plot(x,yi, fmt)
    plt.grid()
    img_path = "{0}\\{1}\\r_from_lambd_multi_osc_{1}".format("img", topology)
    plt.xlabel("lambda")
    plt.ylabel("r")
    plt.savefig(img_path)
    plt.close()


if __name__ == '__main__':
    # experiment_r_l_multi(topology="smallworld", fmt='-')
    # experiment_r_l_multi(topology="regular_sw", fmt='-')
    experiment_r_l_multi(topology="free_scale" , fmt='-')
    # experiment_r_l_multi(topology="fullyconnected" , fmt='-')
    #
    # experiment_crit_lambd()

