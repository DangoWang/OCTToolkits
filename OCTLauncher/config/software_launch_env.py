#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.GLOBAL import *
current_exe_path = CURRENTSCRIPTPATH
launch_env = {
    "Maya2017": {
        "Env": [
            {
                "mode": "post", 
                "name": "MAYA_UI_LANGUAGE", 
                "value": "en_US"
            }, {
                "mode": "over",
                "name": "proj",
                "value": "Z:/DS/Temp/OriginalForce"
            },{
                "mode": "post",
                "name": "PATH",
                "value": "Z:/DS/Temp/OriginalForce/plugin/opiumPipe/0.97/win_lib"
            },
            {
                "mode": "over", 
                "name": "MAYA_DISABLE_CLIC_IPM", 
                "value": "1"
            }, 
            {
                "mode": "over", 
                "name": "MAYA_DISABLE_CER", 
                "value": "1"
            }, 
            {
                "mode": "over", 
                "name": "MAYA_DISABLE_CIP", 
                "value": "1"
            },
            {
                "mode": "pre",
                "name": "PYTHONPATH",
                "value": CURRENTSCRIPTPATH + '/thirdparty;' + CURRENTSCRIPTPATH + ';' + CURRENTSCRIPTPATH + '/DCC_TOOLS'
            },
            # {
            #     "mode": "pre",
            #     "name": "MAYA_MODULE_PATH",
            #     "value": CURRENTSCRIPTPATH + '/DCC_TOOLS/maya_module'
            # },
            {
                "mode": "post",
                "name": "MAYA_SCRIPT_PATH",
                "value": CURRENTSCRIPTPATH + '/DCC_TOOLS'
            },
            {
                "mode": "post",
                "name": "XBMLANGPATH",
                "value": CURRENTSCRIPTPATH + '/icons'
            },
            {
                "mode": "pre", 
                "name": "MAYA_HELP_URL", 
                "value": "file://oct.ds.com/TD/Tools/Plugins/MayaHelp2017_chs/index.html#!/url=./files/mePortal.htm"
            },
        ],
        "Exec": "C:/Program Files/Autodesk/Maya2017/bin/maya.exe",
        "GroupBox": "DCC_btn_grp",
        "Label": "Maya2017"
    },"Maya2019": {
        "Env": [
            {
                "mode": "post",
                "name": "MAYA_UI_LANGUAGE",
                "value": "en_US"
            }, {
                "mode": "over",
                "name": "proj",
                "value": "Z:/DS/Temp/OriginalForce"
            },
            {
                "mode": "over",
                "name": "MAYA_DISABLE_CLIC_IPM",
                "value": "1"
            },
            {
                "mode": "over",
                "name": "MAYA_DISABLE_CER",
                "value": "1"
            },
            {
                "mode": "over",
                "name": "MAYA_DISABLE_CIP",
                "value": "1"
            },
            {
                "mode": "pre",
                "name": "PYTHONPATH",
                "value": CURRENTSCRIPTPATH + '/thirdparty;' + CURRENTSCRIPTPATH + ';' + CURRENTSCRIPTPATH + '/DCC_TOOLS'
            },
            # {
            #     "mode": "pre",
            #     "name": "MAYA_MODULE_PATH",
            #     "value": CURRENTSCRIPTPATH + '/DCC_TOOLS/maya_module'
            # },
            {
                "mode": "post",
                "name": "MAYA_SCRIPT_PATH",
                "value": CURRENTSCRIPTPATH + '/DCC_TOOLS'
            },
            {
                "mode": "post",
                "name": "XBMLANGPATH",
                "value": CURRENTSCRIPTPATH + '/icons'
            },
            {
                "mode": "pre",
                "name": "MAYA_HELP_URL",
                "value": "file://oct.ds.com/TD/Tools/Plugins/MayaHelp2017_chs/index.html#!/url=./files/mePortal.htm"
            },
        ],
        "Exec": "C:/Program Files/Autodesk/Maya2019/bin/maya.exe",
        "GroupBox": "DCC_btn_grp",
        "Label": "Maya2019"
    },
    "Houdini17.5": {
        "Env": [
            {
                "mode": "pre",
                "name": "PYTHONPATH",
                "value": CURRENTSCRIPTPATH + '/DCC_TOOLS/EFX/houdini_scripts/oct_tools;' + CURRENTSCRIPTPATH + '/thirdparty;&'
            },
            {
                "mode": "pre",
                "name": "HOUDINI_TOOLBAR_PATH",
                "value": CURRENTSCRIPTPATH + '/DCC_TOOLS/EFX/houdini_scripts/oct_toolbar;&'
            },
            {
                "mode": "pre",
                "name": "HOUDINI_OTLSCAN_PATH",
                "value": CURRENTSCRIPTPATH + '/DCC_TOOLS/EFX/houdini_scripts/oct_otls;&'
            },
        ],
        "Exec": "C:/Program Files/Side Effects Software/Houdini 17.5.293/bin/houdini.exe",
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Houdini17.5"
    },
    "Nuke9.0": {
        "Env": [
            {
                "mode": "over",
                "name": "foundry_LICENSE",
                "value": '5053@lic.ds.com'
            },{
                "mode": "pre",
                "name": "NUKE_PATH",
                "value": CURRENTSCRIPTPATH + 'DCC_TOOLS/COM/Nuke_plugins_Oct'
            },
        ],
        "Exec": '\"C:/Program Files/Nuke9.0v8/Nuke9.0.exe\" --nukex',
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Nuke9.0"
    },
    "Nuke11.3v6": {
        "Env": [
            {
                "mode": "over",
                "name": "foundry_LICENSE",
                "value": '5053@lic.ds.com'
            },
            {
                "mode": "pre",
                "name": "NUKE_PATH",
                "value": CURRENTSCRIPTPATH + 'DCC_TOOLS/COM/Nuke_plugins_Oct'
            },
        ],
        "Exec": '\"C:/Program Files/Nuke11.3v6/Nuke11.3.exe\" --nukex',
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Nuke11.3v6"
    },
    # "OCT": {
    #     "Env": [
    #         {
    #             "mode": "post",
    #             "name": "PYTHONPATH",
    #             "value": "\\\\192.168.15.242\\plugins\\Maya2017\\Scripts;"
    #         }
    #     ],
    #     "Exec": "\\\\192.168.15.242\\Plugins\\DailyTools\\OCT Tools.bat",
    #     "GroupBox": "pipe_btn_grp",
    #     "Label": "OCT"
    # },
    "BR": {
        "Env": "",
        "Exec": CURRENTSCRIPTPATH + "\\bin\\mayaBatchRender\\Batch Script Generator v1.3.exe",
        "GroupBox": "other_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "BR",
        "Groups": ["Texture", "Lighting"],
    },
    "Mari4": {
        "Env": "",
        "Exec": "C:/Program Files/Mari4.0v1/Bundle/bin/Mari4.0v1.exe",
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Mari4"
    },
    "Snipaste": {
        "Env": "",
        "Exec": CURRENTSCRIPTPATH + "\\bin\\Snipaste-1.16.2-x64\\Snipaste.exe",
        "GroupBox": "other_btn_grp",
        "Label": u"截图工具"
    },
    "RvPlayer": {
        "Env": "",
        "Exec": "C:\\Program Files\\Shotgun\\RV-7.0\\bin\\rv.exe",
        "GroupBox": "other_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Rv7.2"
    },
    "SubstancePainter": {
        "Env": "",
        "Exec": "C:\\Program Files\\Allegorithmic\\Substance Painter\\Substance Painter.exe",
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "SubPainter"
    },
    "Zbrush": {
        "Env": "",
        "Exec": "C:\\Program Files\\Pixologic\\ZBrush 2018\\ZBrush.exe",
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "Zbrush"
    },
    "PsCS6": {
        "Env": "",
        "Exec": "C:\\Program Files\\Adobe\\Photoshop CS6\\Photoshop.exe",
        "GroupBox": "DCC_btn_grp",
        "Forbidden": ["outsource"],
        "Label": "PsCS6"
    },
    # "Chrome": {
    #     "Env": "",
    #     "Exec": u"\\\\192.168.15.8\\资料库\\【软件库】\\4_工具软件\\Chrome\\Application\\chrome.exe",
    #     "GroupBox": "other_btn_grp",
    #     "Label": "Chrome"
    # },
    "Arnold": {
        "Env": "",
        "Exec": CURRENTSCRIPTPATH + "\\bin\\solidangle\\mtoadeploy\\auto_solidangle.bat",
        "GroupBox": "other_btn_grp",
        "Label": "Arnold"
    }, "Yeti2.2.5": {
        "Env": "",
        "Exec": CURRENTSCRIPTPATH + "\\bin\\Yeti-v2.2.5\\auto_Yeti.bat",
        "GroupBox": "other_btn_grp",
        "Label": "Yeti2.2.5"
    }, "Autumn": {
        "Env": "",
        "Exec": "python " + CURRENTSCRIPTPATH + '/SystemTools/Autumn/autumn_main.py',
        "GroupBox": "pipe_btn_grp",
        "Label": "Autumn"
    }, "Ticket": {
        "Env": "",
        "Exec": "python " + CURRENTSCRIPTPATH + '/SystemTools/Ticket_System/TicketSystem.py',
        "GroupBox": "pipe_btn_grp",
        "Forbidden": ["outsource"],
        "Label": u"工单系统"
    }, "ChangeSize": {
        "Env": "",
        "Exec": "python " + CURRENTSCRIPTPATH + '/ArtistTools/change_tex_size/Change_Szie.py',
        "GroupBox": "other_btn_grp",
        "Groups": ["Texture", "Lighting"],
        "Forbidden": ["outsource"],
        "Label": u"更改贴图尺寸"
    },"TimeLog": {
        "Env": "",
        "Exec": "python " + CURRENTSCRIPTPATH + '/SystemTools/TimeLogMessage/my_log_window.py',
        "GroupBox": "pipe_btn_grp",
        "Forbidden": ["outsource"],
        "Label": u"工作日志"
    },"WiKi": {
        "Env": "",
        "Exec": "python " + CURRENTSCRIPTPATH + '/SystemTools/Confluence/main.py',
        "GroupBox": "pipe_btn_grp",
        "Forbidden": ["outsource"],
        "Label": u"WiKi"
    },"CompImage": {
        "Env": "",
        "Exec": CURRENTSCRIPTPATH + '/SystemTools/comp_image/comp_image.exe',
        "GroupBox": "other_btn_grp",
        "Forbidden": ["outsource"],
        "Groups": ["Texture", "Lighting"],
        "Label": u"拼接图片"
    },
}
