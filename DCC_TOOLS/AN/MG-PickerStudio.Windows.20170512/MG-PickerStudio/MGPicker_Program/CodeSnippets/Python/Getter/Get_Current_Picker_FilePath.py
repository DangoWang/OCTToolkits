#get the full path of current picker file/node.
import maya.mel as mel
pickerFileOrNode = mel.eval('MGP_GetCurrentPickerFileOrNode')