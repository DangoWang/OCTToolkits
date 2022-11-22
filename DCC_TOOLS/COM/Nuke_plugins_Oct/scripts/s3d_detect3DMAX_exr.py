import nuke

def s3d_inject_HIT_to_metadata():
    import pickle
    import os.path
    import nuke

    filePath = nuke.getFilename('Get File Contents', '*.s3d')
    print(filePath)

    s3dFILE = open(filePath, 'rb')
    S3D_settings = pickle.load(s3dFILE)
    s3dFILE.close()

    #print('loaded hit: '+str(S3D_settings['HIT']))
    print('loading HIT: ok')
    camName = os.path.basename(filePath).replace('_s3Data.s3d','')	# leave alone cameraname only


    modifyMeta = nuke.createNode('ModifyMetaData')

    #==== create custom knob with HIT animation, to assign it to metadata by frame basis then.
    hitknob = nuke.Double_Knob("hit_store",'HIT')
    modifyMeta.addKnob(hitknob)
    modifyMeta['hit_store'].setAnimated()
    for key,value in S3D_settings['HIT'].items():
        modifyMeta['hit_store'].setValueAt(value,key)
    #===

    newdata = '{set '+ camName +'_HIT "[value knob.hit_store]"}'
    modifyMeta["metadata"].fromScript(newdata)

def getHITsList(node):
    # return list with metadata keys that contain HIT data .
    mdat = node.metadata()
    hitList = []
    for key in mdat.keys() :
        if '_HIT' in key: hitList.append(key)
    return hitList

def s3d_apply_HIT():
    '''
    add HIT data to Metadata stream

    '''
    selectedHIT = getHITsList(nuke.selectedNode())[0]

    if 'left' and 'right' in nuke.views():
        hit_T=nuke.createNode('Transform')
        hit_T.setName('s3d_HIT_transform')

        hit_T['translate'].splitView('right')
        hit_T['translate'].setExpression("-[metadata {0}]".format(selectedHIT),0)
        hit_T['translate'].setExpression("[metadata {0}]".format(selectedHIT),0,view = 'right')
    else: nuke.message('ERRORrrrTrrtrrrrr!! : there is no Left and Right views in nuke.views()')

def detect3DMAX_exr():
    #this function is called "detect3DMAX_exr" because it start as 3dMax only.. but then the same techinque was spreaded to mantra exr's from houdini
    readNode=nuke.thisNode()
    knob = nuke.thisKnob()
    if readNode.Class()=='Read' and knob.name()=='file':
        filename = readNode['file'].value()
        # for detecting 3Dmax exr files we search "exr/cameraFarRange" key in exr metadata. Becouse 3Dmax always generate that field, but Maya not.
        if 'exr/cameraFarRange' in readNode.metadata().keys():
            '''
            ask = nuke.ask('3DMAX exr image detected.\n Do you want apply automatic stereoscopic correction for that sequence?')
            if ask ==1:
                s3d_inject_HIT_to_metadata()
                s3d_apply_HIT()
        elif 'exr/capDate' in readNode.metadata().keys(): 
                    ask = nuke.ask('Houdini exr image detected.\n Do you want apply automatic stereoscopic correction for that sequence?')
                    if ask ==1:
                        s3d_inject_HIT_to_metadata()
                        s3d_apply_HIT()
                        '''
    else: pass

nuke.addKnobChanged(detect3DMAX_exr, nodeClass='Read')

#nuke.removeKnobChanged(detect3DMAX_exr, nodeClass='Read')
