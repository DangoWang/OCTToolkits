#Select all selectButton & slider members of the picker panel with the panel index. 
#The first int arg stands for the selection mode, 0 for replace selection,1 for add selection, 2 for remove selection, 3 for invert selection.
#The second int arg stands for the panel index. 
import maya.mel as mel
mel.eval('MGP_EvalPanelAllSelectButtons_viaPanelIndex 0 0') 