#Switch the camera of current actived 3d view to persp camera.
import maya.mel as mel
mel.eval('MGP_SetActiveViewCamera "persp"');   #To-Do: replace the string with the camera name you wanna switch to.