from config.config_creator import create_config
import numpy as np
import math
import time

try:
    from main.OCL_v2 import ad
except:
    import sys
    rank=0
    print("shell running without opencl", file=sys.stderr)

try:
    from mpi4py import MPI
    import KuramotoSystem as cls
    comm = MPI.COMM_WORLD
    size = comm.Get_size()  # количество узлов
    rank = comm.Get_rank()  # номер узла
except:
    import sys
    rank=0
    print("rk4 running without mpi", file=sys.stderr)



class Timer:
    def __init__(self):
        self.t = 0

    def start(self):
        self.t = time.perf_counter()
        return self

    def stop(self):
        self.t = time.perf_counter()-self.t
        return self.t


#'kuramoto_config.ini'
def load_kuramotosystem_from_config(config):
    return cls.KuramotoSystem(config['omega_vector'], config['lambd'], config['Aij'], config['phase_vector'], config['t0'], config['tf'], config['N'], config['oscillators_number'])


def get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number):
    """
    camculate parametr r
    :param time_output_array_length:
    :param pendulum_phase_output_array:
    :param oscillators_number:
    :return:
    """
    r = np.zeros(time_output_array_length)
    for i in range(time_output_array_length):
        sum_cos = 0
        sum_sin = 0
        for j in pendulum_phase_output_array[i]:
            sum_cos += math.cos(j)
            sum_sin += math.sin(j)

        x = sum_cos/oscillators_number
        y = sum_sin/oscillators_number
        try:
            r[i] = (x**2 + y**2)**0.5
        except:
            r[i] = None
            print("CALCULATE R EXCEPTION")


    return r

def run_K_model(flag, osc_min=1, osc_max=101, osc_step=10):

    for oscillators_number in np.arange(osc_min, osc_max, osc_step):
        config = None
        if rank == 0:
            config = create_config(oscillators_number=oscillators_number, filename=None)
        config= comm.bcast(config, root=0)
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config) #= i+1)    #loading

        if rank == 0:   #calculate
            timer = Timer().start()

        pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution() #system with 1~10 pendulums

        time_output_array_length = len(pendulum_time_output_array)
        pendulum_phase_output_array = np.array(pendulum_phase_output_array).reshape((time_output_array_length, oscillators_number))

        pendulum_phase_output_array = (pendulum_phase_output_array % (2*math.pi))

        pendulum_phase_output_array = np.array([[math.sin(i) for i in e] for e in pendulum_phase_output_array])     ###### cut this string out for radian graph

        if rank==0 :     #write in file
            if "time" in flag:
                timer_result = timer.stop()
                print("Calculate time", timer_result)
                with open("result_txt//time.txt", "a") as myfile: #timer stuff
                    myfile.write(str(timer_result)+"\n") #str(oscillators_number)+" "+
            if "phase" in flag:
                with open("result_txt//test"+str(oscillators_number)+".txt", "w") as myfile:  #plot: phase(time)
                    for i in range(time_output_array_length):
                        myfile.write(str(pendulum_time_output_array[i])+" "+" ".join(str(x) for x in pendulum_phase_output_array[i])+"\n")
            if "r" in flag:    #write in file
                r = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)  # ------------calculating r(t)-------------
                with open("result_txt//testr"+str(oscillators_number)+".txt", "w") as myfile: #plot: r(time)
                    for i in range(time_output_array_length):
                        myfile.write(str(pendulum_time_output_array[i]) + " " + str(r[i]) + "\n")


def run_RLambd_model(flag, lmb_min=0, lmb_max=2.5, lmb_step=0.1, oscillators_number = 10):
    r_out = []
    lambd_out = np.arange(lmb_min, lmb_max, lmb_step)
    if rank == 0:
        timer = Timer().start()

    for _lambda in lambd_out:
        config = None
        if rank == 0:
            config = create_config(lambd=_lambda, oscillators_number=oscillators_number, filename=None)
        config = comm.bcast(config, root=0)
        kuramotosystem_class_exemplar = load_kuramotosystem_from_config(config)  # = i+1)    #loading

        pendulum_time_output_array, pendulum_phase_output_array = kuramotosystem_class_exemplar.get_solution()  # system with 1~10 pendulums

        time_output_array_length = len(pendulum_time_output_array)
        pendulum_phase_output_array = np.array(pendulum_phase_output_array).reshape((time_output_array_length, oscillators_number))
        pendulum_phase_output_array = pendulum_phase_output_array % (2 * math.pi)
        pendulum_phase_output_array = np.array([[math.sin(i) for i in e] for e in pendulum_phase_output_array])  ###### cut this string out for radian graph
        r_array = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)
        n = int(len(r_array) / 2)
        r_out.append( sum(r_array[-n:])/n)
        # ------------calculating r-------------
        #r_out.append( sum(r_array[-5:-1])/len(r_array[-5:-1]) )


    if rank==0 :     #write in file
        if "time" in flag:
            timer_result = timer.stop()
            print("Calculate time", timer_result)
            with open("result_txt//time_r(lambda).txt", "w") as myfile:  # timer stuff
                myfile.write(str(oscillators_number) + " " + str(timer_result) + "\n")
        if "r" in flag:  # write in file
            with open("result_txt//test_r(lambda).txt", "w") as myfile:  # plot: r(time)
                for i in range(len(r_out)):
                    myfile.write(str(lambd_out[i]) + " " + str(r_out[i]) + "\n")
            with open("result_txt//testr" + str(oscillators_number) + ".txt", "w") as myfile:  # plot: r(time)
                for i in range(time_output_array_length):
                    myfile.write(str(pendulum_time_output_array[i]) + " " + str(r_array[i]) + "\n")

        ...

def run_OCL(flag, osc_min=1, osc_max=101, osc_step=10):
    #osc: oscillators number

    for oscillators_number in np.arange(osc_min, osc_max, osc_step):
        config = create_config(oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)
        if rank == 0:
            timer = Timer().start()
        pendulum_phase_output_array, pendulum_time_output_array = ad(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']

        if rank == 0:  # write in file
            timer_result = timer.stop()
            if "time" in flag:
                print("Calculate time", timer_result)
                with open("result_txt//time.txt", "a") as myfile:  # timer stuff
                    myfile.write(str(oscillators_number)+" "+str(timer_result) + "\n")  # str(oscillators_number)+" "+
            if "phase" in flag:
                with open("result_txt//test" + str(oscillators_number) + ".txt", "w") as myfile:  # plot: phase(time)
                    for i in range(time_output_array_length):
                        myfile.write(str(config['h']*i) + " " + " ".join(str(x) for x in pendulum_phase_output_array[i]) + "\n")
            if "r" in flag:  # write in file
                r = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)  # ------------calculating r(t)-------------
                with open("result_txt//testr" + str(oscillators_number) + ".txt", "w") as myfile:  # plot: r(time)
                    for i in range(time_output_array_length):
                        myfile.write(str(config['h']*i) + " " + str(r[i]) + "\n")
# заметка - генератор конфига паралелиться не будет - программа готова! дальше работа над дипломной! и дописание небходимых возможностей подсчёта


def run_OCL_RLambd(flag, lmb_min=0, lmb_max=2.5, lmb_step=0.1, oscillators_number = 10):
    r_out = []
    lambd_out = np.arange(lmb_min, lmb_max, lmb_step)

    if rank == 0:
        timer = Timer().start()

    for _lambda in lambd_out:
        config = create_config(lambd=_lambda, oscillators_number=oscillators_number, filename=None)

        phase_vector = np.zeros((config['N'], oscillators_number), dtype=np.float32)
        phase_vector[0] = config['phase_vector']

        omega_vector = np.array(config['omega_vector'], dtype=np.float32)
        Aij = np.array(config['Aij'], dtype=np.float32)

        pendulum_phase_output_array, pendulum_time_output_array = ad(omega_vector, config['lambd'], Aij, phase_vector, a=config['t0'], b=config['tf'], oscillators_number=config['oscillators_number'], N_parts=config['N'])
        time_output_array_length = config['N']
        r_array = get_r(time_output_array_length, pendulum_phase_output_array, oscillators_number)
        n = 1000
        r_out.append( sum(r_array[-n:])/n)

    if rank==0 :     #write in file
        if "time" in flag:
            timer_result = timer.stop()
            print("Calculate time", timer_result)
            with open("result_txt//time_r(lambda).txt", "w") as myfile:  # timer stuff
                myfile.write(str(oscillators_number) + " " + str(timer_result) + "\n")
        if "r" in flag:  # write in file
            with open("result_txt//test_r(lambda).txt", "w") as myfile:  # plot: r(time)
                for i in range(len(r_out)):
                    myfile.write(str(lambd_out[i]) + " " + str(r_out[i]) + "\n")
            with open("result_txt//testr" + str(oscillators_number) + ".txt", "w") as myfile:  # plot: r(time)
                for i in range(time_output_array_length):
                    myfile.write(str(config['h']*i) + " " + str(r_array[i]) + "\n")
    ...

if __name__ == '__main__':
    flag = {"time","phase","r"}     #flag = {"time", "phase", "r"}
    """
    "time" -> time(oscillators_number) measuring
    "phase" -> phase(time) measuring
    "r" -> r(time) measuring
    """
    with open("result_txt//time.txt", "w") as myfile: #reset previous notes in time.txt
        ...
    #run_OCL(flag, osc_min=10, osc_max=20, osc_step=10)
    #run_OCL(flag, osc_min=5000, osc_max=10000, osc_step=100)
    #run_OCL_RLambd(flag, lmb_min=0, lmb_max=0.4, lmb_step=0.01, oscillators_number=10)


    #Note: change N in config creator: from 200 to 2000
    #Note: Look for time.txt in ./result_txt

    # ====performance OCL tests==============
    run_OCL(flag, osc_min=1000, osc_max=1001, osc_step=20)
    #run_OCL(flag, osc_min=1000, osc_max=1100, osc_step=100)
    #==================

    #====performance MPI tests==============
    #run_K_model(flag, osc_min=100, osc_max=1000, osc_step=20)
    #run_K_model(flag, osc_min=1000, osc_max=1100, osc_step=100)
    #===================

    #run_RLambd_model(flag, lmb_min=0, lmb_max=0.7, lmb_step=0.001, oscillators_number = 10)


    #import PyQt5
    #from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
    #TODO import run.py  functions in UI.py. Run them, if button clicked.

    import UI
    UI.initUI()

#unknown Loopies
