import math
import rk4
"""
Concept:
There is Kuramoto System, wich include Pendula.
Each Pendulum characterised by
couple coefficient lambd,
Pendulum's number,
and Pendulum self frequency coefficient omega.

Pendula present in KuramotoSystem class by list.
"""

class KuramotoSystem:
    """
    class KS implementation;
    don't know what else;
    """
    def __init__(self, omega_vector, lambd, A, phase_vector, t0, tf, N):
        """
        :param omega_vector: vector of constant
        :param lambd: coupling strength  (for all pendulums)
        :param A: 2d vector - couple coefficient Aij
        :param phase_vector: vector of constant. In rk4 it called initial_conditions

        :param t0: start time
        :param tf: final time (greater than start time)
        :param N: number of time divisions
        """
        self.omega_vector = omega_vector
        self.lambd = lambd
        self.A = A
        self.phase_vector = phase_vector

        self.N = N
        self.t0 = t0
        self.tf = tf

        self.vfunc = []
        for i in range(len(omega_vector)):
            self.vfunc.append(Pendulum(lambd, A, i, omega_vector[i]))

    def get_solution_iterator(self):
        """
        :return: Runge-Kutt function result////, wich is ITERATOR
        """
        pendulum_time_output_array = []
        pendulum_phase_output_array = []
        for array in rk4.runge(self.t0, self.tf, self.phase_vector, self.N, self.vfunc):
            pendulum_time_output_array.append(array[0])
            for i in range(len(array[1])):
                pendulum_phase_output_array.append(array[1][i])
        return pendulum_time_output_array, pendulum_phase_output_array

    #def push_to_the_file(self, filename): - see in the shell modul




class Pendulum:
    def __init__(self, lambd, A, pendulum_index, omega):  # lambd -- A[i]
        """
        Parameters will add by the KuramotoSystem class,
        NOT BY USER.
        :param lambd: coupling strength
        :param A: adjacency matrix /матрица смежности i - current pendulum index; j - indexes of his ties / индексы его связей
        :param pendulum_index:
        :param omega:
        """
        self.lambd = lambd
        self.pendulum_index = pendulum_index
        self.omega = omega
        self.A = A

    def calculate(self, phase_vector):
        """
        calculate "phase speed" for our pendulum by the governing equation.
        will use by the Pendulum.__call__ ,
        NOT BY USER
        :param phase_vector: 1d vector --  phases
        :return: pendulum function
        """
        summ = 0
        #print(phase_vector)
        #print(self.pendulum_index)
        my_phase = phase_vector[self.pendulum_index]
        for j in range(len(phase_vector)):
            summ += self.A[self.pendulum_index][j] * math.sin(phase_vector[j] - my_phase)
        return self.omega + self.lambd * summ/len(phase_vector)

    def __call__(self, t, point , phase_vector):
        """
        will work inside Runge-Kutte method,
        NOT BY USER
        :param t:
        :param point:
        :param phase_vector:
        :return:
        """
        return self.calculate(phase_vector)

'''
class RCoeffisient: #dont usable now
    def __init__(self, lambd, pendulum_index, omega):
        """
        Parameters will add by the KuramotoSystem class,
        NOT BY USER.
        :param lambd:
        :param pendulum_index:
        :param omega:
        """
        self.lambd = lambd
        self.pendulum_index = pendulum_index
        self.omega = omega

    def calculate(self, phase_vector):
        """
        calculate "phase speed" for our pendulum by the governing equation.
        will use by the Pendulum.__call__ ,
        NOT BY USER
        :param phase_vector: 1d vector --  phases
        :return: pendulum function
        """
        summ = 0
        my_phase = phase_vector[self.pendulum_index]
        for i in range(len(phase_vector)):
            summ += self.lambd[i] * math.sin(phase_vector[i] - my_phase)
        return self.omega + summ / self.pendulum_index

    def __call__(self, t, point, phase_vector):
        """
        will work inside Runge-Kutte method,
        NOT BY USER
        :param t:
        :param point:
        :param phase_vector:
        :return:
        """
        return self.calculate(phase_vector)
'''

