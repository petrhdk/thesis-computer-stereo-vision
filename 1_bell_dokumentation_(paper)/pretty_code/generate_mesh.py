# --TASK-- generates a blender mesh of vertices and edges

import bpy

def generate_mesh(vertices, edges, color, render_vertices=True, vertex_size_factor=1.0, single_frame=False):
	# argument:  vertices = [ (X,Y,Z,label), ... ]
	# argument:  edges = [ (label1,label2), ... ]

	# generate mesh object
	mesh = bpy.data.meshes.new('mesh')
	mesh_obj = bpy.data.objects.new("MeshObject", mesh)

	# link object into scene
	scene = bpy.context.scene
	scene.objects.link(mesh_obj)

	# add vertices
	for vertex in vertices:
		mesh.vertices.add(1)
		mesh.vertices[-1].co = vertex[:3]
		
	# add edges
	for edge in edges:
		for vertex in vertices:
			if len(vertex)>3 and vertex[3]==edge[0]:
				index_point_1 = vertices.index(vertex)
			if len(vertex)>3 and vertex[3]==edge[1]:
				index_point_2 = vertices.index(vertex)
		mesh.edges.add(1)
		mesh.edges[-1].vertices = (index_point_1, index_point_2)

	# generate particle system for vertices
	if render_vertices:
		bpy.ops.mesh.primitive_uv_sphere_add(size=1.0, location=(0.0, 0.0, 0.0))
		uv_sphere = bpy.context.active_object
		material = bpy.data.materials.new(name="UVSphereParticleMaterial")
		material.diffuse_color = color
		uv_sphere.data.materials.append(material)
		uv_sphere.layers[1] = True
		uv_sphere.layers[0] = False
		particle_system_modifier = mesh_obj.modifiers.new(name="VertexParticles", type="PARTICLE_SYSTEM")
		particle_system_modifier.particle_system.settings.type = 'HAIR'
		particle_system_modifier.particle_system.settings.use_advanced_hair = True
		particle_system_modifier.particle_system.settings.count = len(vertices)
		particle_system_modifier.particle_system.settings.emit_from = 'VERT'
		particle_system_modifier.particle_system.settings.use_emit_random = False
		particle_system_modifier.particle_system.settings.render_type = 'OBJECT'
		particle_system_modifier.particle_system.settings.dupli_object = uv_sphere
		particle_system_modifier.particle_system.settings.particle_size = 0.025*vertex_size_factor


	# generate wire material for edges
	if len(edges)>0:
		material = bpy.data.materials.new(name='WireMaterial')
		material.type = 'WIRE' #'SURFACE'
		material.diffuse_color = color
		material.use_shadeless = True
		mesh.materials.append(material)

	# update
	mesh.update()

	# single frame
	if single_frame:
		scene.frame_set(scene.frame_current-1)
		mesh_obj.hide = True
		mesh_obj.keyframe_insert(data_path='hide')
		mesh_obj.hide_render = True
		mesh_obj.keyframe_insert(data_path='hide_render')

		scene.frame_set(scene.frame_current+2)
		mesh_obj.hide = True
		mesh_obj.keyframe_insert(data_path='hide')
		mesh_obj.hide_render = True
		mesh_obj.keyframe_insert(data_path='hide_render')

		scene.frame_set(scene.frame_current-1)
		mesh_obj.hide = False
		mesh_obj.keyframe_insert(data_path='hide')
		mesh_obj.hide_render = False
		mesh_obj.keyframe_insert(data_path='hide_render')
		
