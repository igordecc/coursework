import matplotlib.pyplot as plt
import numpy as np



def read_file_and_print(filename):
    with open(filename, "r") as myfile:
        lines = myfile.readlines()
        for row in lines:
            x = [float(item) for item in row.split()]
            print(x)


def read_file(filename):
    """
    read filename and return x,y series ready for plot
    :param filename:
    :return:
    """
    with open(filename, "r") as myfile:
        lines = myfile.readlines()
        rows = np.array([[float(item) for item in row.split()] for row in lines])
        columns = rows.transpose()
        return columns


def read_wordy_file(filename):
    """
    read filename and return x,y series ready for plot
    :param filename:
    :return:
    """

    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    with open(filename, "r") as myfile:
        lines = myfile.readlines()
        rows = np.array([[item for item in row.split()] for row in lines])
        columns = rows.transpose()
        new_columns = [[float(i) for i in column] if isfloat(column[0]) else column for column in columns]
        return new_columns


def plot_data(data, fmt="."):
    plt.plot(*data, fmt)
    plt.grid()
    plt.show()


def save_data_img(data, filename, fmt="."):
    plt.grid()
    plt.plot(*data, fmt)
    plt.savefig("./img/" + filename + ".png")


def _path(filename:str):
    return "./log/r_from_" + filename + ".txt"

if __name__ == '__main__':
    FILEPATHS = [
    "./log/r_from_oscillator_number.txt",
    "./log/r_from_lambd.txt",
    "./log/r_from_reconnection_probability.txt",
    "./log/r_from_topology.txt",
]
    FILENAMES = [
        "oscillator_number",
        "lambd",
        "reconnection_probability",
        "topology"
    ]
    filename = FILENAMES[2]
    data = read_wordy_file(_path(filename))
    save_data_img(data, filename)
    # plot_data(data)
