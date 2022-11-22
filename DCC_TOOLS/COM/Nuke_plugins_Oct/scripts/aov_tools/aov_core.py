#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Mon Dec 30 10:09:17 2019
#========================================
import os
import nuke
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_layer_data(node):
    '''
    '''
    channels = [c.split('.')[0] for c in node.channels()]
    layers   = sorted(dict.fromkeys(channels).keys())

    layer_data = dict()
    for lay in layers:
        layer_data.setdefault(lay.split('_')[-1], list()).append(lay)

    return layer_data




def create_aov_network(read_node, aov_keys, aov_data, position=1):
    '''
    '''
    if not read_node:
        return False

    #-
    read_dot = nuke.nodes.Dot()
    read_dot.setXpos(read_node.xpos() + read_node.screenWidth() / 2 - read_dot.screenWidth() / 2 )
    read_dot.setYpos(read_node.ypos() + read_node.screenHeight() * 3)
    read_dot.setInput(0, read_node)  
    read_dot['label'].setValue(os.path.basename(read_node['file'].value()))

    #-
    read_remove = nuke.nodes.Remove()
    read_remove.setXpos(read_dot.xpos() + read_dot.screenWidth() / 2 - read_remove.screenWidth() / 2 )
    read_remove.setYpos(read_dot.ypos() + read_remove.screenHeight() * 5)    
    read_remove['operation'].setValue('keep')
    read_remove['channels'].setValue('rgba')
    read_remove.setInput(0, read_dot)

    #-
    read_merge = nuke.nodes.Merge2()
    read_merge.setXpos(read_remove.xpos())
    read_merge.setYpos(read_remove.ypos() + read_remove.screenHeight() * 40)
    read_merge['operation'].setValue('copy')
    read_merge['also_merge'].setValue('all')
    read_merge.setInput(0, read_remove)

    #-
    read_premult = nuke.nodes.Premult()
    read_premult.setXpos(read_remove.xpos())
    read_premult.setYpos(read_remove.ypos() + read_remove.screenHeight() * 45)    
    read_premult.setInput(0, read_merge)


    #- create nodes
    aov_nodes = dict()
    for index, grp in enumerate(aov_keys):
        #-
        dot = nuke.nodes.Dot()
        aov_nodes.setdefault(grp, dict())['dot'] = dot

        #-
        aov_nodes.setdefault(grp, dict())['sf_out'] = [nuke.nodes.Shuffle() for i in range(len(aov_data[grp]))]

        #-
        if len(aov_nodes[grp]['sf_out']) > 1:
            aov_nodes.setdefault(grp, dict())['merge'] = nuke.nodes.Merge2()
        else:
            aov_nodes.setdefault(grp, dict())['merge'] = None

        #-
        aov_nodes.setdefault(grp, dict())['unpremult']  = nuke.nodes.Unpremult()

        #-
        aov_nodes.setdefault(grp, dict())['sf_in']  = nuke.nodes.Shuffle()

        #-        
        aov_nodes.setdefault(grp, dict())['premult'] = nuke.nodes.Premult()

        #-
        if index == len(aov_keys)-1:
            aov_nodes.setdefault(grp, dict())['merge_out'] = nuke.nodes.Remove()
        else:
            aov_nodes.setdefault(grp, dict())['merge_out'] = nuke.nodes.Merge2()



    #- set node attributes
    for index, grp in enumerate(aov_keys):
        nodes = aov_nodes[grp]

        #-
        nodes['dot']['label'].setValue(grp)
        nodes['dot']['note_font_size'].setValue(30)
        nodes['dot']['note_font_color'].setValue(0xff0000ff)

        #-
        for i, sf_out in enumerate(nodes['sf_out']):
            sf_out.setInput(0, nodes['dot'])
            sf_out['label'].setValue('[value in] -> [value out]')
            sf_out['in'].setValue(aov_data[grp][i])
            sf_out['out'].setValue('rgb')

        #-
        if nodes['merge'] != None:
            for i, sf_out in enumerate(nodes['sf_out']):
                if i > 1:
                    i += 1                
                nodes['merge'].setInput(i, sf_out)
            nodes['merge']['operation'].setValue('plus')
            nodes['merge']['Achannels'].setValue('rgb')
            nodes['merge']['Bchannels'].setValue('rgb')
            nodes['merge']['output'].setValue('rgb')

        #-
        if nodes['merge'] != None:
            nodes['unpremult'].setInput(0, nodes['merge'])
        else:
            nodes['unpremult'].setInput(0, nodes['sf_out'][0])

        #-
        lay = aov_data[grp][0].split('_')[-1]
        if not lay in nuke.layers():
            nuke.Layer(lay, ['{0}.red'.format(lay), '{0}.green'.format(lay), '{0}.blue'.format(lay), '{0}.alpha'.format(lay)])

        nodes['sf_in'].setInput(0, nodes['unpremult'])
        nodes['sf_in']['label'].setValue('[value in] -> [value out]')
        nodes['sf_in']['in'].setValue('rgb')
        nodes['sf_in']['out'].setValue(aov_data[grp][0].split('_')[-1])

        #-
        nodes['premult']['channels'].setValue(grp)
        nodes['premult'].setInput(0, nodes['sf_in'])

        #-
        if index == len(aov_keys)-1:
            nodes['merge_out']['operation'].setValue('keep')
            nodes['merge_out']['channels'].setValue('rgba')
            nodes['merge_out']['channels2'].setValue('{0}.red {0}.green {0}.blue rgba.alpha'.format(grp))
            nodes['merge_out'].setInput(0, nodes['premult'])
        else:
            nodes['merge_out'].setInput(1, nodes['premult'])
            nodes['merge_out']['operation'].setValue('plus')
            nodes['merge_out']['Achannels'].setValue('rgb')
            nodes['merge_out']['Bchannels'].setValue('rgb')
            nodes['merge_out']['output'].setValue('rgb')            
            nodes['merge_out']['also_merge'].setValue(aov_data[grp][0].split('_')[-1])


    #- set node connect
    dot_nodes = [aov_nodes[key]['dot'] for key in aov_keys]
    for i, dot in enumerate(dot_nodes):
        if i == 0:
            dot.setInput(0, read_dot)
        else:
            dot.setInput(0, dot_nodes[i-1])


    merge_out_nodes = [aov_nodes[key]['merge_out'] for key in aov_keys]
    for i in range(len(merge_out_nodes)-1):
        merge_out_nodes[i].setInput(0, merge_out_nodes[i+1])

    read_merge.setInput(1, merge_out_nodes[0])

    #-
    offset = 0
    for index, grp in enumerate(aov_keys):
        nodes = aov_nodes[grp]

        #-
        nodes['dot'].setXpos(read_dot.xpos() + offset)
        nodes['dot'].setYpos(read_dot.ypos())

        #-
        for i, sf_out in enumerate(nodes['sf_out']):
            sf_out.setXpos(read_remove.screenWidth()*2 + nodes['dot'].xpos() + sf_out.screenWidth()*i + i*5)
            sf_out.setYpos(read_remove.ypos())

        x_pos = nodes['sf_out'][0].xpos() + (nodes['sf_out'][-1].xpos() + nodes['sf_out'][-1].screenWidth() - nodes['sf_out'][0].xpos()) / 2
        nodes['dot'].setXpos(x_pos)

        #-
        if nodes['merge'] != None:
            nodes['merge'].setXpos(x_pos - nodes['merge'].screenWidth() / 2)
            nodes['merge'].setYpos(nodes['sf_out'][0].ypos() + nodes['sf_out'][0].screenHeight() * 3)

        #- 
        nodes['unpremult'].setXpos(x_pos - nodes['unpremult'].screenWidth() / 2)
        nodes['unpremult'].setYpos(nodes['sf_out'][0].ypos() + nodes['sf_out'][0].screenHeight() * 6)


        #- 
        nodes['sf_in'].setXpos(x_pos - nodes['sf_in'].screenWidth() / 2)
        nodes['sf_in'].setYpos(nodes['sf_out'][0].ypos() + nodes['sf_out'][0].screenHeight() * 35)

        #- 
        nodes['premult'].setXpos(x_pos - nodes['premult'].screenWidth() / 2)
        nodes['premult'].setYpos(nodes['sf_out'][0].ypos() + nodes['sf_out'][0].screenHeight() * 38)

        #- 
        nodes['merge_out'].setXpos(x_pos - nodes['merge_out'].screenWidth() / 2)
        nodes['merge_out'].setYpos(read_merge.ypos())

        offset += (nodes['sf_out'][-1].xpos() - nodes['sf_out'][0].xpos() + nodes['sf_out'][0].screenWidth()*3)


    if position == 0:
        for nodes in aov_nodes.values():
            nodes['dot'].setXpos(read_dot.xpos() - (nodes['dot'].xpos() - read_dot.xpos()) - nodes['dot'].screenWidth())

            #-
            for sf_out in nodes['sf_out']:
                sf_out.setXpos(read_dot.xpos() - (sf_out.xpos() - read_dot.xpos()) - sf_out.screenWidth())

            #-
            if nodes['merge'] != None:
                nodes['merge'].setXpos(read_dot.xpos() - (nodes['merge'].xpos() - read_dot.xpos()) - nodes['merge'].screenWidth())

            #-
            nodes['unpremult'].setXpos(read_dot.xpos() - (nodes['unpremult'].xpos() - read_dot.xpos()) - nodes['unpremult'].screenWidth())

            #-
            nodes['sf_in'].setXpos(read_dot.xpos() - (nodes['sf_in'].xpos() - read_dot.xpos()) - nodes['sf_in'].screenWidth())

            #-
            nodes['premult'].setXpos(read_dot.xpos() - (nodes['premult'].xpos() - read_dot.xpos()) - nodes['premult'].screenWidth())

            #-
            nodes['merge_out'].setXpos(read_dot.xpos() - (nodes['merge_out'].xpos() - read_dot.xpos()) - nodes['merge_out'].screenWidth())
