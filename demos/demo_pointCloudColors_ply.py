import blendertoolbox as bt
import bpy
import os
import numpy as np
from plyfile import PlyData
cwd = os.getcwd()

outputPath = os.path.join(cwd, './demo_pointCloudColors.png') # make it abs path for windows

## initialize blender
imgRes_x = 1080
imgRes_y = 1080
numSamples = 200
exposure = 1.5
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

pointcloud_path = 'spot_UV.ply'
plydata = PlyData.read(pointcloud_path)

vertices = plydata['vertex']
x = np.array(vertices['x'])
y = np.array(vertices['y'])
z = np.array(vertices['z'])

r = np.array(vertices['red'] / 255.0)
g = np.array(vertices['green'] / 255.0)
b = np.array(vertices['blue'] / 255.0)

P = np.stack((x, y, z), axis=1)
PC = np.stack((r, g, b), axis=1)

## read mesh
location = (1.12, -0.14, 0)
rotation = (90, 0, 227)
scale = (1.5,1.5,1.5)
mesh = bt.readNumpyPoints(P,location,rotation,scale)

## add color to point cloud
mesh = bt.setPointColors(mesh, PC)

## set material ptColor = (vertex_RGBA, H, S, V, Bright, Contrast)
ptColor = bt.colorObj([], 0.5, 1.0, 1.0, 0.0, 0.0)
ptSize = 0.014
bt.setMat_pointCloudColored(mesh, ptColor, ptSize)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 60 # (UI: click camera > Object Data > Focal Length)
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
