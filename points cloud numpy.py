import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
'''from mpl_toolkits.mplot3d import Axes3D

def read_ply_file(ply_file_path):
    """读取PLY文件并返回点云对象"""
    pcd = o3d.io.read_point_cloud(ply_file_path)
    return pcd

def extract_points(pcd):
    """从点云对象中提取点坐标"""
    points = np.asarray(pcd.points)
    return points

def visualize_point_cloud(points):
    """使用matplotlib可视化点云"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='blue', s=1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D Point Cloud')
    plt.show()

def main():
    ply_file_path = 'pcd.ply'  # 替换为你的PLY文件路径
    pcd = read_ply_file(ply_file_path)
    points = extract_points(pcd)
    print("Point cloud shape:", points.shape)
    visualize_point_cloud(points)

if __name__ == "__main__":
    main()'''

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
#p_out的值即是Up

#new_values_positive = (Fpu * Tx - Tz * (p_out - Up0)) / (Jz * (p_out - Up0) - Fpu * Jx)
 # 创建一个与p_out形状相同的数组，填充-1
#p_out = np.where(p_out > 0, new_values_positive, new_values_negative)
new_values_z = (Fpu * Tx - Tz * (p_out - Up0)) / (Jz * (p_out - Up0) - Fpu * Jx)
new_values_x = new_values_z * (i - Uc0) / Fcu
new_values_y = new_values_z * (j - Vc0) / Fcv
new_values_negative = np.full_like(p_out, -1000)
z_out = np.where(p_out > 0, new_values_z, new_values_negative)
x_out = np.where(p_out > 0, new_values_x, new_values_negative)
y_out = np.where(p_out > 0, new_values_y, new_values_negative)
#print(z_out)
'''plt.imshow(p_out)
plt.colorbar()
plt.show()
plt.imshow(x_out)
plt.colorbar()
plt.show()
plt.imshow(y_out)
plt.colorbar()
plt.show()
plt.imshow(z_out)
plt.colorbar()
plt.show()
'''
z = z_out[(z_out > -600)]
x = x_out[(x_out > -600)]
y = y_out[(y_out > -600)]
'''assert x_out.shape == y_out.shape == z_out.shape

# 使用 numpy.dstack 将三个数组堆叠成一个三维数组
# 然后使用 reshape 将结果重塑为 (-1, 3) 形状，其中每行是一个点的 (x, y, z) 坐标
points = np.dstack((x_out, y_out, z_out))
points = points.reshape(-1, 3)'''
points = np.column_stack((x, y, z))
#print(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制点云
ax.scatter(points[:, 0], points[:, 1], points[:, 2])

# 设置坐标轴标签
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_zlabel('Z ')


# 显示图形
plt.show()