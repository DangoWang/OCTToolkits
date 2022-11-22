#Reactivate the model view, so animators could have access to the hotkeys features of Maya, such as set keys,etc.
#but ususually you don't need to do so, cos MG-Picker in animator interactive mode does so automatically after each mouse left mouse button clicking.
import maya.mel as mel
mel.eval('MGP_ReactiveModelViewport')