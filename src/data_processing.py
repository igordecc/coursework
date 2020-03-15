import matplotlib.pyplot as plt
import numpy as np


FOLDER = ""
SAVE_FOLDER = ""


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# def read_file_and_print(filename):
#     with open(filename, "r") as myfile:
#         lines = myfile.readlines()
#         for row in lines:
#             x = [float(item) for item in row.split()]
#             print(x)
#
#
# def read_file(filename):
#     """
#     read filename and return x,y series ready for plot
#     :param filename:
#     :return:
#     """
#     with open(filename, "r") as myfile:
#         lines = myfile.readlines()
#         rows = np.array([[float(item) for item in row.split()] for row in lines])
#         columns = rows.transpose()
#         return columns


def read_wordy_file(filename):
    """
    read filename and return x,y series ready for plot
    :param filename:
    :return:
    """

    with open(filename, "r") as myfile:
        lines = myfile.readlines()

        rows = np.array([[item for item in row.split()] for row in lines[1:]])
        columns = rows.transpose()
        new_columns = [[float(i) for i in column] if isfloat(column[0]) else column for column in columns]
    return new_columns


def plot_data(data, fmt="."):
    plt.plot(*data, fmt)
    plt.grid()
    plt.show()


def save_data_img(data, filename, fmt="."):
    plt.grid()
    plt.ylabel("r")
    plt.xlabel(filename)
    x = data[0]
    for y in data[1:]:
        plt.plot(x, y, fmt)
    plt.savefig("./img"+SAVE_FOLDER+"/" + filename + ".png")
    plt.close()


def _path(filename:str):
    return "./log"+FOLDER+"/r_from_" + filename + ".txt"

def read_plot_save(filename):
    data = read_wordy_file(_path(filename))
    save_data_img(data, filename)
    # plot_data(data)

if __name__ == '__main__':
    FILENAMES = [
        "oscillators_number",
        "lambd",
        "reconnectionProbability", # -sf -regular
        "lambd_for_oscillators_number"   # multigraph
        #"topology"
    ]
    FOLDER = "/regular"
    SAVE_FOLDER = FOLDER
    for filename in FILENAMES:
        read_plot_save(filename)

    FOLDER = "/sf"
    SAVE_FOLDER = FOLDER
    for filename in FILENAMES:
        read_plot_save(filename)

    FOLDER = "/sw"
    SAVE_FOLDER = FOLDER
    for filename in FILENAMES:
        read_plot_save(filename)

    FOLDER = "/random"
    SAVE_FOLDER = FOLDER
    for filename in FILENAMES:
        read_plot_save(filename)