import os
import trimesh
import numpy as np

category = 'car'

# input_mesh_path = f'/data/xiongbj/BlenderToolbox/display_{category}'
input_mesh_path = '/data/xiongbj/BlenderToolbox/meshes'
# output_mesh_path = f'/data/xiongbj/BlenderToolbox/display_{category}_unit'
output_mesh_path = '/data/xiongbj/BlenderToolbox/cow_mesh_unit'

os.makedirs(output_mesh_path, exist_ok = True)

def scale_to_unit_sphere(mesh, evaluate_metric = False):
  if isinstance(mesh, trimesh.Scene):
    mesh = mesh.dump().sum()

  vertices = mesh.vertices - mesh.bounding_box.centroid
  distances = np.linalg.norm(vertices, axis=1)
  vertices /= np.max(distances)
  if evaluate_metric:
        vertices /= 2
  return trimesh.Trimesh(vertices=vertices, faces=mesh.faces)

meshes = os.listdir(input_mesh_path)
meshes = ['spot_UV.obj']

for mesh_name in meshes:
   print(mesh_name)
   mesh_path = os.path.join(input_mesh_path, mesh_name)
   target_path = os.path.join(output_mesh_path, mesh_name)
   mesh = trimesh.load(mesh_path, force = 'mesh')
   mesh = scale_to_unit_sphere(mesh)
   mesh.export(target_path)
