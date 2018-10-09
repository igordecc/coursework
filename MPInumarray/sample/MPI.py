import rk4
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

part_length = [3 for i in range(size)]
part_displacement = [i*3 for i in range(size)]
data = []
data = np.array([i for i in range(part_length[rank])], dtype=float)
print('data ', data) ####
k = np.empty(sum(part_length))

if rank ==0:
    print('pl: ', part_length)
    print('pd: ', part_displacement) ####

comm.Gatherv(data, None if rank != 0 else [k, part_length, part_displacement, MPI.DOUBLE])
comm.Bcast(k, root=0)

print (k) ###