import random
kuramoto_config = open('kuramoto_config.ini', 'w')

kuramoto_config.write("""[DEFAULT]

[visible]
""")
#-----------------------------
oscillators_number = 112
#----------------------------
kuramoto_config.write("oscillators_number = " + str(oscillators_number) + "\n")    #N ~~ oscillators_number
kuramoto_config.write("lambd = " + "0.05" + "\n")    #lambd ~~ lambd ~~ all coupling map
kuramoto_config.write("""
[invisible]
""")
#----------omega_vector----------------
omega_vector = ''
for i in range(oscillators_number):
    omega_vector += ' ' + str(round(random.uniform(0.05, 0.2), 2)) #DONT TOCH

kuramoto_config.write("omega_vector = " + omega_vector + "\n") #omega_i ~~ omega_wector[i]
#--------------------------
#-----------Aij---------------
Aij = ''
for i in range(oscillators_number):
    #Aij += "\n"
    for j in range(oscillators_number):
        #Aij += ' ' + str(1)
        if i!=j:
            Aij += ' ' + str(1)
        else:
            Aij += ' ' + str(0) #str(round(random.uniform(0,1), 2))
kuramoto_config.write("Aij = " + Aij + "\n") #A_ij ~~ oscillators_number^2   NOW enabled
#--------------------------

#-----------phase_vector---------------
phase_vector = ''
for i in range(oscillators_number):
    phase_vector += ' ' + str(round(random.uniform(0, 12), 2)) #str((i+1) * 0.1)#
kuramoto_config.write("phase_vector = " + phase_vector + "\n") #teta_i ~~ phase_vector[i]
#--------------------------

kuramoto_config.write("""t0 = 0
tf = 100
N = 1000""")


"""
5 oscillators = 0.3196
10 = 0.4721
50 = 4.1638
75 = 8.4893
100 oscillators = 14.8766
112 = 19.0881
"""