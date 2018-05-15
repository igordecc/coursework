import matplotlib.pyplot as pp
import numpy as np
#pyploter.py  plot a graphics of lamdas or r parameter
if __name__ == '__main__':
    #filename ='time.txt'      # input('filename:')
    #filename = 'test11.txt'
    filename = 'test_r(lambda).txt'
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

    data_transposed_array = np.transpose(data_array,[1, 0]) 
    #print(data_transposed_array)
    for i in range(oscillators_number):     # пример: пять осцилляторов = пять списков
        pp.plot(data_index_array, data_transposed_array[i])
    pp.grid()
    pp.show()