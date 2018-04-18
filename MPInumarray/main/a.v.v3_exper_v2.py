"""
Experiment function is made from adding_vectors_v3.py
"""

import pyopencl as cl
import numpy as np
from time import perf_counter

#A[self.pendulum_index][j] * sin( phase_vector[j] - my_phase )


kernel_src_main = """
    kernel void  kuramoto_equation(
        global const float* omega_vector
        const float lambda,
        global const float* A, 
        global float* phase_vector, 
        global float* vector_s
        )
    {
        const int global_i = get_global_id(0);
        const int N = get_global_size(0);
        float summ = 0;
        
        for (int j = 0; j < N; ++j)
        {
            summ += A[global_i*N+j] * sin( phase_vector[j] - phase_vector[global_i] ); 
        }
        summ = lambda*summ + omega_vector[i];
        vector_s[global_i] = summ;
        
    }"""
def ad(omega_vector, lambda_c, A, phase_vector, kernel_src=kernel_src_main, a=0, b=10, N=16*10000000,N_parts=16*10000000):
    """
    функция, вычисляющая по интеграл заданной функции на GPU с использованием локальных групп
    вычисляем вектор разбиения отрезка [a,b] и вектор для вывода результата

    - содержит общее уравнение осциллятора (осциллятора Курамото)
    > задаём начальные условия на входе
    > возращаем значения фазы на выходе
    > ...
    > profit


    :param kernel_src: source string of C programm
    :param a: from a
    :param b: to b
    :param N: = N*16 #количество отрезочков, на которые разобьём [a,b]
    :return:
    """
    # TODO разбить на 2 части
    # TODO - наружняя часть принимает все начальные значения и возращает вектор векторов6565 фаз N осцилляторов (эволюция фаз N осцилляторов во времени) и вектор времени;
    # TODO - внутренняя часть принимает все начальные значения и момент времени, и возвращает вектор фаз N осцилляторов в этот момент времени
    N = N*16 # теперь это число осцилляторов
    h = abs(a - b) / N_parts

    platformsNum = 0    #определяем объект устройства (девайса)
    deviceNum = 0
    device = cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum]

    context = cl.Context(devices=[device]) #, dev_type=None     #создаём контекст и очередь
    queue = cl.CommandQueue(context) #,properties=cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(context, kernel_src).build('-cl-std=CL2.0 -D GROUP_SIZE=256')  #создаём программу

    kernel = cl.Kernel(program, name='kuramoto_equation')  #создаём кернель

    kernel.set_scalar_arg_dtypes((np.float32, np.float32, None))    #запускаем кернель

    global_work_size = N
    local_work_size = 256

    size_of_buff = 4* global_work_size//local_work_size          #size of float = 4 (byte)
    out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size_of_buff)

    time_queue = perf_counter()
    # TODO ============== обернуть в цикл здесь! подумать о и передаче phase_vector строки на каждом шаге цикла
    event = kernel(queue, [global_work_size], [local_work_size], omega_vector, lambda_c, A, phase_vector, out_buffer) #vector_s = out_buffer

    #time_kernel = event.get_profiling_info(cl.profiling_info.END)-event.get_profiling_info(cl.profiling_info.START)

    vectors = np.zeros(global_work_size//local_work_size, dtype=np.float32) #считываем результат (2-й баффер)  в вектор площадей s
    cl.enqueue_copy(queue, vectors, out_buffer)
    result = vectors
    time_queue = perf_counter() - time_queue
    #assert all(vector1 + vector2 == vectors)   #просто так, проверяем верно ли выполнена операция

    return result, time_queue


if __name__ == '__main__':
    ...
    result, time_queue = ad()
    print(result, time_queue, sep='\n')
