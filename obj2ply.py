import trimesh
import os
import numpy as np

category = 'rifle'

input_mesh_path = f'/data/xiongbj/BlenderToolbox/display_{category}_color'

output_mesh_path = f'/data/xiongbj/BlenderToolbox/display_{category}_ply'

os.makedirs(output_mesh_path, exist_ok = True)

meshes = os.listdir(input_mesh_path)

def scale_to_unit_sphere_in_place(mesh, evaluate_metric = False):
  if isinstance(mesh, trimesh.Scene):
    mesh = mesh.dump().sum()

  mesh.vertices = mesh.vertices - mesh.bounding_box.centroid
  distances = np.linalg.norm(mesh.vertices, axis=1)
  mesh.vertices /= np.max(distances)
  if evaluate_metric:
    mesh.vertices /= 2

for mesh in meshes:
    name = mesh[:-4]
    mesh_path = os.path.join(input_mesh_path, mesh)
    target_path = os.path.join(output_mesh_path, name + '.ply')

    mesh = trimesh.load(mesh_path, force='mesh')
    scale_to_unit_sphere_in_place(mesh)

    mesh.export(target_path)
