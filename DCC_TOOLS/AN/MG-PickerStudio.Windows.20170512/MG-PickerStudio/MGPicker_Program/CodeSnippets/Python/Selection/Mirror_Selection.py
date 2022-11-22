#Mirror selection & slider via current picker's mirror relationship.
import maya.mel as mel
mel.eval('MGP_MirrorSelection 0')  #arg: 0 for replace selection,1 for add selection.