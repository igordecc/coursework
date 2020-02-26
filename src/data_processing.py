import matplotlib.pyplot as plt


FILENAMES = [
    "./log/r_from_oscillator_number.txt"
]


def read_file(filename):
    with open(filename, "r") as myfile:
        lines = myfile.readlines()
        for row in lines:
            x = [float(item) for item in row.split()]
            print(x)

if __name__ == '__main__':
    read_file(FILENAMES[0])