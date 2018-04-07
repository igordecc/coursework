"""
Experiment function is made from adding_vectors_v3.py
"""

import pyopencl as cl
import numpy as np
from time import perf_counter

kernel_src_main = """

    float f(float x)
    {
        return sin(x);
    }

    kernel void metod_trapeziy(const float a, const float h, global float* vector_s)
    {
        local float local_sum[GROUP_SIZE];
        const int local_i = get_local_id(0);
        const int global_i = get_global_id(0);

        const float x = a + h * global_i;
        local_sum[local_i] = (f(x) + f(x+h))*h/2;

        barrier(CLK_LOCAL_MEM_FENCE);

        __attribute__((opencl_unroll_hint(8)))
        for (int i = 1; i <= GROUP_SIZE/2; i <<= 1 )
        { 
            if (local_i % (i << 1) == 0)
            {
                local_sum[local_i] += local_sum[local_i+i];
                barrier(CLK_LOCAL_MEM_FENCE);
            }
            else
            {
                break;
            }
        }

        if (local_i == 0)
        {
            vector_s[global_i/GROUP_SIZE] = local_sum[0];
        }
    }"""
def ad(kernel_src=kernel_src_main, a=0, b=3.14, N=16*10000000):
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
    N = N*16
    h = abs(a - b) / N

    platformsNum = 0    #определяем объект устройства (девайса)
    deviceNum = 0
    device = cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum]

    context = cl.Context(devices=[device]) #, dev_type=None     #создаём контекст и очередь
    queue = cl.CommandQueue(context) #,properties=cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(context, kernel_src).build('-cl-std=CL2.0 -D GROUP_SIZE=256')  #создаём программу

    kernel = cl.Kernel(program, name='metod_trapeziy')  #создаём кернель

    kernel.set_scalar_arg_dtypes((np.float32, np.float32, None))    #запускаем кернель

    global_work_size = N
    local_work_size = 256

    size_of_buff = 4* global_work_size//local_work_size          #size of float = 4 (byte)
    out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size_of_buff)

    time_queue = perf_counter()

    event = kernel(queue, [global_work_size], [local_work_size], a, h, out_buffer)
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
