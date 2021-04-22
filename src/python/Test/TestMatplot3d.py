from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpathes

xy1 = np.array([0.2,0.2, 0])
xy2 = np.array([0.2,0.8, 0])
xy3 = np.array([0.8,0.2])
xy4 = np.array([0.8,0.8])
xy5 = np.array([[0.5, 0.1], [0.7, 0.3], [0.7, 0.6], [0.2, 0.4], [0.5, 0.1]])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#圆形
circle = mpathes.Circle(xy1,0.05, edgecolor='red', 
#facecolor='black'
fill=False
)
ax.add_patch(circle)
art3d.pathpatch_2d_to_3d(circle, z=0.3, zdir='z')
#长方形
rect = mpathes.Rectangle(xy2,0.2,0.1,color='r')
ax.add_patch(rect)
art3d.pathpatch_2d_to_3d(rect, z=0.1, zdir='z')
#多边形
polygon = mpathes.RegularPolygon(xy3,5,0.1,color='g',fill=False)
ax.add_patch(polygon)
art3d.pathpatch_2d_to_3d(polygon, z=0.7, zdir='z')
# #椭圆形
# ellipse = mpathes.Ellipse(xy4,0.4,0.2,color='y')
# ax.add_patch(ellipse)
# art3d.pathpatch_2d_to_3d(polygon, z=0.7, zdir='z')

#多边形
polygon_norm = mpathes.Polygon(xy5, color='y')
ax.add_patch(polygon_norm)
art3d.pathpatch_2d_to_3d(polygon_norm, z=0.7, zdir='z')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)

plt.show()