import pymel.core as pm
import maya.api.OpenMaya as om
import hashlib

def meshMD5(full_path):
    sl = om.MSelectionList()
    sl.add(full_path)
    mesh_dag = sl.getDagPath(0)
    mesh_mfn = om.MFnMesh(mesh_dag)
    v = mesh_mfn.getVertices()
    v_str0 = '[' + ', '.join([str(i) for i in v[0]]) + ']'
    v_str1 = '[' + ', '.join([str(i) for i in v[1]]) + ']'
    topology = hashlib.md5( v_str0 + ' ' + v_str1).hexdigest()
    return topology

def matchTopu(objlist,lineEdit):
    selist = []
    mesh_path = objlist[0].name()
    if len(objlist)>1:
        objects = []
        grp_name = ''
        for grp in objlist[1:]:
            objects += pm.listRelatives(grp, ad=True, type='mesh', noIntermediate=True)
            grp_name += "%s "%grp
        lineEdit.setText(grp_name)
    else:
        objects = pm.ls(type='mesh')
        lineEdit.setText("Everywhere")
    orgvalue = meshMD5(mesh_path)
    #l_new_mesh = pm.listRelatives(root_node, ad=True, type='mesh', noIntermediate=True)
    for i, mesh in enumerate(objects):
        mesh_name = mesh.name().split('|')[-1]
        full_path = mesh.fullPath()
        newvalue = meshMD5(full_path)
        if newvalue == orgvalue:
            selist.append(mesh)
    return selist


###########
#doMatch()
#######group transfer uv#########
def anylizeGroup(grp_path):
    grp_dic = {}
    #grp_path = pm.ls(sl=1)[0]
    sub_meshs = pm.listRelatives(grp_path, ad=True, type='mesh', noIntermediate=True)
    for mesh in sub_meshs:
        mesh_name = mesh.name().split('|')[-1]
        full_path = mesh.fullPath()
        hash_value = meshMD5(full_path)
        if grp_dic.has_key(hash_value):
            grp_dic[hash_value].append(mesh)
        else:
            grp_dic[hash_value] = [mesh,]
    return grp_dic

def dictTransUV(dic_a,dic_b):
    #dic_a,dic_b = anylizeGroup(pm.ls(sl=1)[0]),anylizeGroup(pm.ls(sl=1)[1])
    for key in dic_a.keys():
        if key in dic_b.keys():
            for i,obj in enumerate(dic_b[key]):
                #pm.transferAttributes(dic_a[key][i%len(dic_a[key])],obj,sampleSpace=4, transferUVs=2)
                pm.polyTransfer(obj,uv=1,ao=dic_a[key][i%len(dic_a[key])])
                print "copy uv from %s to ------>> %s!"%(obj,dic_a[key][i%len(dic_a[key])])

def groupTransUV():
    groups = pm.ls(sl = 1)
    diver_grp = groups.pop(0)
    diver_dic = anylizeGroup(diver_grp)
    for grp in groups:
        tag_dic = anylizeGroup(grp)
        dictTransUV(diver_dic,tag_dic)
#######group transfer uv end#####


