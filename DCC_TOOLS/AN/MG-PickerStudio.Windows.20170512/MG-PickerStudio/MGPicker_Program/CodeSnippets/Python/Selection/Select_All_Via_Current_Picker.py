#Select all selectButton & slider members of current picker. 
#The int arg stands for the selection mode, 0 for replace selection,1 for add selection, 2 for remove selection, 3 for invert selection.
import maya.mel as mel
mel.eval('MGP_EvalPickerAllSelectButtons 0')