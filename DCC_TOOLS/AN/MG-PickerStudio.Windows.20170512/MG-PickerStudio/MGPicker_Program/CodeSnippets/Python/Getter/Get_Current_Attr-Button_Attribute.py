#Get currently interactive attribute button's maya attribute:
#if the attribute is not linked to a maya attribute, this will return empty string.
#the return attribute string is of format: nodeName.attributeName. 
#argument: 0 for no namespace, 1 for has namespace.
import maya.mel as mel
attribute = mel.eval('MGP_GetCurrentAttributeButton_Attribute 0') 