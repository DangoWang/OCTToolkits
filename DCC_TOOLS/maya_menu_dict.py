#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import maya.mel as mel
from config import GLOBAL

def get_config(mode):
    oct_tools_menu_register_local = dict(
                common=mod_tools + rig_tools + tex_tools + flo_tools + efx_tools + cfx_tools + an_tools + lgt_tools,
    )
    if mode in ['online']:
        import utils.shotgun_operations as sg
        oct_tools_menu_register = dict(common=[{'label': 'Login Info', 'value': '', 'icon': '', },
                                               {'label': 'User: ' + sg.get_user(), 'value': 'pass_func', 'icon': '', },
                                               {'label': 'Project: ' + sg.get_project(), 'value': 'pass_func',
                                                'icon': '', }, {'label': 'PipeLine', 'value': '', 'icon': '', },
                                               {'value': 'oct_loader', 'label': 'Loader',
                                                'icon': 'multimedia/_Playing Music.svg', },
                                               {'value': 'maya_submit', 'label': 'SubmitFiles',
                                                'icon': 'business/compass-1.svg', },
                                               {'label': 'Tools', 'value': '', 'icon': '', }],
                                       Model=mod_tools, Rigging=rig_tools, Texture=tex_tools,
                                       Flo=flo_tools, Ef=efx_tools, Cloth=cfx_tools,
                                       Fur=cfx_tools, An=an_tools, Lgt=lgt_tools,
                                      )
        return oct_tools_menu_register
    return oct_tools_menu_register_local


mod_tools = [{'label': u'模型工具', 'value': [{'label': 'abSymMesh', 'value': 'absymmesh_win', 'icon': '', },
                {'label': 'apiTransUVs', 'value': 'apitransuvs_win', 'icon': '', },
                {'label': 'setTexPathCMD', 'value': 'set_texture_path', 'icon': '', },
                {'label': 'cut_ch_head', 'value': 'cut_head_win', 'icon': '', },
                {'label': 'CheckModel', 'value': 'check_model', 'icon': '', },
                # {'label': 'modCheckTools', 'value': 'model_check_tool', 'icon': '', },
                # {'label': 'modelReshape', 'value': 'model_reshape', 'icon': '', },
                {'label': 'GMH 2.x', 'value': 'run_GMH2', 'icon': '', },
                {'label': 'PivotZeroWin', 'value': 'pivot_zero_win', 'icon': '', },
                {'label': 'quick_pipe', 'value': 'quick_pipe_tool', 'icon': '', },
                {'label': 'replaceAllShaderToLambert', 'value': 'replace_shader_to_lambert', 'icon': '', },
                {'label': 'wp_rename', 'value': 'wp_rename_tool', 'icon': '', }, ], 'icon': '', }]
rig_tools = [{'label': u'绑定工具',
                      'value': [{'label': 'animReverseDirection', 'value': 'an_reverse_direction', 'icon': '', },
                          {'label': 'cut_ch_model', 'value': 'cut_model_win', 'icon': '', },
                          {'label': 'dsf_my_wave', 'value': 'dsf_my_wave_tool', 'icon': '', },
                          {'label': 'setTexPathCMD', 'value': 'set_texture_path', 'icon': '', },
                          {'label': 'CheckRig', 'value': 'check_rig', 'icon': '', },

                          # {'label': 'meshCentCrvDrawer', 'value': 'mesh_center_drawer', 'icon': '', },
                          {'label': 'Mirror_BlendshapeUI', 'value': 'mirror_blendshape_win', 'icon': '', },
                          {'label': 'ngskintools', 'value': 'ngskintools', 'icon': '', },
                          {'label': 'NurbsShapeTransferTool', 'value': 'nurbsshape_transfer_tool', 'icon': '', },
                          {'label': 'riggingReverseDirection', 'value': 'rig_reverse_direction', 'icon': '', },
                          {'label': 'runLatticeToMesh', 'value': 'run_lattice_to_mesh', 'icon': '', }, ],
                      'icon': '', }, ]
tex_tools = [{'label': u'材质工具',
                      'value': [{'label': 'change_texture', 'value': 'change_texture_tool', 'icon': '', },
                          # {'label': 'Env_To_OCT', 'value': 'env_to_oct', 'icon': '', },
                          {'label': 'FileTextureManager', 'value': 'file_texture_manager', 'icon': '', },
                          {'label': 'shaderTransfer', 'value': 'shaderTransfer', 'icon': '', },
                          {'label': 'hotOceanDeformer', 'value': 'hot_ocean_deformer', 'icon': '', },
                          {'label': 'lcxtranuv', 'value': 'lcxtranuv_tool', 'icon': '', },
                          {'label': 'NSUV', 'value': 'nusv_tool', 'icon': '', },
                          {'label': 'CheckTex', 'value': 'check_tex', 'icon': '', },
                          {'label': 'setTexPathCMD', 'value': 'set_texture_path', 'icon': '', },
                          {'label': 'shader_library', 'value': 'shader_library_tool', 'icon': '', },
                          {'label': 'spPaint3d', 'value': 'sppaint3d_tool', 'icon': '', },
                          {'label': 'transfer_uv', 'value': 'transfer_uv_tool', 'icon': '', },
                          {'label': 'TransferShaderWindow', 'value': 'transfer_shader_window', 'icon': '', },
                          {'label': 'TransferShadingCmd', 'value': 'transfer_shading_cmd', 'icon': '', },
                          {'label': 'Show_Material', 'value': 'show_material_cmd', 'icon': '', },],
                      'icon': '', }, ]
cfx_tools = [{'label': u'角色特效工具',
                    'value': [{'label': 'createClothRig', 'value': 'create_cloth_rig', 'icon': '', },
                        {'label': 'AbcExportTool', 'value': 'abc_export_tool', 'icon': '', },
                        {'label': 'AbcInputTool', 'value': 'abc_input_tool', 'icon': '', },
                        {'label': 'AbcUpdateTool', 'value': 'abc_update_tool', 'icon': '', },
                        {'label': 'CheckCFX', 'value': 'check_cfx', 'icon': '', }, ], 'icon': '', }, ]
an_tools = [{'label': u'动画工具',
                        'value': [{'label': 'animationCreateCurve', 'value': 'an_create_curve', 'icon': '', },
                            {'label': 'animLayerToBase', 'value': 'an_layer_tobase', 'icon': '', },
                            {'label': u'反转动画轴向', 'value': 'an_reverse_direction', 'icon': '', },
                            # {'label': 'AssetLibraryWin', 'value': 'asset_library_win', 'icon': '', },
                            {'label': u'文件检查', 'value': 'check_an', 'icon': '', },
                            {'label': u'MGPicker', 'value': 'MG_picker', 'icon': 'PickerWindowIcon_anim.png', },
                            # {'label': 'cleanFileCMD', 'value': 'clean_file_cmd', 'icon': '', },
                            {'label': 'connectMocapWin', 'value': 'connect_mocap_win', 'icon': '', },
                            {'label': 'DisplayLayerForAnimationWin', 'value': 'display_layer_animation', 'icon': '', },
                            {'label': u'梦魇运动路径工具', 'value': 'night_maremotion_path', 'icon': '', },
                            {'label': u'拍屏工具', 'value': 'oct_play_blast', 'icon': 'multimedia/Forward.svg', },
                            {'label': 'parentToTargetCmd', 'value': 'parent_to_target', 'icon': '', },
                            {'label': 'ShakeToRotateCmd', 'value': 'shake_to_rotate', 'icon': '', },
                            {'label': u'标准相机工具', 'value': 'standard_camera_win', 'icon': '', },
                            {'label': u'StudioLibrary', 'value': 'studio_library_tool', 'icon': '', },
                            {'label': 'animHUD', 'value': 'animation_hud', 'icon': '', },
                            {'label': u'打组工具', 'value': 'group_win', 'icon': '', },
                            {'label': u'导出缓存', 'value': 'abc_export_tool', 'icon': '', },
                            {'label': u'缓存代理工具', 'value': 'abc_proxy_tool', 'icon': '', }], 'icon': '', }, ]
lgt_tools = [{'label': u'灯光工具',
                       'value': [{'label': 'mayaToNuke', 'value': 'maya_to_nuke', 'icon': '', },
                           {'label': 'SaveSequenceForRenderView', 'value': 'save_sequence_for_renderview',
                            'icon': '', }, {'label': 'toStereoToolCmd', 'value': 'to_stereo_tool', 'icon': '', },
                           {'label': 'AbcUpdateTool', 'value': 'abc_update_tool', 'icon': '', },
                           {'label': 'AbcInputTool', 'value': 'abc_input_tool', 'icon': '', }, ], 'icon': '', }, ]
flo_tools = [{'label': 'FLOTools',
                          'value': [{'label': 'AbcInputTool', 'value': 'abc_input_tool', 'icon': '', },
                              # {'label': 'AbcInputWin', 'value': 'abc_input_win', 'icon': '', },
                              # {'label': 'AbcOutputWin', 'value': 'abc_output_win', 'icon': '', },
                              # {'label': 'AssetLibraryWin', 'value': 'asset_library_win', 'icon': '', },
                              # {'label': 'CompareTopo', 'value': 'compare_topo', 'icon': '', },
                              # {'label': 'fl_work_cmd', 'value': 'fl_work_win', 'icon': '', },
                              # {'label': 'fur_in', 'value': 'fur_in_win', 'icon': '', },
                              # {'label': 'fur_out', 'value': 'fur_out_win', 'icon': '', },
                              # {'label': 'loadUV', 'value': 'load_uv', 'icon': '', },
                          ], 'icon': '', }, ]
efx_tools = [{'label': u'场景特效工具',
                       'value': [{'label': '', 'value': '', 'icon': '', },
                     ], 'icon': '', }, ]


def run_GMH2():
    os.environ['MAYA_SCRIPT_PATH'] = os.environ['MAYA_SCRIPT_PATH'] + ';' + \
                                      GLOBAL.CURRENTSCRIPTPATH + '/DCC_TOOLS/MOD;'\
                                    + GLOBAL.CURRENTSCRIPTPATH + '/DCC_TOOLS/MOD/THUNDERCLOUD;'\
                                    + GLOBAL.CURRENTSCRIPTPATH + '/DCC_TOOLS/MOD/THUNDERCLOUD/PDDMelLib;'
    mel.eval('source "MOD/THUNDERCLOUD/GMH2/GMH2_starter.mel";')


def maya_submit():
    from DCC_TOOLS.common.maya_submit import main
    reload(main)
    submit_win = main.OctMayaSubmit()
    submit_win.show()


def oct_loader():
    from DCC_TOOLS.common.Loader import oct_loader_main
    oct_loader_win = oct_loader_main.main()
    oct_loader_win.show()
    pass


def pass_func():
    pass


#  -------------------------------------------Animation_Tool---------------------------------------------

def an_create_curve():
    import DCC_TOOLS.AN.animationCreateCurve as animationCreateCurve
    reload(animationCreateCurve)
    animationCreateCurve.animationCreateCurve()


def an_layer_tobase():
    from DCC_TOOLS.AN import animLayerToBase
    reload(animLayerToBase)
    animLayerToBase.animLayerToBase()


def an_reverse_direction():
    from DCC_TOOLS.AN.RevDireTool import reverse_animcrv
    reload(reverse_animcrv)
    reverse_animcrv.ReverseAniCrv().show()


def MG_picker():
    mel_string = """
    string $mgpicker_programDir = `getenv "MGPICKER_PROGRAM_FILE_DIR"`;if(`filetest -d $mgpicker_programDir`)
    {eval ("source \\""+$mgpicker_programDir+"/MGPicker_WrittenByMiguel.mel"+"\\"");}else 
    { eval ("source \\"%sDCC_TOOLS/AN/MG-PickerStudio.Windows.20170512/MG-PickerStudio/MGPicker_Program/MGPicker_WrittenByMiguel.mel\\""); };
    MG_PickerStudio 1;
    """ % GLOBAL.CURRENTSCRIPTPATH
    print mel_string
    mel.eval(mel_string)


def asset_library_win():
    from DCC_TOOLS.common.AssetsLibrary import assetLibrary
    reload(assetLibrary)
    assetLibrary.show()


def clean_file_cmd():
    # from DCC_TOOLS.AN.
    pass


def connect_mocap_win():
    import DCC_TOOLS.AN.connectMocap as connect_Mocap
    reload(connect_Mocap)
    connect_Mocap.main()


def display_layer_animation():
    import DCC_TOOLS.AN.DisplayLayerForAnimation as Display_animation
    reload(Display_animation)
    Display_animation.show()


def night_maremotion_path():
    from DCC_TOOLS.AN.NightmareMotionPath import oct_nm_mopath
    reload(oct_nm_mopath)
    window = oct_nm_mopath.OctNMMPath()
    window.show()


def oct_play_blast():
    from DCC_TOOLS.AN.simple_playblast import spb_main
    reload(spb_main)
    window = spb_main.DsfSimplePlayBlast()
    window.show()


def parent_to_target():
    import os
    import maya.mel as mel
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/")+"/AN/parentToTarget.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('whr_parentToTarget')


def shake_to_rotate():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/AN/whr_shakeToRotateCmd.mel"
    print(current_dir)
    mel.eval('source "{}";whr_shakeToRotateCmd();'.format(current_dir))


def standard_camera_win():
    from DCC_TOOLS.AN.StandardCamera import std_camera
    reload(std_camera)
    std_camera.show()


def studio_library_tool():
    import sys
    import inspect
    import DCC_TOOLS.AN
    sys.path.append(str(os.path.split(os.path.realpath(inspect.getsourcefile(DCC_TOOLS.AN)))[0])+"\\studiolibrary")
    import studiolibrary
    reload(studiolibrary)
    studiolibrary.main()


def animation_hud():
    import os
    import maya.mel as mel
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/AN/animHUD.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('animHUD')


def group_win():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/AN/dazu/dazu.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir) )
    mel.eval('dazumel')


def abc_export_tool():
    from DCC_TOOLS.common.abc_pipe import abc_export_win
    abc_export_win.main()


def abc_input_tool():
    from DCC_TOOLS.common.abc_pipe import abc_input_win
    abc_input_win.main()


def abc_proxy_tool():
    from DCC_TOOLS.AN.proxySwitch import addProxySwitch
    reload(addProxySwitch)
    addProxySwitch.win()


#  -------------------------------------------CFX_Tool---------------------------------------------


def create_cloth_rig():
    from DCC_TOOLS.CFX.CreateClothRig import clothRig_dlg
    reload(clothRig_dlg)
    clothRig_dlg._OCT_runClothRig_DLG()

def abc_update_tool():
    from DCC_TOOLS.common.abc_pipe import abc_update_win
    reload(abc_update_win)
    abc_update_win.main()


#  -------------------------------------------FLO_Tool---------------------------------------------


def abc_input_win():
    from DCC_TOOLS.FLO.AbcCacheTool import AbcInput
    reload(AbcInput)
    AbcInput.main()


def abc_output_win():
    from DCC_TOOLS.FLO.AbcCacheTool import AbcOutput
    reload(AbcOutput)
    AbcOutput.main()


def compare_topo():
    from DCC_TOOLS.FLO.topo_compare import main as topoin
    reload(topoin)
    topo_window = topoin.TopoCompare()
    topo_window.show()


def fl_work_win():
    from DCC_TOOLS.FLO.fl_work import main as flwm
    reload(flwm)
    flwm_window = flwm.FlWork()
    flwm_window.show()


def fur_in_win():
    from DCC_TOOLS.FLO.fur_pipe import main as furm
    reload(furm)
    furmWin = furm.FurInWin()
    furmWin.show()


def fur_out_win():
    from DCC_TOOLS.FLO.fur_pipe import main as furm
    reload(furm)
    furmW = furm.FurOutWin()
    furmW.show()


def load_uv():
    import DCC_TOOLS.FLO.uv_load.main as uvin
    reload(uvin)
    uvin_window = uvin.UVLoad()
    uvin_window.show()


#  -------------------------------------------Model_Tool---------------------------------------------


def absymmesh_win():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/MOD/abSymMesh.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('abSymMesh')


def apitransuvs_win():
    from DCC_TOOLS.MOD import apiTransUVs
    reload(apiTransUVs)
    apiTransUVs.apiTransUVsUI()


def clean_scene_win():
    from DCC_TOOLS.MOD.check_model import check_model
    reload(check_model)
    check_model_window = check_model.CheckModel()
    check_model_window.show()


def cut_head_win():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/MOD/cut_head/cut_head.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))


def model_check_tool():
    from DCC_TOOLS.MOD import modCheckTools
    reload(modCheckTools)
    modCheckTools.modCheckToolsUI()


def model_reshape():
    from DCC_TOOLS.MOD.meshReshaper import mesh_reshape_main
    reload(mesh_reshape_main)
    check_model_window = mesh_reshape_main.MeshReshape()
    check_model_window.show()


def pivot_zero_win():
    import DCC_TOOLS.MOD.PivotZero2 as PivotZero
    reload(PivotZero)
    PivotZero.main()


def quick_pipe_tool():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/") + "/MOD/Quick Pipe 1_5b/LaunchQuickPipe.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))


def replace_shader_to_lambert():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/MOD/replaceAllShaderToLambert.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('replaceAllShaderToLambert')


def wp_rename_tool():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/MOD/wp_rename.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('wp_rename')


#  -------------------------------------------Rig_Tool---------------------------------------------


def cut_model_win():
    from DCC_TOOLS.RIG.cutCHModel import cut_ch_model
    reload(cut_ch_model)
    cut_ch_model.CutChModel().show()


def dsf_my_wave_tool():
    from DCC_TOOLS.RIG.DsfMyWave import main as nmw
    reload(nmw)
    nmw_window = nmw.NMWave()
    nmw_window.show()


def mesh_center_drawer():
    from DCC_TOOLS.RIG.meshCentCrvDrawer import mesh_central_crv_drawer_main
    reload(mesh_central_crv_drawer_main)
    mesh_central_crv_drawer_main.MeshCentrCrvDrawer().show()


def mirror_blendshape_win():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/RIG/Mirror_BlendShapeUI.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('Mirror_BlendShapeUI')


def ngskintools():
    from DCC_TOOLS.RIG.ngskintools.ui.mainwindow import MainWindow
    MainWindow.open()


def nurbsshape_transfer_tool():
    from DCC_TOOLS.RIG.nurbsShapeTransfer import main as nsf
    reload(nsf)
    window1 = nsf.NurbsShapeTransfer()
    window1.show()


def rig_reverse_direction():
    from DCC_TOOLS.RIG.RevDireTool import reverse_direction
    reload(reverse_direction)
    reverse_direction.ReverseDirection().show()


def run_lattice_to_mesh():
    from DCC_TOOLS.RIG.latticeToMesh import latticeToMesh_dlg
    reload(latticeToMesh_dlg)
    latticeToMesh_dlg._OCT_runLatticeToMesh_DLG()


#  -------------------------------------------TEX_Tool---------------------------------------------


def shaderTransfer():
    from DCC_TOOLS.TEX.shaderTransfer import jn_shaderTransfer
    reload(jn_shaderTransfer)
    jn_shaderTransfer.main()

def change_texture_tool():
    from DCC_TOOLS.TEX.change_tex import change_tex_main
    reload(change_tex_main)
    change_tex_win = change_tex_main.ChangeTex()
    change_tex_win.show()


def env_to_oct():
    # from DCC_TOOLS.TEX.setTexPath import se
    # from setTexPath import
    # setOctPath.setPathEnvToOCT()
    pass


def file_texture_manager():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/TEX/FileTextureManager.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval("FileTextureManager;")


def hot_ocean_deformer():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/TEX/hotOcean_Maya/Release/deformer/2017/win64/hotOceanDeformer.mll"
    print(current_dir)
    try:
        mel.eval('deformer -type hotOceanDeformer;')
    except:
        mel.eval('loadPlugin "{}"'.format(current_dir))
        hot_ocean_deformer()


def lcxtranuv_tool():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/TEX/lcxtranuv.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('lcxtranuv;')


def nusv_tool():
    import DCC_TOOLS.TEX.NSUV
    pass


def set_texture_path():
    from DCC_TOOLS.TEX.setTexPath import main as stp
    reload(stp)
    stp.SetTexPath().show()


def shader_library_tool():
    import DCC_TOOLS.TEX.shaderLibrary as shaderLibrary
    shaderLibrary.show_window()


def sppaint3d_tool():
    import maya.mel as mel
    import os,sys
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\","/")
    print(current_dir)
    help_path = current_dir + "TEX/spPaint3d_2011.1/help"
    script_path = current_dir + "TEX/spPaint3d_2011.1/scripts"
    icons_path = current_dir + "TEX/spPaint3d_2011.1/prefs/icons"
    sys.path.append(help_path)
    sys.path.append(script_path)
    import spPaint3dGui
    old_icon_path = mel.eval('getenv XBMLANGPATH;')
    mel.eval('putenv "XBMLANGPATH" "{};{};";'.format(icons_path,old_icon_path))
    spPaint3dwin = spPaint3dGui.spPaint3dWin()


def transfer_uv_tool():
    from DCC_TOOLS.TEX.transfer_uv import transfer_uv_tools
    reload(transfer_uv_tools)
    window = transfer_uv_tools.showWindow()


def transfer_shader_window():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/TEX/transferShader_v05.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))
    mel.eval('TransferShaderWindow;')


def transfer_shading_cmd():
    import DCC_TOOLS.TEX.TransferShading as TransferShading
    reload(TransferShading)
    TransferShading.TransferShading("")


def show_material_cmd():
    import DCC_TOOLS.TEX.Tex_Generate_Preview.tex_generate_preview as tex_generate_preview
    reload(tex_generate_preview)
    tex_generate_preview.GeneratePreview().show()

#  -------------------------------------------LIG_Tool---------------------------------------------


def maya_to_nuke():
    # import DCC_TOOLS.LGT.mayaToNuke
    import DCC_TOOLS.LGT.mayaToNuke as mayaToNuke
    mayaToNuke.mayaToNuke()


def save_sequence_for_renderview():
    import maya.mel as mel
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__)).replace("\\",
                                                                     "/") + "/LIG/saveRenderImageSequence.mel"
    print(current_dir)
    mel.eval('source "{}"'.format(current_dir))


def to_stereo_tool():
    pass


#  -------------------------------------------check---------------------------------------------


def check_model():
    from DCC_TOOLS.common.maya_submit.tools.check_mod import check_mod
    check_mod.CheckModel().show()


def check_an():
    from DCC_TOOLS.common.maya_submit.tools.check_an import check_an
    reload(check_an)
    check_an.CheckLayout().show()


def check_ly():
    from DCC_TOOLS.common.maya_submit.tools.check_ly import check_ly
    reload(check_ly)
    check_ly.CheckLayout().show()


def check_rig():
    from DCC_TOOLS.common.maya_submit.tools.check_rig import check_rig
    reload(check_rig)
    check_rig.CheckRigging().show()


def check_tex():
    from DCC_TOOLS.common.maya_submit.tools.check_tex import check_tex
    check_tex.CheckMaterial().show()


def check_cfx():
    from DCC_TOOLS.common.maya_submit.tools.check_cloth import check_cloth
    check_cloth.CheckCFX().show()






