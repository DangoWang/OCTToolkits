'''
add HIT data to Metadata stream

'''

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


# to use tha info in transform.. : nuke.thisNode().metadata()['key']
# to use tha info in transform.. : [metadata C_HIT]