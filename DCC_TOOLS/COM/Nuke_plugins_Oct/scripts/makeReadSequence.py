import nuke
import nukescripts
import os
import os.path
from datetime import date

class ShapePanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self,"Append sequence's")
        self.overlap = nuke.String_Knob('overlapping', 'Overlapping','2')
        self.addKnob(self.overlap)

p = ShapePanel()

#this function return Readers
def nodes():
 selAll = []
 sel = nuke.selectedNodes()
 pref = nuke.toNode('preferences')
 pref["maxPanels"].setValue(len(sel)+1)
 if sel == []:
  sel = nuke.allNodes()
 for i, s in enumerate(sel):
  if s.Class() == "Read":
   s.showControlPanel()
   selAll.append(sel[i])
 return selAll  
 
#create folder for rendering
def pathToRender():
 now = str(date.today())
 name = now[2:].replace('-','')
 path = 'x:\\SAVVA\\_dailies\\{0}'.format(name)
 path2 = path + '\\Montage'
 if os.path.isdir(path)==False:
  os.mkdir(path)
 if os.path.isdir(path)==True:
  if os.path.isdir(path2)==False:
   os.mkdir(path2)
#set writer
 filepath = 'x:/SAVVA/_dailies/{0}{1}'.format(name,'/Montage/Ep_.####.jpg')
 Node = nuke.toNode( 'kolbasa' )
 Node['file'].setValue(filepath)
 Node['file_type'].setValue('jpeg') 

#select all readers in order to see it in DopeSheet 
def selectReader():
 list = []
 list = nuke.allNodes()
 for i in list:
  if i.Class() == 'Read':
    name = i.name()
    node = nuke.toNode(name) 
    node.knob("selected").setValue(True)

#create sequence 
def makeReadSequence():
#show menu
 if p.showModalDialog():
  nuke.restoreWindowLayout(6)
#get user data
  overlap = int(p.overlap.value())

#set attributes for selected Read"ers
  selAll = nodes()
# merge all readers 
  mergeAll = nuke.createNode("Merge2")
  mergeAll.hideControlPanel()
  nuke.nodes.Write(name="kolbasa").setInput(0, mergeAll)
 
  for all in selAll:
    all['before'].setValue('black')
    all['after'].setValue('black')
    all['frame_mode'].setValue('offset')
    LastFrame = all['origlast'].value()#take origin last frame of each reader
    all['last'].setValue(LastFrame-overlap)#set last frame of each reader to(origin minus user overlap)

  lastFrame = []
  count = len(selAll)
  list1,list2,list3,list4,names = [],[],[],[],[]
  for i, sel in enumerate(selAll):
   list1.insert(i,selAll[i]['file'].value())# path to files
   list2.insert(i,sel.name())# name of node ex. read1, read2...
   list3.insert(i,list1[i]+"::"+list2[i])# concatenation path with name 
  list3.sort()# sorting path(for normal sort of names)

  for i in range(len(list3)):
   list4.insert(i,list3[i].split('::'))# separate path and name
   names.insert(i,list4[i][1])#take only sorted names
 
  for x in range(count):
   my = nuke.toNode(names[x])
   lastFrame.insert(x,my['last'].value())#list of last frame of readers
 
  for x in range(count):
   global offset
   my = nuke.toNode(names[x])
   if my.name() == names[0]:#for first reader - dont need offset
     my['frame'].setValue(str(0))#for first reader - dont need offset
   else:
    offset = offset + lastFrame[x-1]
#if frame range not equal to 1
    if my['first'].value() > 1:
     firstFrame = my['first'].value()
     offset -= firstFrame - 1
    my['frame'].setValue(str(-offset))# set offset for each reader
 #set project last frame
  nuke.toNode( 'root' ).knob( 'last_frame' ).setValue(offset+lastFrame[count-1])
  offset = 0
  pathToRender()
  selectReader()
offset = 0

#reset all readers into default
def reset():
 selAll = nodes()
 for x in selAll:
  x['frame'].setValue('')
  x['after'].setValue('hold')
  x['before'].setValue('hold')
  LastFrame = x['origlast'].value()
  x['last'].setValue(LastFrame)
  x['frame_mode'].setValue('expression')











  













 