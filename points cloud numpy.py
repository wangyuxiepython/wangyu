import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
p_out=np.load('phase_map.npy')
Fpv=2546.109
Tx=-0.7149
Tz=9.1538
Up0=979.677
Fpu=2548.264
R11=-0.9998
R12=-0.0144
R13=-0.0156
R31=-0.0132
R32=-0.1531
R33=0.9881
Uc0=1243.802
Vc0=1013.233
Fcu=5148.256
Fcv=5148.179
tm=27
p_out[np.where(p_out > 0)] *= (tm/2*np.pi) #求 Up
#p_out[np.where(p_out < 0)] = -20
i_indices = np.arange(p_out.shape[0])[:, np.newaxis]
j_indices = np.arange(p_out.shape[1])[np.newaxis, :]
i = i_indices
j = j_indices
Jx = R11 * (i - Uc0) / Fcu + R12 * (j - Vc0) / Fcv + R13
Jz = R31 * (i - Uc0) / Fcu + R32 * (j - Vc0) / Fcv + R33
new_values_z = (Fpu * Tx - Tz * (p_out - Up0)) / (Jz * (p_out - Up0) - Fpu * Jx)
new_values_x = new_values_z * (i - Uc0) / Fcu
new_values_y = new_values_z * (j - Vc0) / Fcv
new_values_negative = np.full_like(p_out, -1000)
z_out = np.where(p_out > 0, new_values_z, new_values_negative)
x_out = np.where(p_out > 0, new_values_x, new_values_negative)
y_out = np.where(p_out > 0, new_values_y, new_values_negative)
z = z_out[(z_out > -600)]
x = x_out[(x_out > -600)]
y = y_out[(y_out > -600)]
points = np.column_stack((x, y, z))
#print(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2])
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_zlabel('Z ')
plt.show()
