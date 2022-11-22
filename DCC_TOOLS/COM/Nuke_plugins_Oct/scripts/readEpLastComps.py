import nuke
import os.path
import nukescripts
import threading
import time
import glob

#create menu
class ShapePanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self,"Read Episodes")
        self.chanel = nuke.Enumeration_Knob('chanel', 'Chanel', ['l', 'r','stereo'])
        self.episod = nuke.String_Knob('episod', 'Episode','46')
        for k in (self.episod, self.chanel):
            self.addKnob(k)

p = ShapePanel()

def readEpLastComps(): 
#show menu
 if p.showModalDialog():
  
#get user data
  episod = p.episod.value()
  chan = p.chanel.value()
  task = nuke.ProgressTask("")                  #UI user interface

  if chan == 'stereo':
   chan = '%v'
   nukescripts.stereo.setViewsForStereo()       #set stereo scene for nuke
  
  dir = "X:/SAVVA/result/Feature"
  dirnames,dirnames2,var_list,last,list,list2=[],[],[],[],[],[]
  dirnames = os.listdir(dir)            #all directories
  
#counter of scenes of selected episode
  for i,sel in enumerate(dirnames):
   split = dirnames[i].split('_')
   if split[0] == 'P01' and split[1] == 'Ep'+str(episod):
     dirnames2.append(dirnames[i])
  newList = sorted(dirnames2)
  
  for i,sel in enumerate(newList):
   path1 = "X:/SAVVA/result/Feature/"+sel+"/comp"
   task.setMessage("Reading files: "+ str(path1)) 		#UI
   task.setProgress(i)									#UI
   if os.path.isdir(path1)==False:
    nuke.message(dir2 + ' ....PATH ISN`T EXIST')   
   Ep = sel
   dirnames2 = os.listdir(path1)
   var_list = sorted([sel for i,sel in enumerate(dirnames2) if sel[:2] == "v0"])
   last = var_list[len(var_list)-1]
   path2 = path1 +"/"+ last +"/"+Ep+"_comp_"+last+"_"+str(chan)+".####.jpg"
   path3 = path1 +"/"+ last +"/"
   num_files = glob.glob(path3 + '*.jpg')
   if num_files:
    for i,sel in enumerate(num_files):
     list.insert(i,num_files[i][-10:])
     if list[i][:1] == "l":
      list2.append(list[i][2:6]) 
    list2.sort()
#create reader
    node_name = nuke.nodes.Read(file=path2)
#get first and last frame   
    
    node_name['first'].setValue(int(list2[0]))
    node_name['last'].setValue(int(list2[-1]))
    list2=[]







