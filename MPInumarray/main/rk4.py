from mpi4py import MPI
"""
python's module, wich handle Message Passing Interface (MPI)
for parallel rungecute method calculus
"""

comm = MPI.COMM_WORLD
size = comm.Get_size()  # количество узлов
rank = comm.Get_rank()  # номер узла

import numpy as np


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
    y = initial_conditions # [1,2,3,4] # начальные условия для каждого уравнения, одно уравнение - один маятник
    ###oscillators_number = len(initial_conditions)  # количество уравнений// осцилляторов (было eqcount)
    divv = oscillators_number // size
    modd = oscillators_number % size

    part_length_first = [divv + 1 for i in range(modd)]
    part_length_second = [divv for i in range(size - modd)]
    part_length = part_length_first + part_length_second
    # смещение (первого элемента в отрезке) относительно начала
    part_diplacement_first = [(divv + 1) * i for i in range(modd)]
    part_diplacement_second = [divv * i + modd for i in np.arange(modd, size)]
    part_diplacement = part_diplacement_first + part_diplacement_second

    def compute_in_parallel(comm, vfunc, h, oscillators_number, t, y):
        """
        this function is paralleling runge method;
        NOW IT'S WORKING LONG -- DO SOMETHING;
        :param comm: comm = MPI.COMM_WORLD
        :param vfunc: 1d vector of general equasions
        :param h: length of the segment of our timeline
        :param oscillators_number: constant; literal sense
        :param t: current time
        :param y: 1d vector of oscillators phases

        :return: k - one of four part of y - 4 phase vectors for calculus
        """
        #=========== paralleled part ==============#####################ERROR IS HERE
        #==============================###size == amount of parts
        if rank < modd:
            data = np.empty(divv + 1)
            for i in range(part_length[rank]):
                data[i] = (h* vfunc[ part_diplacement[rank]+i ](None ,None ,y))
        else:
            data = np.empty(divv)
            for i in range(part_length[rank]):
                data[i] = (h* vfunc[ part_diplacement[rank]+i ](None, None, y))

        #================================
        k = np.empty(oscillators_number)
        #TODO Extract "if rank==0" gap out of kfunk and rewrite "if rank<modd" part


        comm.Gatherv(data, None if rank!=0 else [k, part_length, part_diplacement, MPI.DOUBLE])  # TIS NUMPY ARRAY NOW  k = [[#data1], [#data1], [#data], ...]#####################ERROR IS HERE
        #[1,4,0,3,2]
        #[0,1,2,3,4]
        # [1-[1,2,3,4],2-[1,2,3,4], 3-[1,2,3,4],..]
        comm.Bcast(k, root=0)  # рассылаем обратно на все узлы конечный ответ
        return k   # TIS NUMPY ARRAY NOW

    for i in range(N):
        yield t, y
        y = compute_in_parallel(comm, vfunc, h, oscillators_number, t, y)
        '''
        k1 = compute_in_parallel(comm, vfunc, h, oscillators_number, t, y)

        yik2 = [y[j] + k1[j]/2 for j in range(oscillators_number)]
        k2 = compute_in_parallel(comm, vfunc, h, oscillators_number, t + h / 2, yik2)
        #элементы y:1        2         3
        #[[1,1,2,3],[2,1,2,3],[3,1,2,3]] - это yik2
        #k2 = [h*f(t + h/2, *yik2) for f in vfunc]

        yik3 = [y[j] + k2[j]/2 for j in range(oscillators_number)]
        k3 = compute_in_parallel(comm, vfunc, h, oscillators_number, t + h / 2, yik3)  #k3 = [h*f(t + h/2, *yik3) for f in vfunc]

        yik4 = [y[j] + k3[j] for j in range(oscillators_number)]
        k4 = compute_in_parallel(comm, vfunc, h, oscillators_number, t + h, yik4)  #k4 = [h*f(t + h, *yik4) for f in vfunc]

        for j in range(oscillators_number):
            y[j] += (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6
'''
        t += h
    return t, y

#TODO runge() work right with Euler method, use it for tests.

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

