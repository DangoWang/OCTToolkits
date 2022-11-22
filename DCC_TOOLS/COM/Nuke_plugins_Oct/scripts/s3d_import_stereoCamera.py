'''
last edit:
27.01.2011, robocop

type: tool script
This Tool script for assigning animation of stereo camera parameters from special file (*.s3d) with all stereosettings. This file generated from AutodeskMaya
'''



'''
FLength
AoV
Stereo.Method='Parallel'
ResolutionGateFit = 'Height'\'Width'
Stereo.EyeSeparation
Stereo.ConvergenceDistance
ApertureW
ApertureH
Transform3DOp.Translate.X
Transform3DOp.Translate.Y
Transform3DOp.Translate.Z
Transform3DOp.Rotate.X
Transform3DOp.Rotate.Y
Transform3DOp.Rotate.Z
'''

'''
ToDo:
add checking that current comp has 'left' and 'right' views, if not - error window popup
add checking if current comp frame-range is different than framerange in metadata
'''

import pprint, pickle
import nukescripts
import nuke
import os.path

def s3d_import_stereoCamera():
    def applyCamTransforms(cam,S3D_settings):
        cam['xform_order'].setValue('SRT')
        cam['rot_order'].setValue('XYZ')
        cam['useMatrix'].setValue(0)
        for cur_view in nuke.views():
            cam['translate'].clearAnimated(view=cur_view)
            cam['rotate'].clearAnimated(view=cur_view)
            cam['translate'].unsplitView(cur_view)
        cam['translate'].splitView('right')
        cam['rotate'].splitView('right')
        for cur_view in nuke.views():
            cam['translate'].setAnimated(view=cur_view)
            cam['rotate'].setAnimated(view=cur_view)
        for frame,value in S3D_settings['camL_TranslateX'].items():
            cam['translate'].setValueAt(value,frame,0,view = 'left')
            cam['translate'].setValueAt(S3D_settings['camR_TranslateX'][frame],frame,0,view = 'right')
        for frame,value in S3D_settings['camL_TranslateY'].items():
            cam['translate'].setValueAt(value,frame,1,view='left')
            cam['translate'].setValueAt(S3D_settings['camR_TranslateY'][frame],frame,1,view = 'right')
        for frame,value in S3D_settings['camL_TranslateZ'].items():
            cam['translate'].setValueAt(value,frame,2,view='left')
            cam['translate'].setValueAt(S3D_settings['camR_TranslateZ'][frame],frame,2,view = 'right')
        
        for frame,value in S3D_settings['camL_RotateX'].items():
            cam['rotate'].setValueAt(value,frame,0,view = 'left')
            cam['rotate'].setValueAt(S3D_settings['camR_RotateX'][frame],frame,0,view = 'right')
        for frame,value in S3D_settings['camL_RotateY'].items():
            cam['rotate'].setValueAt(value,frame,1,view = 'left')
            cam['rotate'].setValueAt(S3D_settings['camR_RotateY'][frame],frame,1,view = 'right')
        for frame,value in S3D_settings['camL_RotateZ'].items():
            cam['rotate'].setValueAt(value,frame,2,view = 'left')
            cam['rotate'].setValueAt(S3D_settings['camR_RotateZ'][frame],frame,2,view = 'right')
    
    def applyCamMatrix(cam,left_matrixdata,right_matrixdata):
        cam['useMatrix'].setValue(1)
        for cur_view in nuke.views():
            cam['matrix'].clearAnimated(view=cur_view)
            cam['matrix'].unsplitView(cur_view)
        cam['matrix'].splitView('right')
        for cur_view in nuke.views():            
            cam['matrix'].setAnimated(view=cur_view)
        for Frame,value in left_matrixdata.items() :
            left_matrixValues = left_matrixdata[Frame]
            right_matrixValues = right_matrixdata[Frame]
            myMatrix_left = nuke.math.Matrix4()
            myMatrix_right = nuke.math.Matrix4()
            for index in range(len(left_matrixValues)):
                myMatrix_left[index] = left_matrixValues[index]
                myMatrix_right[index] = right_matrixValues[index]

            myMatrix_left.transpose()
            myMatrix_right.transpose()
            for index in range(16):
                left_value = myMatrix_left[index]
                right_value = myMatrix_right[index]
                cam['matrix'].setValueAt(left_value,Frame,index,view='left')
                cam['matrix'].setValueAt(right_value,Frame,index,view='right')

    def fromTo(inMayaAttr,inNuke):
        '''
            assign attribute from maya camera to appropriate Nuke camera attr.
        '''
        inMaya = S3D_settings[inMayaAttr]
        inNuke.clearAnimated()    #    remove already existing animation in case when it ixist.
        if len(inMaya)>1:        # if parameter has animation 
            inNuke.setAnimated(0)
            for Frame,value in inMaya.items():
                inNuke.setValueAt(value,Frame,0,view='left')    # i set default view to "left" becouse it works fine for all mono attributes and i need separate view for setup the "win_translate" attribute only for left view.
        else:                                # if parameter haven`t animation
            inNuke.setValue(list(inMaya.values())[0],0,view='left') 
                
    class ModalFramePanel( nukescripts.PythonPanel ):
        # Modal Dialog class
        def __init__( self,header,text ):
         nukescripts.PythonPanel.__init__( self, header, "uk.co.thefoundry.FramePanel" )
         #self.frame = nuke.Int_Knob( "frame", "Frame:" )
         self.text = nuke.Text_Knob('' )
         #self.addKnob( self.frame )
         self.addKnob( self.text )
         self.text.setValue( text )
        def showModalDialog( self ):
         result = nukescripts.PythonPanel.showModalDialog( self )  
    
    # check current scene for stereo views
    if not nuke.views() == ['left','right']: 
        ModalFramePanel('WARNING','No "left\right" stereo views found,\nplease setup default "stereo views" in composition global settings\n Script works only with "left" and "right" views names, not with "R" and "L" or\n something like that.').showModalDialog()
    else :
        camera=nuke.selectedNode()
        nukescriptDir = nuke.root().name()
        directory = ''
        if os.path.exists(nukescriptDir):             
            if os.path.exists(os.path.dirname(nukescriptDir).replace("comp/_nk",'data/')):
                directory = os.path.dirname(nukescriptDir).replace("comp/_nk",'data/')                
            else:
                directory = os.path.dirname(nukescriptDir)
        filePath = nuke.getFilename('Get File Contents', '*.s3d',directory)
        FILE = open(filePath, 'rb')
        S3D_settings = pickle.load(FILE)
        FILE.close()

        applyCamTransforms(camera,S3D_settings)

        '''turn off <limit plane> creation
        # Create plane that show stereo limits for nearest point.
        mycamPos = [camera.xpos() , camera.ypos()]
        mytransform = nuke.nodes.TransformGeo(xpos = mycamPos[0]+100, ypos = mycamPos[1]+20)
        myCard = nuke.nodes.Card(xpos = mycamPos[0]+100, ypos = mycamPos[1]-20, render_mode=0)
        myText = nuke.nodes.Text(xpos = mycamPos[0]+100, ypos = mycamPos[1]-40,message = 'STEREO LIMIT', xjustify=1, yjustify=2, invert=1,font = r'C:/Windows/Fonts/arial.ttf',size =200)

        mytransform.setInput(1,camera)
        mytransform.setInput(0,myCard)
        myCard.setInput(0,myText)
        myText['color'].setValue([0.9, 0.6, 1.0, 1.0])
        myText['box'].setValue(((camera.format().width(), 0.0, 0.0, camera.format().height())))
        '''

        #==== create custom knob with HIT animation, to assign it to metadata by frame basis then.
        interaxial_knob = nuke.Double_Knob("interaxial",'Interaxial')
        zeroParallax_knob = nuke.Double_Knob("zeroParallax",'Zero Parallax')
        safeNegativeParallaxLimit_knob = nuke.Double_Knob("safeNegativeParallaxLimit",'Safe NegativeParallax Limit (pixels)')
        safeNegativeParallaxDistance_knob = nuke.Double_Knob("safeNegativeParallaxDistance",'Safe Negative Parallax Distance')
        #interaxial_knob2 = nuke.Double_Knob("interaxial2",'Interaxial2')
        #zeroParallax_knob2 = nuke.Double_Knob("zeroParallax2",'Zero Parallax2')
        camera.addKnob(interaxial_knob)
        camera.addKnob(zeroParallax_knob)
        camera.addKnob(safeNegativeParallaxLimit_knob)
        camera.addKnob(safeNegativeParallaxDistance_knob)
        #camera.addKnob(interaxial_knob2)
        #camera.addKnob(zeroParallax_knob2)
        
        #applyCamMatrix(camera,S3D_settings['camL_Tmatrix'],S3D_settings['camR_Tmatrix'])
        fromTo('focalLength',camera['focal'])
        fromTo('horizontalFilmAperture',camera['haperture'])
        camera['haperture'].setValue(camera['haperture'].getValue()*25.4)
        fromTo('verticalFilmAperture',camera['vaperture'])
        camera['vaperture'].setValue(camera['vaperture'].getValue()*25.4)
        camera['safeNegativeParallaxLimit'].setValue(-45)
        #fromTo('interaxialSeparation',camera['interaxial2'])
        #fromTo('zeroParallax',camera['zeroParallax2'])        
        
        camera['interaxial'].setExpression('sqrt(pow(translate.left.x-translate.right.x,2)+pow(translate.left.y-translate.right.y,2)+pow(translate.left.z-translate.right.z,2))')
        camera['zeroParallax'].setExpression('win_translate==0?1:abs(interaxial*focal/(win_translate*haperture))')
        camera['safeNegativeParallaxDistance'].setExpression('1.0/(safeNegativeParallaxLimit*haperture/(width*focal*interaxial)-1.0/zeroParallax)')
        #myCard['z'].setExpression('-{camName}.safeNegativeParallaxDistance'.format(camName=camera.name()))
        
        #camera['pivot'].splitView('right')
        #camera['pivot'].setExpression('interaxial/2',0,view='left')   # set left camera pivot
        #camera['pivot'].setExpression('-interaxial/2',0,view='right')   # set left camera pivot
        #camera['translate'].splitView('right')
        
        #camera['translate'].setExpression('curve-interaxial/2',0,view='left')   # set left camera interaxial
        #camera['translate'].setExpression('curve+interaxial/2',0,view='right') # set right camera interaxial
        camera['win_translate'].splitView('right')
        fromTo('filmTranslateH',camera['win_translate'])
        #camera['win_translate'].setExpression('interaxial*focal/(zeroParallax*haperture)', 0,view='left')
        #camera['win_translate'].setExpression('-interaxial*focal/(zeroParallax*haperture)',0,view='right')
        camera['win_translate'].setExpression('-win_translate.left.u',0,view='right')

        
        ModalFramePanel('jogi-jogi','Import stereo camera: succesefull').showModalDialog()
