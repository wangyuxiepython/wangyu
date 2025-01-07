import open3d as o3d
import numpy as np
import copy
import matplotlib.pyplot as plt

def draw_registration_result(source, target, transformation):
    # 分别显示的是源点云，目标点云，
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0, 0])  # 源点云上红色
    target_temp.paint_uniform_color([0, 1, 0])  # 目标点云上绿色
    source_temp.transform(transformation)  # 对源点云进行矩阵的变换
    # 变换后和目标点云一起显示
    o3d.visualization.draw_geometries([source_temp, target_temp],)
                                      # zoom=0.4559,
                                      # front=[0.6452, -0.3036, -0.7011],
                                      # lookat=[1.9892, 2.0208, 1.8945],
                                      # up=[-0.2779, -0.9482, 0.1556])


def pick_points(pcd):
    print("1) 按 [shift + 左击]采点")
    print("   按 [shift + 右击] 撤销拾取的点")
    print("2) 拾取点后，按“Q”关闭窗口")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()
    vis.destroy_window()
    return vis.get_picked_points()


def cont_dist(pcd):
    print("选择鼻尖到左脚爪的对应点")
    points = pick_points(pcd)
    point1 = np.array(pcd.points[points[0]])
    point2 = np.array(pcd.points[points[1]])
    distance = np.linalg.norm(point1 - point2)
    return distance
    #采集源点云与目标点云相同对应点的距离

source = o3d.io.read_point_cloud("denoised.pcd")#=================采集图到CAD
target = o3d.io.read_point_cloud("lookup.pcd")
# target = o3d.io.read_point_cloud("denoised.pcd")#=================CAD到采集图
# source = o3d.io.read_point_cloud("lookup.pcd")


target_diag = cont_dist(target)
source_diag = cont_dist(source)
scale_factor = target_diag / source_diag# 计算缩放因子
a = np.identity(4)
a[:3, :3] *= scale_factor
source = source.transform(a) #对原点云进行放缩


picked_id_source = pick_points(source)
picked_id_target = pick_points(target)
assert (len(picked_id_source) >= 3 and len(picked_id_target) >= 3),"至少选三个点"
assert (len(picked_id_source) == len(picked_id_target)),"两组点应该有相同的顺序与数量"
corr = np.zeros((len(picked_id_source), 2))  #选对应点，至少三对


corr[:, 0] = picked_id_source
corr[:, 1] = picked_id_target
p2p = o3d.pipelines.registration.TransformationEstimationPointToPoint()
trans_init = p2p.compute_transformation(source, target,o3d.utility.Vector2iVector(corr))
source = source.transform(trans_init)
# 计算原点云到目标点云的转换矩阵，并对原点云进行转换


threshold = 0.02
trans_init = np.eye(4)  # 初始变换矩阵为单位矩阵
reg_p2p = o3d.pipelines.registration.registration_icp(
    source, target, threshold, trans_init,
    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=20)
)
draw_registration_result(source, target,reg_p2p.transformation)
source = source.transform(reg_p2p.transformation)
#o3d.io.write_point_cloud("icp.pcd", source)
# 调用ICP算法，进行敬配准


# source = o3d.io.read_point_cloud("icp.pcd")#==========直接用保存的icp后的点云计算
# target = o3d.io.read_point_cloud("lookup.pcd")
# cl, ind = source.remove_statistical_outlier(nb_neighbors=5, std_ratio=.5)
#
# transformation = np.identity(4)
# transformation[0,3] = 1
# pcd_clean = source.select_by_index(ind)
# draw_registration_result(source, pcd_clean, transformation )
# # # 可视化去噪后的点云
# o3d.visualization.draw_geometries([pcd_clean])
# # o3d.visualization.draw_geometries([source, target],)

distances = source.compute_point_cloud_distance(target)
distances_1 = target.compute_point_cloud_distance(source)
dist_x = np.asarray(distances)
cmap = plt.get_cmap('jet')
dist_min = np.min(dist_x)
dist_max = np.max(dist_x)
print(dist_min, dist_max)
a = np.linspace(dist_min, dist_max, 1000)[:, np.newaxis]
b = np.repeat(a, 200, axis=1, )
plt.imshow(b, cmap=cmap, vmin=dist_min, vmax=dist_max)
plt.colorbar()
plt.show()
dist_x = (dist_x - dist_min) / (dist_max - dist_min)
# dist_x = dist_x / 2 + 0.5
colors = cmap(dist_x)[:, :3]
#colors = (colors * 255).astype(np.uint8)
target.paint_uniform_color([0, 1, 0])
source.colors = o3d.utility.Vector3dVector(colors)
# 对点云添加颜色并进行可视化
o3d.visualization.draw_geometries([source,],)

