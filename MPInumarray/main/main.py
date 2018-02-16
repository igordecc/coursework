# sudo mount -t vboxsf PycharmProjects ~/PycharmProjects
# sudo mount -t vboxsf course_work t ///маунт папки
# python3 ./PycharmProjects/MPIyoung/main/main.py (путь к файлу)
# mpirun -n 3 python3 ./PycharmProjects/MPIyoung/main/main.py (запуск на n узлах - почитать документацию по mpirun - именно по ней)
# shotdown -P 0
# (mpirun) https://www.open-mpi.org/doc/current/man1/mpirun.1.php
# (mpi docs) https://www.open-mpi.org/doc/v2.0/
# (kursovaya Kosti) https://github.com/yaphtes/course_work
# (login, password, sudo password) = user, password, password
# (mpi tutor) https://pythonhosted.org/mpi4py/usrman/tutorial.html
# (python doc mpi) http://mpi4py.readthedocs.io/en/2.0.0/
"""
from mpi4py import MPI
print("zapuweno na uzle %d" % (MPI.COMM_WORLD.Get_rank(),))
print("Luchshe testit dlya dvux uzlov")
"""
#--
#-- сделать вывод в файл для уже готовой программы
#-- реализовать распаралеливание по циклам for метода Рунге-Кутта
#-- реализовать подсчёт времени вычислений для непаралеленых и паралельных вычислений

import math
import time
from rk4 import runge          #* - import all functions
import random

class Timer:
    def __init__(self):
        self.t = 0

    def start(self):
        self.t = time.perf_counter()
        return self

    def stop(self):
        self.t = time.perf_counter()-self.t
        return self.t


if __name__ == '__main__':
    """
    d = 15      #number of equations
    omega = []
    for i in range(d):
        omega += [random.uniform(-1,1)]   #[(i+1)**(-1.5)*10]

    K = []
    for i in range(d):
        K += [0.2]#[random.uniform(0,0.5)]   #[(i+1)**2]

    vfunc = []
    for nf in range(d): #nf - function number
        #_omega, _K = omega[nf], K[nf]
        def f(t, *theta):
            _sum = 0
            thetalist = [*theta]
            for j in range(d):
                _sum += math.sin(thetalist[j] - thetalist[nf])
            return omega[nf] + K[nf] / d * _sum
        vfunc.append(f)

    initial_conditions = []               # theta[_i] in zero-time
    for _i in range(d):
        initial_conditions.append(0.4)  # [_i/2]

    import matplotlib.pyplot as mpl
    a = 0
    b = 10
    N = 100
    x = [[] for i in range(d)] #x = [[],[],[], ...]
    t = []
    timer = Timer().start()                        ###

    for i in range(d):
        for e in runge(a,b,initial_conditions[i],N,vfunc[i],i):
            x[i].append(e[1])
            t.append(e[0]) # NOT AN ERROR
    print("Elapsed time: %f s" % (timer.stop(),))  ### % floating point format
    for i in range(d):
        mpl.plot(t,x[i])
    mpl.show()
    """
    d = 15  # number of equations
    omega = []
    for i in range(d):
        omega += [random.uniform(-1, 1)]  # [(i+1)**(-1.5)*10]

    K = []
    for i in range(d):
        K += [0.2]  # [random.uniform(0,0.5)]   #[(i+1)**2]

    vfunc = []
    for nf in range(d):  # nf - function number
        def f(t, nf, *thetalist):
            _sum = 0
            for j in range(d):
                _sum += math.sin(thetalist[j] - thetalist[nf])
            return omega[nf] + K[nf] / d * _sum
        vfunc.append(f)

    initial_conditions = []  # theta[_i] in zero-time
    for _i in range(d):
        initial_conditions.append(0.4)  # [_i/2]

    import matplotlib.pyplot as mpl

    a = 0
    b = 10
    N = 100
    x = [[] for i in range(d)]  # x = [[],[],[], ...]
    t = []
    timer = Timer().start()  ###

    for e in runge(a, b, initial_conditions, N, vfunc):
        for i in range(d):
            x[i].append(e[1][i])
        t.append(e[0])  # NOT THE ERROR
    print("Elapsed time: %f s" % (timer.stop(),))  ### % floating point format
    for i in range(d):
        mpl.plot(t, x[i])
    mpl.show()