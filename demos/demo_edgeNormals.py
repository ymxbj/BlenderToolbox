import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
cwd = os.getcwd()

outputPath = os.path.join(cwd, './demo_edgeNormals.png') # make it abs path for windows

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh (choose either readPLY or readOBJ)
meshPath = '../meshes/frog_paparazzi_l0.obj'
location = (-0.38,0,0.29) # (UI: click mesh > Transform > Location)
rotation = (0, 0, 58.6) # (UI: click mesh > Transform > Rotation)
scale = (1,1,1) # (UI: click mesh > Transform > Scale)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading 
angle = 10
bt.edgeNormals(mesh, angle)

## subdivision
bt.subdivision(mesh, level = 2)

# # set material
meshColor = bt.colorObj(bt.derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
AOStrength = 0.0
bt.setMat_singleColor(mesh, meshColor, AOStrength)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
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