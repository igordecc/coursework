import matplotlib.pyplot as pp
import numpy as np
from scipy import polyval, polyfit
#pyploter.py  plot a graphics of lamdas or r parameter
if __name__ == '__main__':
    #filename ='MPI_time_outdated.txt'      # input('filename:')
    filename ='time1.txt'      # input('filename:')
    #filename = 'test11.txt'
    #filename = 'test_r(lambda).txt'
    with open('result_txt//'+filename, "r") as myfile:
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
        #pp.plot(data_index_array, data_transposed_array[i])
        pp.scatter(data_index_array, data_transposed_array[i], s=3)#, linestyle=":", )
        #====approximation======
        a, b, c, d, q, p = polyfit(data_index_array, data_transposed_array[i], 5)
        y_pred = polyval([a, b, c, d, q, p], data_index_array)
        print(y_pred)
        pp.plot(data_index_array, y_pred, color="orange")

        #=======================
    pp.grid()
    pp.axes().set_yscale("log", nonposy='clip')
    pp.xlabel("количество осцилляторов  osc")
    pp.ylabel("время выполнения программы T, log(с)")
    pp.show()