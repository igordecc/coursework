from mpi4py import MPI
"""
python's module, wich handle Message Passing Interface (MPI)
for parallel rungecute method calculus
"""

comm = MPI.COMM_WORLD
size = comm.Get_size()  # количество узлов
rank = comm.Get_rank()  # номер узла

import numpy as np


def compute_part(vfunc, h, t, y, part_length, part_displacement):
    data = np.empty(part_length[rank], dtype=float)
    for i in range(part_length[rank]):
        data[i] = (h * vfunc[part_displacement[rank] + i](t, y))
    return data  # TIS NUMPY ARRAY NOW

def compute_partition(oscillators_number, size):
    divv = oscillators_number // size
    modd = oscillators_number % size

    part_length_first = [divv + 1 for i in range(modd)]
    part_length_second = [divv for i in range(size - modd)] ####&&&
    part_length = part_length_first + part_length_second

    # смещение (первого элемента в отрезке) относительно начала
    part_displacement_first = [(divv + 1) * i for i in range(modd)]
    part_displacement_second = [divv * i + modd for i in range(modd, size)]
    part_displacement = part_displacement_first + part_displacement_second

    return part_length, part_displacement

def update(full_data, part_data, part_length, part_displacement):
    comm.Gatherv(part_data, None if rank != 0 else [full_data, part_length, part_displacement, MPI.DOUBLE])  # TIS NUMPY ARRAY NOW  k = [[#data1], [#data1], [#data], ...]#####################ERROR IS HERE
    comm.Bcast(full_data, root=0)

def runge(a, b, initial_conditions, N, vfunc, oscillators_number):
    """
    Solve differential equation system using Runge-Kutt 4th order method
    RETURN ITERATOR
    :param a: initial time
    :param b: final time
    :param initial_conditions: literal sense; vector of constants
    :param N: step count for given interval [a,b]
    :param vfunc: 1d vector of general equations; please, define functions like f(t, ...) ,
    because first variable is used like time counter from a to b
    :return: t - 1d vector, y - 2d vector of constants
    """
    # существует временной отрезок ab
    # N это количество разбиений этого отрезка
    h = (b - a) / N     # h это шаг разбиения
    t = a               # время начинается с момента времени a
    y = np.array(initial_conditions, dtype=float) # [1,2,3,4] # начальные условия для каждого уравнения, одно уравнение - один маятник
    k = np.empty(oscillators_number, dtype=float)
    part_length, part_displacement = compute_partition(oscillators_number, size)

    for i in range(N):
        yield t, y
        #method EULERA
        data = compute_part(vfunc, h, t, y, part_length, part_displacement)
        update(k, data, part_length, part_displacement)

        """
        data1 = compute_part(vfunc, h, t, y, part_length, part_displacement)
        k1 = np.empty(oscillators_number, dtype=float)
        update(k1, data1, part_length, part_displacement)

        yik2 = [y[j] + k1[j]/2 for j in range(oscillators_number)]
        data2 = compute_part(vfunc, h, t+h/2, yik2, part_length, part_displacement)
        k2 = np.empty(oscillators_number, dtype=float)
        update(k2, data2, part_length, part_displacement)
        #элементы y:1        2         3
        #[[1,1,2,3],[2,1,2,3],[3,1,2,3]] - это yik2
        #k2 = [h*f(t + h/2, *yik2) for f in vfunc]

        yik3 = [y[j] + k2[j]/2 for j in range(oscillators_number)]
        data3 = compute_part(vfunc, h, t+h/2, yik3, part_length, part_displacement) #k3 = [h*f(t + h/2, *yik3) for f in vfunc]
        k3 = np.empty(oscillators_number, dtype=float)
        update(k3, data3, part_length, part_displacement)

        yik4 = [y[j] + k3[j] for j in range(oscillators_number)]
        data4 = compute_part(vfunc, h, t+h, yik4, part_length, part_displacement)  #k4 = [h*f(t + h, *yik4) for f in vfunc]
        k4 = np.empty(oscillators_number, dtype=float)
        update(k4, data4, part_length, part_displacement)

        for j in range(oscillators_number):
            y[j] += (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6
        """
        y += k  #method EULERA
        t += h
    return t, y

#TODO write simple example of this programm:.
#1 цикл: расчёт (какие нибудь простые проверяемые данные; принт где угодно), газер, бродкаст; также, юзая функцию compute_partition

if __name__ == '__main__':
    import math
    import matplotlib.pyplot as mpl

    a = 0
    b = 1000
    initial_conditions = [0.4,-0.5]
    N = 10
    #gamma = 0
    omega = 1
    K = 2.7
    vfunc = [
        lambda t, nf,x, x1: 1 + 2.7/2*(math.sin(x1-x) + math.sin(x-x)),
        lambda t, nf,x, x1: 3.5 + 0.2/2*(math.sin(x-x1) + math.sin(x1-x1)),
    ]
    x = []
    y = []
    t = []
    output = open("output.txt", "w")
    for e in runge(a,b,initial_conditions,N,vfunc):
        x.append(e[1][0])
        y.append(e[1][1])
        t.append(e[0])
        if rank == 0:
            print('rank = '+str(rank))
            print('size = ' + str(size))
            output.write(str(e[1][0]) + ' ')
            output.write(str(e[1][1]) + ' ')
            output.write(str(e[0])+'\n')
    output.flush()
    output.close()
    mpl.plot(t,x)
    mpl.plot(t,y)
    mpl.show()

