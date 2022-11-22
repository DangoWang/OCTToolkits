#!/usr/bin/env python
# -*- coding:utf-8 -*-

#---------------------------------------------------------------
#
#        OCT Abc Cache v1.0 
#        BY WangHaoRun
#        2019.03.06
#
#---------------------------------------------------------------

import os
import json
import searchDB
reload(searchDB)
from maya import mel
from maya import cmds
from maya import utils


def get_top_hierarchy(obj):
    parent = cmds.listRelatives(obj, p=1)
    if parent:
        return get_top_hierarchy(parent[0])
    return obj


class AbcCache:
    version = "V1.00beta By WangHaoRun"
    def __init__(self, *args, **kwargs):
        pass

    def project(self):
        return ["", "dsf"]

    def copyUV(self, s_ns, t_ns, node):
        l_node = []
        s_objs = cmds.listRelatives(node, ad=True, pa=True, typ="mesh")
        print s_objs
        err = ""
        for s_o in s_objs:
            if cmds.objectType( s_o ) == "mesh":
                print "s:", s_o
                t_o = s_o.replace(s_ns+":", t_ns+":")
                print "t:", t_o
                if cmds.objExists(t_o):
                    if cmds.objectType( s_o ) == "mesh":
                        l_node.append(cmds.polyTransfer(t_o, uv=1, ao=s_o))
                    else:
                        err = err + "// Object Type Error: "+t_o +"; //\n" 
                else:
                    err = err + "// No object exists: "+t_o +"; //\n"
        return l_node, err
#l_node, err = copyUV("dsf_HX_DanX_TEX", "", "|dsf_HX_DanX_TEX:HX_DanX_Grp|dsf_HX_DanX_TEX:Geometry|dsf_HX_DanX_TEX:high")

    def savepath(self, project):
        return "Z:/DS/Library/TD/Cache/"+project

    def outputAbc(self, cmd):
        print cmd
        mel.eval(cmd)
        pass

    def outputAbcAll(self, l_cmd):
        print "\n"
        print "// Output Abc Cache: //"
        print "// Start... //"
        for cmd in l_cmd:
            utils.executeInMainThreadWithResult( self.outputAbc, cmd )
        print "// Final. //"
        print "\n"
        pass

    def loadSetup(self, path, all = 0):
        print "\n"
        print "// Loading setup file: //"

        l_cmd = []
        with open(path, 'r') as json_file:
            load_dict = json.load(json_file)
            project = load_dict["project"]
            now = searchDB.taskInfo(project).now()
            s = load_dict["start"]
            e = load_dict["end"]
            scenename = load_dict["scenename"]
            version = load_dict["version"]
            d_typ = load_dict["typ"]
            cmd1 = 'AbcExport -verbose -j "-frameRange '+str(s)+' '+str(e)+' -ro -stripNamespaces -worldSpace -writeVisibility -dataFormat ogawa'
            for typ in d_typ.keys():
                # typ : CAM
                if typ in ['CAM']:
                    dir = d_typ[typ].rstrip(d_typ[typ].split('/')[-1])
                    if not os.path.isdir(dir):
                        os.mkdir(dir)
                    l_cmd.append(cmd1+' -root |CAM -file ' + d_typ[typ] + '"')
                    pass
                else:
                    # if typ in ['ENV']:
                        # cmd1 = 'AbcExport -verbose -j "-frameRange ' + str(s) + ' ' + str(
                        #     s) + ' -ro -stripNamespaces -worldSpace -writeVisibility -dataFormat ogawa'
                    for ref in d_typ[typ]:
                        group = ref["group"]
                        name = ref["name"]
                        namespace = ref["namespace"]
                        objects = ref["objects"]
                        version = ref["version"]
                        output = ref["output"]
                        isuv = ref["isuv"]
                        isout = ref["isout"]
                        name_en = ref["name_en"]
                        cmd2 = ''
                        cmd3 = ' -file '+output.replace("{datetime}", now)+'";'
                        if isout > 0 or all != 0:
                            for obj in objects.keys():
                                cmd2 = cmd2 + " -root " + obj
                            if cmd2 != '':
                                print "// Asset Name: "+name+" //"
                                print "// Group: "+group+" //"
                                print "// Namespace: "+namespace+" //"
                                print "// Version: "+str(version)+" //"
                                if not os.path.exists(os.path.dirname(output)):
                                    os.makedirs(os.path.dirname(output))
                                    if os.path.exists(os.path.dirname(output)):
                                        print "// Path to create success. //"
                                    else:
                                        print "// Create failure path. //"
                                print "// Abc Path: "+output+" //"
                                #print(cmd1 + cmd2 + cmd3)
                                cmd_str = cmd1 + cmd2 + cmd3
                                if typ in ['ENV']:
                                    cmd_str = 'print \"ENV found, skipped...\"'
                                l_cmd.append(cmd_str)

                                print "\n"
            return l_cmd

    def inputAbc(self, abc, ct=None, eft=None, namespace=None, bs=False):
        if not bs:
            cmd = 'AbcImport -mode import -ct \"{0}\" -eft \"{1}\" \"{2}\"'.format(ct, eft, abc)
            print cmd
            mel.eval(cmd)
            return
        cmd = 'AbcImport -mode import  \"{0}\"'.format(abc)
        abc_node = mel.eval(cmd)
        if namespace:
            high_grp = cmds.ls('|high')[0]
            cache_name = namespace + '_cache'
            cmds.group(high_grp, name=cache_name)
            if not cmds.objExists('|Cache'):
                cmds.group(cache_name, name='|Cache')
                cmds.setAttr('|Cache.v', 0)
            else:
                cmds.parent(cache_name, '|Cache')
                cmds.setAttr('|Cache.v', 0)
            aa = cmds.blendShape('|Cache|%s|high' % cache_name, ct, at=1)[0]
            cmds.setAttr(aa+'.high', 1)
        print cmd
        return

    def inputAbcAll(self, l_data):
        print "\n"
        print "// Input Abc Cache: //"
        for data in l_data:
            utils.executeInMainThreadWithResult( self.inputAbc, data )
        print "// Final. //"  
        print "\n"
        