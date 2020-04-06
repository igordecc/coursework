import pyopencl as cl
import numpy as np
from time import perf_counter

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

def compute_time_series_for_system_ocl(omega_vector, lambda_c, A, phase_vector, kernel_src=kernel_src_main, a=0, b=200, oscillators_number=16 * 10000000, N_parts=2000):
    h = abs(a - b) / N_parts

    platformsNum = 0    #определяем объект устройства (девайса)
    deviceNum = 0
    # print("platforms --")
    # print(cl.get_platforms())
    # print(cl.get_platforms()[platformsNum])
    # print(cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum])
    # print("devices ------")
    # print(cl.device_type)
    # print(cl.device_type.GPU)
    # print(cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU))

    device = cl.get_platforms()[platformsNum].get_devices(cl.device_type.GPU)[deviceNum]


    context = cl.Context(devices=[device]) #, dev_type=None     #создаём контекст и очередь
    queue = cl.CommandQueue(context) #,properties=cl.command_queue_properties.PROFILING_ENABLE)

    program = cl.Program(context, kernel_src).build('-cl-std=CL2.0')  #создаём программу

    kernel = cl.Kernel(program, name='kuramoto_equation')  #создаём кернель


    phase_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number)
    omega_vector_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number)
    cl.enqueue_copy(queue, omega_vector_buffer, omega_vector)

    A_buffer = cl.Buffer(context, cl.mem_flags.READ_ONLY, 4*oscillators_number**2)
    cl.enqueue_copy(queue, A_buffer, A)

    out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=4*oscillators_number) #size - size of buffer
    temp_out_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, size=4*oscillators_number) #size - size of buffer


    time_queue = perf_counter()
    cl.enqueue_copy(queue, phase_vector_buffer, phase_vector[0])
    for i in range(N_parts):
        event = kernel(queue, [oscillators_number,], None,
                       np.float32(h),
                       np.float32(lambda_c),
                       omega_vector_buffer,
                       A_buffer,
                       phase_vector_buffer,
                       out_buffer,
                       temp_out_buffer
                       )

        cl.enqueue_copy(queue, phase_vector_buffer, temp_out_buffer)
        cl.enqueue_copy(queue, phase_vector[i], out_buffer)


    time_queue = perf_counter() - time_queue
    print("  GPU {0:.6f} sec".format(time_queue))
    return phase_vector, time_queue

