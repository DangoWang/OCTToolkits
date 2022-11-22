#Popup a prompt dialog, which user could input a frame count to keyframe object at this each frame count.
import maya.mel as mel
mel.eval('MGP_SetKeyframeEachKeyOrGap 1') #arg: 0 for each keytick, 1 for each certain frames.