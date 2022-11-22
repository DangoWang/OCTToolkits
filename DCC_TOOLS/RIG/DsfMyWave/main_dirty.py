import maya.mel as mel


all_sel = cmds.ls(sl=1)
sub_ctrls = all_sel[:-1]
main_ctrl = all_sel[-1]
connect_list = ["translateX", "translateY", "translateZ", 
                "scaleX", "scaleY", "scaleZ"]
connect_dict = {"translateX": "tx_amplitude", "translateY": "ty_amplitude", "translateZ": "tz_amplitude", 
                "scaleX": "sx_amplitude", "scaleY": "sy_amplitude", "scaleZ": "sz_amplitude"}

def add_attr():
    for each in sub_ctrls:
        mel.eval("addAttr -ln \"_____wave_____\" -nn \"_____wave _____\" -at bool %s;" % each)
        mel.eval("setAttr -e-keyable true %s._____wave_____" % each)
        
        mel.eval("addAttr -ln \"tx_amplitude\" -at double -min 0 -max 100 -dv 3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.tx_amplitude" % each)
        
        mel.eval("addAttr -ln \"ty_amplitude\" -at double -min 0 -max 100 -dv 3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.ty_amplitude" % each)
        
        mel.eval("addAttr -ln \"tz_amplitude\" -at double -min 0 -max 100 -dv 3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.tz_amplitude" % each)
        
        mel.eval("addAttr -ln \"t_fps\" -at double -min 0.001 -max 1 -dv 0.1 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.t_fps" % each)
        
        mel.eval("addAttr -ln \"t_offset\" -at double -min 0 -max 100 -dv 0 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.t_offset" % each)
        
        mel.eval("addAttr -ln \"t_noise\" -at double -min 0 -max 1 -dv 0 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.t_noise" % each)
        
        mel.eval("addAttr -ln \"_____scale_____\" -nn \"_____scale _____\" -at bool %s;" % each)
        mel.eval("setAttr -e-keyable true %s._____scale_____" % each)
        
        
        mel.eval("addAttr -ln \"sx_amplitude\" -at double -min 0 -max 100 -dv 0.3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.sx_amplitude" % each)
        
        mel.eval("addAttr -ln \"sy_amplitude\" -at double -min 0 -max 100 -dv 0.3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.sy_amplitude" % each)
        
        mel.eval("addAttr -ln \"sz_amplitude\" -at double -min 0 -max 100 -dv 0.3 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.sz_amplitude" % each)
        
        mel.eval("addAttr -ln \"s_fps\" -at double -min 0.001 -max 1 -dv 0.1 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.s_fps" % each)
        
        mel.eval("addAttr -ln \"s_offset\" -at double -min 0 -max 100 -dv 0 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.s_offset" % each)
        
        mel.eval("addAttr -ln \"s_noise\" -at double -min 0 -max 1 -dv 0 %s;" % each)
        mel.eval("setAttr -e -keyable true %s.s_noise" % each)


    mel.eval("addAttr -ln \"t_wave\" -at bool %s;" % main_ctrl)
    mel.eval("setAttr -e -keyable true %s.t_wave" % main_ctrl)
    mel.eval("addAttr -ln \"s_wave\" -at bool %s;" % main_ctrl)
    mel.eval("setAttr -e -keyable true %s.s_wave" % main_ctrl)

    mel.eval("addAttr -ln \"t_wave_offset\" -at long -min -100 -max 100 -dv 10 %s;" % main_ctrl)
    mel.eval("setAttr -e -keyable true %s.t_wave_offset" % main_ctrl)
    mel.eval("addAttr -ln \"s_wave_offset\" -at long -min -100 -max 100 -dv 10 %s;" % main_ctrl)
    mel.eval("setAttr -e -keyable true %s.s_wave_offset" % main_ctrl)


def create_nodes():
    offset_plms = []
    for i, each in enumerate(sub_ctrls):
        for attr in connect_list:
            mld = cmds.shadingNode('multiplyDivide', asUtility=1, name=each+"_"+attr+"_multiDivideNode")
            plm = cmds.shadingNode('plusMinusAverage', asUtility=1, name=each+"_"+attr+"_plusMinusAverageNode")
            mm = cmds.createNode('mayaMathNode', name=each+"_"+attr+"_mayaMathNode")
            mmn = cmds.createNode('mayaMathNode', name=each+"_"+attr+"_mayaMathNodeNoise")
            if 'translate' in attr:
                parent = cmds.listRelatives(each, parent=1)[0]
                connect_info = {(each+"._____wave_____"): (mld+".input1.input1Z"),
                                (each+".t_fps"): (mld+".input2.input2X"),
                                (each+'.'+connect_dict[attr]): (mld+".input2.input2Z"),
                                (each+".t_offset"): (plm+".input1D[0]"),
                                ("time1.outTime"): (plm + '.input1D[1]'),
                                (plm + '.output1D'): (mld + '.input1.input1X'),
                                (each+".t_noise"): (mmn+".input2"),
                                (mmn+".noiseOut"): (parent + '.' +attr),
                                (mld + '.output.outputZ'): (mld+'.input2.input2Y'),
                                (mm+'.sineOut'): (mld+'.input1.input1Y'),
                                (mld+'.output.outputX'): (mm+'.input1'),
                                (mld+'.output.outputY'): (mmn+'.input1')
                                }
            else:
                connect_info = {(each+"._____scale_____"): (mld+".input1.input1Z"),
                                (each+".s_fps"): (mld+".input2.input2X"),
                                (each+'.'+connect_dict[attr]): (mld+".input2.input2Z"),
                                (each+".s_offset"): (plm+".input1D[0]"),
                                (each+".s_noise"): (mmn+".input2"),
                                ("time1.outTime"): (plm + '.input1D[1]'),
                                (plm + '.output1D'): (mld + '.input1.input1X'),
                                ("time1.outTime"): (plm + '.input1D[1]'),
                                (mld + '.output.outputZ'): (mld+'.input2.input2Y'),
                                (mm+'.sineOut'): (mld+'.input1.input1Y'),
                                (mld+'.output.outputX'): (mm+'.input1'),
                                (mld+'.output.outputY'): (mmn+'.input1'),
                                (mmn+'.noiseOut'): (plm+'.input2D[0].input2Dx'),
                                (plm+'.output2D.output2Dx'): (parent + '.' +attr)
                                }
                mel.eval('setAttr \"%s.input2D[1].input2Dx\" 1;'%plm)

            for k, v in connect_info.items():
                cmds.connectAttr(k, v)
        cmds.connectAttr(main_ctrl+'.t_wave', each+'._____wave_____')
        cmds.connectAttr(main_ctrl+'.s_wave', each+'._____scale_____')
        offset_plm = cmds.shadingNode('plusMinusAverage', asUtility=1, name=each+"_wave_offset_plm_"+ str(i))
        offset_plms.append(offset_plm)
        print offset_plm
        cmds.connectAttr(main_ctrl+'.t_wave_offset', offset_plm+'.input1D[0]')
        cmds.connectAttr(each+'.t_offset', offset_plm+'.input1D[1]')
        cmds.connectAttr(main_ctrl+'.s_wave_offset', offset_plm+'.input2D[0].input2Dx')
        cmds.connectAttr(each+'.s_offset', offset_plm+'.input2D[1].input2Dx')
        if i == 0:
            continue
        cmds.connectAttr(offset_plms[i-1]+'.output1D', each+'.t_offset')
        cmds.connectAttr(offset_plms[i-1]+'.output2Dx', each+'.s_offset')

        


def main():
    add_attr()
    create_nodes()
    mel.eval("cycleCheck -e off;")


if __name__ == '__main__':
    main()