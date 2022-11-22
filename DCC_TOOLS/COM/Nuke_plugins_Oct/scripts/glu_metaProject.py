import nuke
import os, re
import string
import nukescripts


class MetaProject( nukescripts.PythonPanel):

    def __init__( self ):
        nukescripts.PythonPanel.__init__( self, 'MetaProject', 'com.ohufx.SearchReplace')
    # Docum
        #self.dokumum_file = 'C:/Users/zufarov/.nuke/script/projects_list.txt' 
        self.dokumum_file = os.getenv( 'NUKE_PATH' ).replace( '\\', '/' ) + '/scripts/glu_metaProject.txt'
        self.dokum = open( self.dokumum_file, 'r' ).readlines()
                #'Mult_3=\\\\gamma\\RenderOUT\\Zvezdnie_Golovy\\Episodes_3_sezon\n', 'Dozor_1=\\\\gamma\\RenderOUT\\Dozor\\Noviy_Dozor\\Series\\Series001\n',...

        self.project_file = {}
        self.project_key=[]
        for i in self.dokum:
            self.k = i.strip().replace( '\\', '/' ).split( ' = ' ) # udalenie '\n' . zamena '\\' na '/' . droblenie v '=' 
                                                        # ['Mult_3' , '\\\\gamma\\RenderOUT\\Zvezdnie_Golovy\\Episodes_3_sezon',..]
            self.project_file[ self.k[0] ] = self.k[1].lower()     # {'Mult_3' : '\\\\gamma\\RenderOUT\\Zvezdnie_Golovy\\Episodes_3_sezon',..}
            self.project_key.append( self.k[0] )           # ['Mult_3',....]


        self.Episode_choice = nuke.Enumeration_Knob('Episode choice','Episode choice' , self.project_key  )
        self.Nomer_EP = nuke.Int_Knob('Number_EP','Number_EP')
        self.Scene = nuke.Enumeration_Knob( 'Scene','Scene',['P00_Ep00_Sc0000'] )
        self.Scipts = nuke.Enumeration_Knob('Scipts','Scipts', ['P00_Ep00_Sc0000______________'] )
        self.Open_Sc = nuke.PyScript_Knob('Open Script', 'Open Script')
        self.Op_Folder = nuke.PyScript_Knob('Open Folder', 'Open Folder')
        self.Op_Shot_Folder = nuke.PyScript_Knob('Op Shot Folder', 'Op Shot Folder')
        self.Sc_shot = nuke.Text_Knob('')
        self.Op_Shot = nuke.PyScript_Knob('Open Shot', 'Open Shot')
        #self.addKnob(nuke.Tab_Knob('Scipts)'))

        self.addKnob(self.Episode_choice)
        self.addKnob(self.Nomer_EP)
        self.addKnob(self.Scene)
        self.addKnob(self.Scipts)
        #________
        self.addKnob(nuke.Text_Knob(''))
        self.addKnob(self.Open_Sc)
        self.addKnob(self.Op_Folder)
        #________
        self.addKnob(self.Sc_shot)
        self.addKnob(self.Op_Shot)
        self.addKnob(self.Op_Shot_Folder)
        #________
        self.addKnob(nuke.Text_Knob(''))
        #self.addKnob(nuke.Tab_Knob('source'))
        
#        self.source = nuke.PyScript_Knob('show_source','show_source' , 'import t_work \nt_work.ModalFramePanel().showModalDialog_()')
#        self.addKnob(self.source)

        

#        self.Scipts_list()
    def knobChanged(self,knob):
        if nuke.thisKnob().name() == "Scene":
            self.Scipts_list()
            self.Show_shot()

        if nuke.thisKnob().name() == "Number_EP":
            print 'ooooooooooo'
            self.Sc_list()
            self.Scipts_list()
            self.Show_shot()

        if nuke.thisKnob().name() == "Scipts":
            self.Show_shot()

        if nuke.thisKnob().name() == "Open Script":
            self.Open_Script()
            #print self.project_file[ self.Episode_choice.value() ] +'/'+ self.Scipts.value()
            #self.k = open('C:/BSII/projects_n.txt',w)

        if nuke.thisKnob().name() == "Open Folder":
            self.Folt_file = self.project_file[ self.Episode_choice.value() ] + '/' + self.Scene.value() + '/comp/_nk' 
            os.startfile(self.Folt_file.replace('/','\\'))

        if nuke.thisKnob().name() == "Op Shot Folder":
            os.startfile(self.Show_shot()[0].replace('/','\\'))

        if nuke.thisKnob().name() == "Open Shot":
            os.startfile(self.Show_shot()[2].replace('/','\\'))

#        if nuke.thisKnob().name() == "show_source":
#            self.Source()
            



    def Sc_list(self):
        
        self.Ep = str( string.zfill(self.Nomer_EP.value(),2) )
        self.XXX = os.listdir( self.project_file[ self.Episode_choice.value() ] )
        print  self.project_file[ self.Episode_choice.value() ] 
        self.a=[]
        for i in self.XXX:
            try:
                if i.split( '_' )[1][2:] == str(self.Ep) :
                    self.a.append(i)
            except : self.s=1
        
        self.a.sort()
        print self.a
        self.Scene.setValues(self.a )
        
        return self.a 


    def Scipts_list(self):
        
        self.SSS = os.listdir( self.project_file[ self.Episode_choice.value() ] + '/' + self.Scene.value() + '/comp/_nk' )
        self.list = filter(lambda i: i.endswith('.nk'),self.SSS)
        self.list.sort()

        self.numVers=[]
        for l in self.list:
            try:
                self.numVers.append( int(l.split('.')[0][-3:] ))
            except : q=1
            q=1
        self.numVers.sort()
        self.maxNumVers = self.numVers[-1]
        self.maxVers = self.Scene.value()+'_comp_v' + string.zfill( int(self.maxNumVers),3 ) +'.nk'
        self.Scipts.setValues(self.list )
        self.num = 0 

        for i in self.Scipts.values():
            if i == self.maxVers:
                self.Scipts.setValue(self.num)
            self.num = self.num + 1

        return
        
    
    def Show_shot(self):
        try:
            self.Shot_foder = self.project_file[ self.Episode_choice.value() ] + '/' + self.Scene.value() + '/comp/' + self.Scipts.value().split('.')[0][-4:]
            self.Shot = os.listdir(self.Shot_foder)
            self.Shot_file = self.Shot_foder +'/'+ self.Shot[0]
            print self.Shot_file
            self.Sc_shot.setValue('<img src='+ self.Shot_file +' width="400" height="230" />')
        except :
            self.Sc_shot.setValue('<img src="X:/SAVVA/data/images/images.jpg" width="400" height="230" />')
        return self.Shot_foder, self.Shot, self.Shot_file
        #os.startfile(self.WWW.replace('/','\\'))

    
    def Open_Script(self):
        return nuke.scriptOpen( self.project_file[ self.Episode_choice.value() ] +'/'+self.Scene.value() + '/comp/_nk/' +  self.Scipts.value() )


    def this_script(self):
        os.path.split( nuke.scriptName() )[1]


    




def addPanel_MP():
    return MetaProject().addToPane()
menu = nuke.menu('Pane')
menu.addCommand('MetaProject', addPanel_MP)
nukescripts.registerPanel('com.ohufx.SearchReplace', addPanel_MP)



#    def this_script(self): 
#        try:
#            self.Sc_name = os.path.splitext(os.path.basename(nuke.scriptName()))[0].split('_')
#            print 'no_eror'
#        except : return
#        self.ep = int( self.Sc_name[1][2:] )
#        self.Nomer_EP.setValue(self.ep)
#        for i in range( len( self.Sc_list() ) ):
#            print i
#        return











