import os
import shutil

def get_images():
    return [(i,i["file"].value()) for i in [i for i in nuke.allNodes() if i.Class() in ["Read", "Camera2", "ReadGeo2"]]]

def copy_images():
    proj_path = "Z:/DS/Work/LGT/render/lr01/090"
    local_path = os.path.dirname(nuke.root().knob("name").value())+"/elements"
    n = get_images()
    for i in n:
        if proj_path in i[1]:
            print i[0].name()+":"
            if "%" in i[1]:
                if not os.access(os.path.dirname(i[1].replace(proj_path, local_path)), 1):
                    shutil.copytree(os.path.dirname(i[1]), os.path.dirname(i[1].replace(proj_path, local_path)))
                    print "copy %s => %s"%(os.path.dirname(i[1]), os.path.dirname(i[1].replace(proj_path, local_path)))
                else:
                    print "file %s is exist"%i[1].replace(proj_path, local_path)
            elif not os.access(i[1].replace(proj_path, local_path), 1):
                if not os.access(os.path.dirname(i[1].replace(proj_path, local_path)), 1):
                    os.makedirs(os.path.dirname(i[1].replace(proj_path, local_path)))
                shutil.copyfile(i[1], i[1].replace(proj_path, local_path))
                print "copy %s => %s"%(i[1], i[1].replace(proj_path, local_path))
        if i[0].Class() == "Read":
            i[0]["proxy"].setValue(i[1].replace(proj_path, local_path))
    nuke.root()["proxy"].setValue(1)
    nuke.root()["proxy_scale"].setValue(1)
    nuke.root()["proxySetting"].setValue(3)
