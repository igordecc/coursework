import matplotlib.pyplot as pp
import numpy as np
if __name__ == '__main__':
    filename ='test_r5.txt'      # input('filename:')
    with open('test_txt//'+filename, "r") as myfile:
        data_index_array = []
        data_array = []

        line = myfile.readline()
        while line != '':
            listed_line = line.split()
            list = [list]

            data_index_array.append(float(listed_line[0]))

            data_array.append([float(listed_line[i+1]) for i in (range(len(listed_line)-1))]) #append a list with all elements, except first element

            line = myfile.readline()

    oscillators_number = len(data_array[0])
    index_length = len(data_index_array)

    data_array = np.array(data_array)
    data_reshaped_array = np.reshape(data_array,[oscillators_number, index_length])
    print(data_array)

    for i in range(oscillators_number):
        pp.plot(data_index_array, data_reshaped_array[i])
    pp.show()