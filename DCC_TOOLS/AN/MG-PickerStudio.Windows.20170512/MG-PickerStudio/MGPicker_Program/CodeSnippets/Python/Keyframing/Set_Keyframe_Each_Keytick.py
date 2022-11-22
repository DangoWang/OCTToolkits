#Set keyframe each keytick via time range control.The ensure each selected object all have keys at same frames.
import maya.mel as mel
mel.eval('MGP_SetKeyframeEachKeyOrGap 0') #arg: 0 for each keytick, 1 for each certain frames.
