import numpy as np
import math
import matplotlib.pyplot as plt
pi=math.pi
phase_map=np.load('phase_m_1.npy')
phase_map_1=np.load('phase_s.npy')
def phase_unwrapping( phase_map , phase_map_1):
    j = 0
    print(phase_map[2047, 2559])
    while j < 2560:
        i = 1
        while i < 2048:
            variable_1=phase_map_1[i, j]*40-phase_map[i,j]/(2*pi)
            phase_map[i,j]+= round(variable_1)*2*pi
            i+=1
        j+=1
    plt.imshow(phase_map)
    plt.show()
if __name__ == '__main__':
    phase_unwrapping(phase_map, phase_map_1)










'''i=0
j=0
x=1
print(phase_map[2047,2559])
while j < 2560:
    i=1
    x=0
    while i < 2048:
        k=3
        if phase_map[i,j] >= 0:
            k=phase_map[i-1,j]-phase_map[i,j]
        if abs(k) > 6:
            x+=1
            phase_map[i, j] += x*2*pi
        i += 1
    j+=1
plt.imshow(phase_map)
plt.show()'''


