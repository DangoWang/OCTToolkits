import nuke

#
# starts here
#
def ProEXR():
    if len( nuke.selectedNodes() ) > 0:
        root_node = nuke.selectedNode()
    
        available_layers = nuke.layers(root_node)
    
        layers_string = root_node.metadata().get('exr/PSlayers', None)
    
        if layers_string is not None:
            layer_dict_array = parsePSlayers(layers_string)
            
            # Shuffle nodes get the channels out
            for i in range(0, len(layer_dict_array)):
                layer_dict = layer_dict_array[i]
                layer_name = getLayerName(layer_dict_array[i])
    
                # checking the layer names we have against Nuke's
                # no guarantee we'll get them all
                if layer_name in available_layers:
                    # new Shuffle node
                    shuffle_node = nuke.nodes.Shuffle(name = layer_dict['name'])
    
                    # silly thing we need for PLE (or else we hit the node access limit and get errors)
                    if nuke.env['ple']:
                        nuke.message('PLE says wait!')
    
                    shuffle_node.setXYpos(root_node.xpos() + (i * 100), root_node.ypos() + 150)
                    shuffle_node.setInput(0, root_node)
                    shuffle_node['in'].setValue( layer_name )
                    shuffle_node['postage_stamp'].setValue(True)
    
                    layer_dict['shuffle_node'] = shuffle_node
            
                    # Remove nodes 
                    remove_node = nuke.nodes.Remove()
                    
                    remove_node.setXYpos(shuffle_node.xpos(), shuffle_node.ypos() + 85)
                    remove_node.setInput(0, shuffle_node)
                    remove_node['operation'].setValue('keep')
                    remove_node['channels'].setValue('rgba')
                    
                    layer_dict['remove_node'] = remove_node
            
            # Merge nodes
            if len(layer_dict_array) >= 2:
                last_merge = layer_dict_array[0].get('remove_node', None)
        
                for i in range(1, len(layer_dict_array)):
                    layer_dict = layer_dict_array[i]
                    
                    # new Merge node
                    new_merge = nuke.nodes.Merge()
                    
                    # silly thing we need for PLE (or else we hit the node access limit and get errors)
                    if nuke.env['ple']:
                        nuke.message('PLE says wait!')
    
                    remove_node = layer_dict.get('remove_node', None)
                    
                    if last_merge is not None:
                        new_merge.setInput(0, last_merge)
    
                    if remove_node is not None:
                        new_merge.setInput(1, remove_node)
                        
                        new_merge.setXYpos(remove_node.xpos(), remove_node.ypos() + 100)                   
    
                    # set merge parameters based on Photoshop transfer modes, opacity, etc
                    if layer_dict['properties'].get('visible', 'true') == 'false':
                        new_merge['disable'].setValue(True)
    
                    new_merge['operation'].setValue( PhotoshopToNukeMode(layer_dict['properties'].get('mode', 'Normal') ) )
                    
                    # special case for Mult - in Photoshop, nothing with black alpha will get multed
                    if new_merge['operation'].value() == 'mult' and remove_node is not None:
                        new_merge.setInput(2, remove_node)
                    
    
                    opacity = int( layer_dict['properties'].get('opacity', '255') )
    
                    if opacity != 255:
                        new_merge['mix'].setValue( float(opacity) / 255.0 )
    
                    last_merge = new_merge
    
        else:
            # no PSlayers metadata, but we do have some channels, so we'll do our best
           # nuke.message('No ProEXR PSlayers data available, using channel data instead')
    
            shuffle_array = []
    
            for i in range(0, len(available_layers)):
                layer = available_layers[i]
    
                shuffle_node = nuke.nodes.Shuffle(name = layer)
    
                # silly thing we need for PLE (or else we hit the node access limit and get errors)
                if nuke.env['ple']:
                    nuke.message('PLE says wait!')
    
                shuffle_node.setXYpos(root_node.xpos() + (i * 100), root_node.ypos() + 150)
                shuffle_node.setInput(0, root_node)
                shuffle_node['in'].setValue( layer )
                shuffle_node['postage_stamp'].setValue(True)
                #shuffle_node['hide_input'].setValue(True)
    
                shuffle_array.append(shuffle_node)
    
            # decided merging doesn't really make sense if we don't know anything about the layers
            # un-comment if you disagree           
            #if len(shuffle_array) >= 2:
            #    last_merge = shuffle_array[0]
            #
            #    for i in range(1, len(shuffle_array)):
            #        new_merge = nuke.nodes.Merge()
            #
            #        # silly thing we need for PLE (or else we hit the node access limit and get errors)
            #        nuke.env['ple']:
            #            nuke.message('PLE says wait!')
            #
            #        new_merge.setInput(0, last_merge)
            #        new_merge.setInput(1, shuffle_array[i])
            #
            #        new_merge.setXYpos(shuffle_array[i].xpos(), shuffle_array[i].ypos() + (i * 50))
            #
            #        last_merge = new_merge
                



if __name__ == "__main__":
    ProEXR()
    