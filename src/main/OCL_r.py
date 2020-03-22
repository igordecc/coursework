import pyopencl as cl
import numpy as np
from time import perf_counter

kernel_src_main = """
kernel void  kuramoto_equation(
    const float h,
    const int N,
    const global float* lambda,
    const global float* omega_vector,
    const global float* A, 
    const global float* phase_vector, 
    global float* vector_s,
    global float* vector_transformed
    )
{
    const int system_id = get_global_id(0);
    const int id = get_global_id(1);
    
    A += id*N;
    float summ = 0;

    for (int j = 0; j < N; ++j)
    {
        summ += A[j] * sin( phase_vector[system_id*N + j] - phase_vector[system_id*N + j] ); 
    }
    summ = lambda[system_id]*summ/N + omega_vector[system_id*N + id];

    summ = phase_vector[system_id*N + id] + summ * h;
    vector_transformed[system_id*N + id] = summ;
    vector_s[system_id*N + id] = sin( fmod(summ,  2*M_PI_F) );
        
}"""


def compute_last_time_series_for_multiple_systems_with_ocl(omega_vector, lambda_c, A, phase_vector_2d, kernel_src=kernel_src_main, a=0, b=200, n_systems=None, n_oscillators=16 * 10000000, N_parts=2000):
    h = abs(a - b) / N_parts

    platformsNum = 0  # определяем объект устройства (девайса)
    deviceNum = 0

    if n_systems==None:
        n_systems = len(phase_vector_2d[0])
    # print("platforms --")
    # print(cl.get_platforms())
    # print(cl.get_platforms()[platformsNum])
    # print(cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum])
    # print("devices ------")
    # print(cl.device_type)
    # print(cl.device_type.GPU)
    # print(cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU))

    device = cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum]

    context = cl.Context(devices=[device])  # , dev_type=None     #создаём контекст и очередь
    queue = cl.CommandQueue(context)  # ,properties=cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(context, kernel_src).build('-cl-std=CL2.0')  # создаём программу

    kernel = cl.Kernel(program, name='kuramoto_equation')  # создаём кернель

    phase_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase_vector_2d[0])

    omega_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=omega_vector)

    lambda_c_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=lambda_c)

    A_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=A)


    out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase_vector_2d[0])  # size - size of buffer

    temp_out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase_vector_2d[0])  # size - size of buffer

    # new_phase_vector = np.shape(phase_vector_2d.shape)
    time_queue = perf_counter()
    for i in range(N_parts):
        event = kernel(queue, [n_systems, n_oscillators, ], None,  # oscillators number 1d -> 2d [system number; oscillators number] # global size 0 global size 1
                       np.float32(h),
                       np.int32(n_oscillators),
                       lambda_c_buffer,
                       omega_vector_buffer,
                       A_buffer,
                       phase_vector_buffer,
                       out_buffer,
                       temp_out_buffer
                       )

        cl.enqueue_copy(queue, phase_vector_buffer, temp_out_buffer)
    cl.enqueue_copy(queue, phase_vector_2d[-1], out_buffer)

    time_queue = perf_counter() - time_queue
    # print(time_queue)
    return phase_vector_2d, time_queue


if __name__ == '__main__':
    from config_creator import create_config
    oscillators_number = 100
    lambda_bounds = np.arange(0.1, 100, 0.1)    # 8 GB
    systems_amount = lambda_bounds.__len__()
    multi_config_list = [ create_config(oscillators_number=oscillators_number, filename=None) for _lambda in lambda_bounds]
    N_iterations_amount = multi_config_list[0]['N']
    phase_vector_2d = np.array([[config['phase_vector'] for config in multi_config_list], ])
    omega_vector_2d = np.array([config['omega_vector'] for config in multi_config_list])
    Aij = np.array([config['Aij'] for config in multi_config_list])

    x = compute_last_time_series_for_multiple_systems_with_ocl(omega_vector_2d,
                                                               lambda_bounds,
                                                               Aij,
                                                               phase_vector_2d,
                                                               kernel_src=kernel_src_main,
                                                               a=0,
                                                               b=200,
                                                               n_systems=systems_amount,
                                                               n_oscillators=oscillators_number,
                                                               N_parts=N_iterations_amount)
    print(x)