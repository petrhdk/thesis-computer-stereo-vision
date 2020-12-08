# --TASK-- visualize located objects based on datafile

import bpy, json
from calibration import get_calibration
from generate_mesh import generate_mesh

# load data
data_file = open('<source_datafile_path>', 'r')
data = json.loads(data_file.read())
data_file.close()

# iterate frames in data
for frame_count, frame_data in data.items():
	
	# generate mesh for located objects
	vertices = []
	edges = []
	for obj in frame_data['objects']:
		vertices.append(tuple(obj['X']))
	bpy.context.scene.frame_set(int(frame_count))
	generate_mesh(vertices, edges, color=(0.9, 1.0, 0.0), vertex_size_factor=4.0, single_frame=True)

	# generate mesh for camera rays
	calibration = get_calibration()
	for obj in frame_data['objects']:
		vertices = [
			tuple(calibration['X0_A']) + ('X0_A',),
			tuple(calibration['X0_B']) + ('X0_B',),
			tuple(obj['X']) + ('X',)
		]
		edges = [
			('X0_A','X'),
			('X0_B','X'),
		]
		generate_mesh(vertices, edges, color=(0.9, 1.0, 0.0), render_vertices=False, single_frame=True)

# set keyframe range of animation
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = len(data.keys())-1
