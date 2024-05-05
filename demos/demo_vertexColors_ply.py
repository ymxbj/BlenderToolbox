import blendertoolbox as bt
import bpy
import os
import numpy as np
from mathutils import Vector
cwd = os.getcwd()

gpu_id = 7
os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_id}"

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons["cycles"].preferences.get_devices()
print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
for d in bpy.context.preferences.addons["cycles"].preferences.devices:
    d["use"] = 1 # Using all devices, include GPU and CPU
    print(d["name"], d["use"])
bpy.context.preferences.addons["cycles"].preferences.compute_device_type = 'CUDA'
device_type = bpy.context.preferences.addons['cycles'].preferences.compute_device_type

"""
Warning: this function may be obsolete: please check out demo_vertexColors.py and demo_faceColors.py
"""

## initialize blender
imgRes_x = 1080
imgRes_y = 1080
numSamples = 200
exposure = 1.5

category = 'rifle'

## read mesh (choose either readPLY or readOBJ)
location = (0, 0, 0.5) # (UI: click mesh > Transform > Location)
rotation = (90, 0, eval(f'bt.{category}_azimuth')) # (UI: click mesh > Transform > Rotation)
scale = (0.5, 0.5, 0.5) # (UI: click mesh > Transform > Scale)

## read mesh (choose either readPLY or readOBJ)

mesh_dir = f'/data/xiongbj/BlenderToolbox/display_{category}_ply'

output_dir = f'/data/xiongbj/BlenderToolbox/{category}_rgb_images'

os.makedirs(output_dir, exist_ok = True)

meshes = os.listdir(mesh_dir)

for mesh in meshes:

    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

    meshPath = os.path.join(mesh_dir, mesh)

    index = mesh[:-4]

    mesh = bt.readMesh(meshPath, location, rotation, scale)

    outputPath = os.path.join(output_dir, f'{index}.png')

    # # set material (TODO: this has some new issue due to new version of Blender)
    meshVColor = bt.colorObj([], 0.5, 1.0, 1.0, 0.0, 0.0)
    bt.setMat_VColor(mesh, meshVColor)

    bound = [bpy.context.object.matrix_world @ Vector(bbox_co[:]) for bbox_co in bpy.context.object.bound_box[:]]
    ## set invisible plane (shadow catcher)
    bt.invisibleGround(location = (0,0,bound[0].z - 0.03), shadowBrightness=0.9)

    ## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
    camLocation = (3, 0, 2)
    lookAtLocation = (0,0,0.5)
    focalLength = 90 # (UI: click camera > Object Data > Focal Length)
    cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

    ## set light
    lightAngle = (6, -30, -155)
    strength = 2
    shadowSoftness = 0.3
    sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

    ## set ambient light
    bt.setLight_ambient(color=(0.1,0.1,0.1,1))

    ## set gray shadow to completely white with a threshold
    bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

    ## save blender file so that you can adjust parameters in the UI
    bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

    ## save rendering
    bt.renderImage(outputPath, cam)
