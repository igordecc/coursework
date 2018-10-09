"""
Experiment function is made from adding_vectors_v3.py
"""

import pyopencl as cl
import numpy as np
from time import perf_counter

#A[self.pendulum_index][j] * sin( phase_vector[j] - my_phase )


kernel_src_main = """
kernel void  kuramoto_equation(
    const float h,
    const float lambda,
    const global float* omega_vector,
    const global float* A, 
    const global float* phase_vector, 
    global float* vector_s,
    global float* vector_transformed
    )
{
    const int id = get_global_id(0);
    const int N = get_global_size(0);
    A += id*N;
    float summ = 0;
    
    for (int j = 0; j < N; ++j)
    {
        summ += A[j] * sin( phase_vector[j] - phase_vector[id] ); 
    }
    summ = lambda*summ/N + omega_vector[id];
    
    summ = phase_vector[id] + summ * h;
    vector_transformed[id] = summ;
    vector_s[id] = sin( fmod(summ,  2*M_PI_F) );
    
}"""

def ad(omega_vector, lambda_c, A, phase_vector, kernel_src=kernel_src_main, a=0, b=200, oscillators_number=16 * 10000000, N_parts=2000):
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
    :param oscillators_number: = N*16 #количество отрезочков, на которые разобьём [a,b]
    :return:
    """
    # TODO разбить на 2 части
    # TODO - наружняя часть принимает все начальные значения и возращает вектор векторов6565 фаз N осцилляторов (эволюция фаз N осцилляторов во времени) и вектор времени;
    # TODO - внутренняя часть принимает все начальные значения и момент времени, и возвращает вектор фаз N осцилляторов в этот момент времени
    #oscillators_number = oscillators_number * 16 # теперь это число осцилляторов
    h = abs(a - b) / N_parts

    platformsNum = 0    #определяем объект устройства (девайса)
    deviceNum = 0
    device = cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum]

    context = cl.Context(devices=[device]) #, dev_type=None     #создаём контекст и очередь
    queue = cl.CommandQueue(context) #,properties=cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(context, kernel_src).build('-cl-std=CL2.0')  #создаём программу

    kernel = cl.Kernel(program, name='kuramoto_equation')  #создаём кернель

    #kernel.set_scalar_arg_dtypes((np.float32, np.float32, np.float32, np.float32, np.float32))    #запускаем кернель

    phase_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number)
    omega_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number)
    cl.enqueue_copy(queue, omega_vector_buffer, omega_vector)

    A_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number**2)
    cl.enqueue_copy(queue, A_buffer, A)

    out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=4*oscillators_number) #size - size of buffer
    temp_out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=4*oscillators_number) #size - size of buffer


    time_queue = perf_counter()
    cl.enqueue_copy(queue, phase_vector_buffer, phase_vector[0])
    # here starts actual calculating
    for i in range(N_parts):
        event = kernel(queue, [oscillators_number,], None,
                       np.float32(h),
                       np.float32(lambda_c),
                       omega_vector_buffer,
                       A_buffer,
                       phase_vector_buffer,
                       out_buffer,
                       temp_out_buffer
                       ) #vector_s = out_buffer

        #time_kernel = event.get_profiling_info(cl.profiling_info.END)-event.get_profiling_info(cl.profiling_info.START)

        cl.enqueue_copy(queue, phase_vector_buffer, temp_out_buffer)
        cl.enqueue_copy(queue, phase_vector[i], out_buffer)


    time_queue = perf_counter() - time_queue
    #assert all(vector1 + vector2 == vectors)   #просто так, проверяем верно ли выполнена операция

    return phase_vector, time_queue


#TODO: move to tests

#from config_creator import create_config
# if __name__ == '__main__':
#     oscillators_number=16 * 100
#     config = create_config(oscillators_number=oscillators_number, filename=None)
#
#
#     phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
#     phase_vector[0] = config['phase_vector']
#
#     omega_vector = np.array(config['omega_vector'], dtype=np.float32)
#     Aij = np.array(config['Aij'], dtype=np.float32)
#
#     phase_vector, time_queue = ad(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
#     #result, time_queue = ad()
#     #print(result, time_queue, sep='\n')
