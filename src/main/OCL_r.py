import numpy
import pyopencl as cl
from time import perf_counter

KERNEL_SRC = """
kernel void kuramoto_equation(
    const float step,
    const global float* lambda,
    const global float* omega,
    const global float* A, 
    const global float* phase,
    global float* vector_transformed
) {
    const int system_id = get_global_id(0);
    const int oscillator_id = get_global_id(1); 
    const int N = get_global_size(1);

    phase += system_id*N;
    A += oscillator_id*N;

    float summ = 0;

    for (int j = 0; j < N; ++j) {
        summ += A[j] * sin(phase[j] - phase[oscillator_id]); 
    }

    summ = lambda[system_id]*summ / N + omega[oscillator_id];
    summ = phase[oscillator_id] + summ * step;

    vector_transformed[system_id*N + oscillator_id] = summ;
}

kernel void transform_result(
    const int n_osc, 
    const global float* result,
    global float* final_result
) {
    const int id = get_global_id(0);

    result += id*n_osc;

    float sum_cos = 0;
    float sum_sin = 0;

    for (int i = 0; i < n_osc; ++i) {
        const float norm = sin(fmod(result[i], 2*M_PI_F));
        sum_cos += cos(norm);
        sum_sin += sin(norm);
    }

    const float x = sum_cos / n_osc;
    const float y = sum_sin / n_osc;

    final_result[id] = sqrt(x*x + y*y);
}

"""


def as_cl_buffer(ctx, arr, flags=cl.mem_flags.READ_ONLY):
    if isinstance(arr, cl.Buffer):
        return arr
    elif isinstance(arr, numpy.ndarray):
        return cl.Buffer(ctx, flags | cl.mem_flags.COPY_HOST_PTR, hostbuf=arr)
    else:
        raise TypeError(f"{type(arr)} cannot be converted to cl.Buffer")


class KuramotoSystem:

    def __init__(self, platform_id=0, device_id=0):
        start = perf_counter()
        device = cl.get_platforms()[platform_id].get_devices(cl.device_type.GPU)[device_id]

        self.context = cl.Context(devices=[device])
        self.queue = cl.CommandQueue(self.context)
        self.program = cl.Program(self.context, KERNEL_SRC).build(options=['-cl-std=CL2.0'])
        self._solve = cl.Kernel(self.program, name='kuramoto_equation')
        self._transform_result = cl.Kernel(self.program, name='transform_result')
        # print(f" kernel init {perf_counter() - start}")

    def _solve_multiple(self, step: float, iterations: int, n_systems: int, n_oscillators: int,
                        omega: cl.Buffer, phase: cl.Buffer, adjacency: cl.Buffer, lambdas: cl.Buffer):
        timings = {}

        phase_size = phase.get_info(cl.mem_info.SIZE)
        phase2_buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE, size=phase_size)

        start = perf_counter()
        for _ in range(iterations):
            self._solve(
                self.queue, (n_systems, n_oscillators), None,
                numpy.float32(step),
                lambdas,
                omega,
                adjacency,
                phase,
                phase2_buf
            )

            phase, phase2_buf = phase2_buf, phase
        self.queue.finish()
        timings["_solving for"] = perf_counter() - start
        print(f" _solving for _ {perf_counter() - start}")
        phase_out = numpy.empty((n_systems,), dtype=numpy.float32)
        # phase_out_buf = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY, size=phase_out.nbytes)
        phase_out_buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase_out)
        # phase_buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase)
        start = perf_counter()
        self._transform_result(
            self.queue, (n_systems,), None,
            numpy.int32(n_oscillators),
            phase,
            phase_out_buf
        )
        self.queue.finish()
        timings["_transform_result"] = perf_counter() - start
        print(f" _transform_result {perf_counter() - start}")
        start = perf_counter()
        cl.enqueue_copy(self.queue, phase_out, phase_out_buf)
        timings["copy"] = perf_counter() - start
        print(f" COPY {perf_counter() - start}")


        return phase_out, timings

    def solve_multiple(self, step: float, iterations: int, phase: numpy.ndarray, omega, adjacency, lambdas):
        n_systems, n_oscillators = len(lambdas), len(phase)

        phase = numpy.tile(phase, n_systems)
        phase_buf = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=phase)

        omega_buf = as_cl_buffer(self.context, omega)
        lambdas_buf = as_cl_buffer(self.context, lambdas)
        adjacency_buf = as_cl_buffer(self.context, adjacency)

        _result, timings = self._solve_multiple(
            step, iterations, n_systems, n_oscillators,
            omega_buf, phase_buf, adjacency_buf, lambdas_buf
        )

        return _result, timings


if __name__ == '__main__':
    KuramotoSystem()
