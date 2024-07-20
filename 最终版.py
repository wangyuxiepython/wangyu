import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
def main():
    ply_path='pcd.ply'#即定义所打开ply文件相对位置
    ply_shujv=o3d.io.read_point_cloud(ply_path)#将文件打开以获取点云数据
    points_zuobiao=np.asarray(ply_shujv.points)#用numpy来将点数据变换为三维坐标数组
    chuangkou = plt.figure()#新建窗口
    zitu = chuangkou.add_subplot(111, projection='3d')#设定子图
    zitu.scatter(points_zuobiao[:, 0], points_zuobiao[:, 1], points_zuobiao[:, 2], color='red', s=0.5)
    '''坐标数组中第一列表示x轴坐标，第二列表示y轴坐标，第三列表示z轴坐标'''
    zitu.set_xlabel('X')
    zitu.set_ylabel('Y')
    zitu.set_zlabel('Z')#为三个坐标轴设置标签
    plt.title('3D Point Cloud')#图表标题
    plt.show()#显示图表
if __name__=="__main__":
    main()