import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
def main():
    ply_path='pcd.ply'#即定义所打开ply文件相对位置
    ply_data=o3d.io.read_point_cloud(ply_path)#将文件打开以获取点云数据
    points_coord=np.asarray(ply_data.points)#用numpy来将点数据变换为三维坐标数组
    window = plt.figure()#新建窗口
    sub = window.add_subplot(111, projection='3d')#设定子图
    sub.scatter(points_coord[:, 0], points_coord[:, 1], points_coord[:, 2], color='red', s=0.5)
    '''坐标数组中第一列表示x轴坐标，第二列表示y轴坐标，第三列表示z轴坐标'''
    sub.set_xlabel('X')
    sub.set_ylabel('Y')
    sub.set_zlabel('Z')#为三个坐标轴设置标签
    plt.title('3D Point Cloud')#图表标题
    plt.show()#显示图表
if __name__=="__main__":
    main()