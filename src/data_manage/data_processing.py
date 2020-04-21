import pickle
import matplotlib.pyplot as plt
import os
import numpy


def file_read(path):
    if os.path.exists(path):
        with open(path, "rb") as file:
            print(f"path {path}")
            return pickle.load(file)


def read_system(folder_name, topology, osc_n, dl=1,):
    """
    read multiple systems at once
    :return: x lambd, y [r1_list, r2_list, r3_list,...]
    """
    filename = f"r_from_lambd_mean_{osc_n}_{dl}"
    _path = os.path.join(folder_name, "data", topology, filename)
    if not(os.path.exists(_path)):
        raise ValueError(f"Path '{_path}' does not exist")
    x,y = file_read(_path)   # lambda_vector # r_mean_multiple
    return x, y


def cut_the_right_side_of_x(x, y,*args, start_from_l=5):
    x = numpy.array(x)
    y = numpy.array(y)
    x = x[x<start_from_l]
    y = y[:len(x)]
    return x,y

# ====================


def plot_multigraph(plots, xlable:str, ylable:str, img_path:str, fmt="", legend=None, **kwargs):
    """
    plot multiple graphs
    :param plots: (x,y), (x,y), (x,y)
    :return:
    """
    if legend:
        for i, plot in enumerate(plots):
            plt.plot(*plot, fmt, label=legend[i], **kwargs)
            plt.legend()
    else:
        for i, plot in enumerate(plots):
            plt.plot(*plot, fmt, **kwargs)

    plt.grid()
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.savefig(img_path)
    plt.close()
    return "Plot complete"


def find_crit_lambda(lamd_vector, r_mean, r_critical):
    """
    calculate r and lambda of the critical point on the r(lambda) function.
    :return: r_critical, lambda_critical
    """

    lambd_higher_cr = [lamd_vector[i] for i in range(len(r_mean)) if r_mean[i] >= r_critical]
    if len(lambd_higher_cr) > 0:
        lambd_critical = [lamd_vector[i] for i in range(len(r_mean)) if r_mean[i] >= r_critical][0]
    else:
        lambd_critical = None
    return lambd_critical


def plot_plot(plot, xlable:str, ylable:str, img_path:str, fmt=""):
    plt.plot(*plot, fmt)
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.grid()
    plt.savefig(img_path)
    plt.close()

# ====================


def experiment_critical_lambda(
    osc_boundaries,
    folder_name = "experiment",
    img_name = "crit_lambda_from_osc_n",
    topology = "small_world",
    r_critical = 0.95
):

    lambdas_critical = [find_crit_lambda(*read_system(folder_name, topology, osc_n, dl=1,), r_critical)
                        for osc_n in osc_boundaries]


    img_path = os.path.join(folder_name, "plots", topology, img_name)
    plot_plot((osc_boundaries, lambdas_critical), xlable="oscillator number", ylable="lambda_critical", img_path=img_path, fmt=".-")
    return (osc_boundaries, lambdas_critical)


def experiment_multigraph(folder_name, topology, dl=1, fmt=".", max_l=None):
    """
    Plot multiple r(lambda) series on a figure. Then save in the folder_name/plots/topology
    :return: None
    """
    osc_boundaries = list( range(100, 501, 50) )

    if max_l:
        plots = [cut_the_right_side_of_x(*read_system(folder_name, topology=topology, osc_n=osc_n, dl=dl, ),
                                         start_from_l=max_l
                                         )
                 for osc_n in osc_boundaries]
    else:
        plots = [read_system(folder_name, topology=topology, osc_n=osc_n, dl=dl, ) for osc_n in osc_boundaries]

    img_path = os.path.join(folder_name, "plots", topology, "".join(f"multigraph_{dl}"))
    plot_multigraph(plots, xlable="lambda", ylable="r", img_path=img_path, legend=[f"{osc} osc" for osc in osc_boundaries])


def experiment_critical_multigraph():
    topologies = (
     "random_sw",
     "small_world"
     )
    plots = [experiment_critical_lambda(list(range(100, 501, 50)), topology=topology)
     for topology in topologies]

    img_path = os.path.join("experiment", "plots", "lambda_critical_multigraph")
    plot_multigraph(plots, xlable="osc_number", ylable="lambda_critical", img_path=img_path, fmt=".-", legend=topologies)


def replot_with_legend(data_path,
                                  img_path,
                                  xlabel="",
                                  ylabel="",
                                  fmt="",
                                  legend=None
                                  ):
    plot = file_read(data_path)
    if legend:
        plt.plot(*plot, fmt, label=legend)
    else:
        plt.plot(*plot, fmt)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    plt.savefig(img_path)
    plt.close()


def experiment_replot(
    folder_name = "experiment",
    topology = "small_world",
    ):
    data_path = os.path.join(folder_name, "data", topology, )
    images = os.listdir(data_path)
    img_list = [os.path.join(folder_name, "plots", topology, image) for image in images]
    replot_with_legend()


if __name__ == '__main__':
    # experiment_multigraph("experiment", topology="small_world", dl=1, fmt="-", max_l=30)
    # experiment_critical_lambda( list(range(100, 501, 50)) , topology="small_world")
    # experiment_critical_multigraph()
    experiment_replot()

