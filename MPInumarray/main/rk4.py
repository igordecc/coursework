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

    def kfunc(comm, size, rank, vfunc, h, oscillators_number, t, y):
        """
        this function is paralleling runge method;
        NOW IT'S WORKING LONG -- DO SOMETHING;
        :param comm: comm = MPI.COMM_WORLD
        :param size: size = comm.Get_size(); size of the claster
        :param rank: rank = comm.Get_rank(); rank of the node

        :param vfunc: 1d vector of general equasions
        :param h: length of the segment of our timeline
        :param oscillators_number: constant; literal sense
        :param t: current time
        :param y: 1d vector of oscillators phases

        :return: k - one of four part of y - 4 phase vectors for calculus
        """
        #=========== paralleled part ==============#####################ERROR IS HERE
        """
        i = 0
        point = rank
        while point < oscillators_number:
            i += 1
            point += size
        #print(i,' rank:',rank)
        data = np.empty(i) #[,]

        i = 0
        point = rank
        while point < oscillators_number:
            try:
                data[i] = (h * vfunc[point](t, point, y))  # *data - [1,2]
            except:
                quit()
            point += size
            i += 1
        """
        point = rank
        #==============================
        divv = oscillators_number//size
        modd = oscillators_number%size
        if rank < modd:
            data = np.empty(divv+1)
        else:
            data = np.empty(divv)

        if rank < modd:
            for i in range(len(data)):
                data[i] = (h* vfunc[ (divv+1)*rank + i ](t, point,y))
        else:
            for i in range(len(data)):
                data[i] = (h* vfunc[ (divv)*rank + modd + i ](t, point,y))

        #================================
        k = np.empty(oscillators_number)
        #[1,4]
        #[0,3]
        #[2]

        comm.Gatherv(data, k, root=0)  # TIS NUMPY ARRAY NOW  k = [[#data1], [#data1], [#data], ...]#####################ERROR IS HERE
        #[1,4,0,3,2]
        #[0,1,2,3,4]
        #==========================================
        """
        data = []
        point = rank
        while point < oscillators_number:
            print('kfunk while1 core' + str(rank))
            data.append(h * vfunc[point](t, point, *y))  # *y - [1,2,3,4]
            point += size
        k = comm.gather(data, root=0)  # k = [[#data1], [#data1], [#data], ...]
        """
        #==========================================
        """
        k11 = []

        for point in range(size):
            j = 0
            while True:
                try:
                    print('kfunk while2 core', rank, ' ', j, ' ',point)  # !!!!Исправь ПРИНТЫ !! смотреть здесь что не так для случая с одним ядром?
                    print(k[point][j])
                    k11.append(k[point][j])
                    j += 1
                except:
                    break
        """
        k11 = k        # [1-[1,2,3,4],2-[1,2,3,4], 3-[1,2,3,4],..]
        k11 = comm.bcast(k11, root=0)  # рассылаем обратно на все узлы конечный ответ
        return k11   # TIS NUMPY ARRAY NOW

    for i in range(N):
        yield t, y
        k1 = kfunc(comm, size, rank, vfunc, h, oscillators_number, t, y)

        yik2 = []
        for j in range(oscillators_number):#элементы y:1        2         3
            yik2.append(y[j] + k1[j]/2) #[[1,1,2,3],[2,1,2,3],[3,1,2,3]] - это yik2
        k2 = kfunc(comm, size, rank, vfunc, h, oscillators_number, t, yik2)        #k2 = [h*f(t + h/2, *yik2) for f in vfunc]

        yik3 = []
        for j in range(oscillators_number):
            yik3.append(y[j] + k2[j]/2)
        k3 = kfunc(comm, size, rank, vfunc, h, oscillators_number, t, yik3)        #k3 = [h*f(t + h/2, *yik3) for f in vfunc]

        yik4 = []
        for j in range(oscillators_number):
            yik4.append(y[j] + k3[j])
        k4 = kfunc(comm, size, rank, vfunc, h, oscillators_number, t, yik4)        #k4 = [h*f(t + h, *yik4) for f in vfunc]

        for j in range(oscillators_number):
            y[j] += (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6
        t += h
    return t, y

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
