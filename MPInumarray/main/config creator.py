import random
kuramoto_config = open('kuramoto_config.ini', 'w')

kuramoto_config.write("""[DEFAULT]

[visible]
""")
#-----------------------------
oscillators_number = 5
#----------------------------
kuramoto_config.write("oscillators_number = " + str(oscillators_number) + "\n")    #N ~~ oscillators_number
kuramoto_config.write("lambd = " + "2.5" + "\n")    #lambd ~~ lambd ~~ all coupling map
kuramoto_config.write("""
[invisible]
""")
#----------omega_vector----------------
omega_vector = ''
for i in range(oscillators_number):
    omega_vector += str( i*0.1 )+' '  # + str(round(random.uniform(1, 2), 2))

kuramoto_config.write("omega_vector = " + omega_vector + "\n") #omega_i ~~ omega_wector[i]
#--------------------------
#-----------Aij---------------
Aij = ''
for i in range(oscillators_number):
    for j in range(oscillators_number):
        #Aij += ' ' + str(1)
        Aij += ' ' + str(round(random.uniform(0,1), 2))
kuramoto_config.write("Aij = " + Aij + "\n") #A_ij ~~ oscillators_number^2   NOW enabled
#--------------------------

#-----------phase_vector---------------
phase_vector = ''
for i in range(oscillators_number):
    phase_vector += ' ' + str((i+1) * 0.1)#str(round(random.uniform(0, 12), 2))
kuramoto_config.write("phase_vector = " + phase_vector + "\n") #teta_i ~~ phase_vector[i]
#--------------------------

kuramoto_config.write("""t0 = 0
tf = 1000
N = 1000""")


"""
import random
random.randint(0,10)
"""