# --TASK-- visualize cameras in blender scene

from calibration import get_calibration
from helper_functions import ray_endpoint
from generate_mesh import generate_mesh

# load calibration
calibration = get_calibration()
locals().update(calibration)

# generate mesh for camera A
vertices = []
edges = []
vertices.append( tuple(calibration['X0_A']) + ('X0_A',) )
vertices.append( tuple(ray_endpoint(X0_A, KI_A, RT_A, x=(0,0), length=2)) + ('topleft_ray_A',) )
vertices.append( tuple(ray_endpoint(X0_A, KI_A, RT_A, x=(0,1080), length=2)) + ('bottomleft_ray_A',) )
vertices.append( tuple(ray_endpoint(X0_A, KI_A, RT_A, x=(1920,1080), length=2)) + ('bottomright_ray_A',) )
vertices.append( tuple(ray_endpoint(X0_A, KI_A, RT_A, x=(1920,0), length=2)) + ('topright_ray_A',) )
edges.append(('X0_A','topleft_ray_A'))
edges.append(('X0_A','bottomleft_ray_A'))
edges.append(('X0_A','bottomright_ray_A'))
edges.append(('X0_A','topright_ray_A'))
edges.append(('topleft_ray_A','bottomleft_ray_A'))
edges.append(('bottomleft_ray_A','bottomright_ray_A'))
edges.append(('bottomright_ray_A','topright_ray_A'))
edges.append(('topright_ray_A','topleft_ray_A'))
generate_mesh(vertices, edges, color=(0.0, 1.00, 1.00))

# generate mesh for camera B
vertices = []
edges = []
vertices.append( tuple(calibration['X0_B']) + ('X0_B',) )
vertices.append( tuple(ray_endpoint(X0_B, KI_B, RT_B, x=(960,540), length=10000)) + ('center_ray_B',) )
vertices.append( tuple(ray_endpoint(X0_B, KI_B, RT_B, x=(0,0), length=2)) + ('topleft_ray_B',) )
vertices.append( tuple(ray_endpoint(X0_B, KI_B, RT_B, x=(0,1080), length=2)) + ('bottomleft_ray_B',) )
vertices.append( tuple(ray_endpoint(X0_B, KI_B, RT_B, x=(1920,1080), length=2)) + ('bottomright_ray_B',) )
vertices.append( tuple(ray_endpoint(X0_B, KI_B, RT_B, x=(1920,0), length=2)) + ('topright_ray_B',) )
edges.append(('X0_B','center_ray_B'))
edges.append(('X0_B','topleft_ray_B'))
edges.append(('X0_B','bottomleft_ray_B'))
edges.append(('X0_B','bottomright_ray_B'))
edges.append(('X0_B','topright_ray_B'))
edges.append(('topleft_ray_B','bottomleft_ray_B'))
edges.append(('bottomleft_ray_B','bottomright_ray_B'))
edges.append(('bottomright_ray_B','topright_ray_B'))
edges.append(('topright_ray_B','topleft_ray_B'))
generate_mesh(vertices, edges, color=(0.0, 1.0, 0.0))
