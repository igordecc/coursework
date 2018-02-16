import math

def get_r(time_output_array, pendulum_phase_output_array, oscillators_number):
    for i in range(time_output_array):
        sum_cos = 0
        sum_sin = 0
        for j in pendulum_phase_output_array[i]:
            sum_cos += math.cos(j)
            sum_sin += math.sin(j)
        x = sum_cos/oscillators_number
        y = sum_sin/oscillators_number
        r = 0
        try:
            r = (x**2 + y**2)**0.5
        except:
            print("CALCULATE R EXCEPTION")
    return r