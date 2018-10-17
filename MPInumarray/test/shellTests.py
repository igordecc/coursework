import shell
import numpy as np
import matplotlib.pyplot as plt

def test_computeSystemOCL():
    pendulum_phase_output_array, pendulum_time_output_array, time_output_array_length = shell.computeSystemOCL(osc_min=10, osc_max=100, osc_step=1)
    pendulum_phase_output_array = np.transpose(np.array(pendulum_phase_output_array))
    for pendulum in pendulum_phase_output_array:
        plt.plot(np.linspace(0, time_output_array_length, time_output_array_length), pendulum)
    plt.show()

def test_computeRLSystemOCL():
    #print(shell.computeRLSystemOCL())
    RLArray = shell.computeRLSystemOCL()
    ln = len(RLArray)
    plt.plot(np.linspace(0, ln, ln), RLArray)
    plt.show()

test_computeRLSystemOCL()