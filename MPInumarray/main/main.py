# sudo mount -t vboxsf PycharmProjects ~/PycharmProjects (sudo mount -t vboxsf course_work ~/t)
# cd ./t/MPInumarray/main
# mpurun -n 4 python3 ./shell\ and\ run\ timers.py

# python3 ./t/MPInumarray/main/main.py (путь к файлу)
# mpirun -n 3 python3 ./t/MPInumarray/main/main.py (запуск на n узлах - почитать документацию по mpirun - именно по ней)
# shotdown -P 0
# (mpirun) https://www.open-mpi.org/doc/current/man1/mpirun.1.php
# (mpi docs) https://www.open-mpi.org/doc/v2.0/
# (kursovaya Kosti) https://github.com/yaphtes/course_work
# (login, password, sudo password) = user, password, password
# (mpi tutor) https://pythonhosted.org/mpi4py/usrman/tutorial.html
# (python doc mpi) http://mpi4py.readthedocs.io/en/2.0.0/
"""
how to instal openmpi
download openmpi.tar.gr/// wget https://www.open-mpi.org/software/ompi/v3.0/downloads/openmpi-3.0.0.tar.gz
unpack/// tar -xzf openmpi-3.0.0.tar.gz
go to folder openmpi-3.0.0///cd openmpi-3.0.0
now we run configure/// configure
now we run make /// make
now we run sudo make install// sudo make install
"""
"""
if mpirun cannot work with error:
mpi cannot find libopen-rte.so.40
then run /// sudo ldconfig
"""

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
    from mpi4py import MPI
    import numpy as np

    comm = MPI.COMM_WORLD
    size = comm.Get_size()  # количество узлов
    rank = comm.Get_rank()  # номер узла

    def kfunc(comm, size, rank, vfunc, h, oscillators_number, t, y):
        divv = oscillators_number//size
        modd = oscillators_number%size
        if rank < modd:
            data = np.empty(divv+1)
        else:
            data = np.empty(divv)

        if rank < modd:
            for i in range(len(data)):
                data[i] = (h* vfunc[ (divv+1)*rank + i ](t, rank,y[i]))
        else:
            for i in range(len(data)):
                data[i] = (h* vfunc[ (divv)*rank + modd + i ](t, rank,y[i]))
        k = np.empty(oscillators_number)
        if rank==0:
            part_length_first = [divv+1 for i in range(modd)]
            part_length_second = [divv for i in range(size-modd)]
            part_length = part_length_first + part_length_second
            # смещение (первого элемента в отрезке) относительно начала
            part_diplacement_first = [(divv+1)*i for i in range(modd)]
            part_diplacement_second = [divv*i+modd for i in np.arange(modd, size)]
            part_diplacement = part_diplacement_first + part_diplacement_second
        comm.Gatherv(data, None if rank!=0 else [k, part_length, part_diplacement, MPI.DOUBLE])
        #[1,4,0,3,2]
        #[0,1,2,3,4]
        comm.Bcast(k, root=0)
        return k


    class Pendulum:
        def __init__(self, indicator):  # lambd -- A[i]
            self.indicator = indicator

        def __call__(self, t, point, phase_vector):
            return phase_vector * self.indicator


    oscillators_number = 11
    test_phase_vector = [1 for i in range(oscillators_number)]
    vfunc = [Pendulum(i) for i in range(oscillators_number)]
    """
    vfunc = []
    for i in range(oscillators_number):
        vfunc.append(lambda z,y,x:x*i)
    """


    k = kfunc(comm, size, rank, vfunc, 0.1, oscillators_number, 1, test_phase_vector)
    print(k)

#TODO still run, but didn't work right on full version,(run and work on test version) - make it work right