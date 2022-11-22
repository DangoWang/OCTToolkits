import nukescripts
import nuke

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
    hitList = getHITsList(nuke.selectedNode())
    hitListStr=''
    for hit in hitList:
        hitListStr=hitListStr+hit+' '
# ------------------------- UI part
    selectHIT_ui = nuke.Panel('WAALLAPPAA!')
    selectHIT_ui.addEnumerationPulldown('available HIT data: ', hitListStr)
    selectHIT_ui.show()
    selectHIT_ui.value('available HIT data: ')
# -------------------------- end UI part
    selectedHIT = selectHIT_ui.value('available HIT data: ')
    if 'left' and 'right' in nuke.views():
        hit_T=nuke.createNode('Transform')
        hit_T.setName('s3d_HIT_transform')

        hit_T['translate'].splitView('right')
        hit_T['translate'].setExpression("-[metadata {0}]/2".format(selectedHIT),0)
        hit_T['translate'].setExpression("[metadata {0}]/2".format(selectedHIT),0,view = 'right')
    else:
        nuke.message('ERRORrrrTrrtrrrrr!! : there is no Left and Right views in nuke.views()')




# to use tha info in transform.. : nuke.thisNode().metadata()['key']
# to use tha info in transform.. : [metadata C_HIT]