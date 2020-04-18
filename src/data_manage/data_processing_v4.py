import pickle
import matplotlib.pyplot as plt
import os


def file_read(path):
    if os.path.exists(path):
        with open(path, "rb") as file:
            print(f"path {path}")
            return pickle.load(file)


def compile_path(experiment_folder, osc_n, topology, dl):
    file = f"r_from_lambd_mean_{osc_n}_{dl}"
    path = os.path.join(f"{experiment_folder}", "data", f"{topology}")
    complete_path = os.path.join(path, file)
    return complete_path


def read_systems(folder_name, topology, dl=1, list_osc_n=range(100, 501, 100)):
    """
    read multiple systems at once
    :param folder_name:
    :param topology:
    :param dl:
    :param list_osc_n:
    :return: x lambd, y [r1_list, r2_list, r3_list,...]
    """
    _path = compile_path(folder_name, list_osc_n[0], topology, dl)
    x = file_read(_path)[0]     # lambda_vector
    _path_list = [compile_path(folder_name, osc_n, topology, dl) for osc_n in list_osc_n]
    y = [file_read(_path)[1] for _path in _path_list]   # r_mean_multiple
    return x, y


def cut_the_right_side_of_x(x, y, start_from_l=5):
    x = x[x<start_from_l]
    y = [yi[:len(x)] for yi in y]
    return x,y


def experiment_multigraph(folder_name, topology, dl=1, fmt=".", max_l=None):
    """

    :param folder_name:
    :param topology:
    :param dl:
    :param fmt:
    :param max_l:
    :return:
    """

    x,y = read_systems(folder_name, topology=topology, dl=1,list_osc_n= range(100, 501, 50))

    if max_l:
        x, y = cut_the_right_side_of_x(x, y, start_from_l=max_l)

    # plot section
    for yi in y:
        plt.plot(x,yi, fmt)
    plt.grid()
    plt.xlabel("lambda")
    plt.ylabel("r")

    # save section
    img_path = os.path.join(folder_name, "plots", topology, "multigraph")
    plt.savefig(img_path)
    plt.close()

#====================
import numpy
def critical_r(r_critical= 0.80, topology= "regular_sw", list_osc_n= range(100, 501, 100)):
    lambd_critical = numpy.empty(len(list_osc_n))
    i = 0
    for osc_n in list_osc_n:
        lamd_vector, r_mean = read_systems(osc_n, topology)
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

if __name__ == '__main__':

    experiment_multigraph("exp1", topology="small_world", dl=1, fmt="-", max_l=30)
