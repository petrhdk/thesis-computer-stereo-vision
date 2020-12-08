# --TASK-- visualize calibration points in blender scene 

from calibration_points import get_calibration_points
from generate_mesh import generate_mesh

# load calibration points
calibration_points = get_calibration_points()

# generate mesh
vertices = []
edges = []
for cp in calibration_points:
    vertices.append(cp['X'])
generate_mesh(vertices, edges, color=(1.0, 0.0, 0.0), vertex_size_factor=2.0)
