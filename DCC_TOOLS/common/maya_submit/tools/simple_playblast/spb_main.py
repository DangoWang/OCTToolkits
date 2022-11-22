#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/10


__author__ = "dango wang"


import os
import sys
import time
import logging
import shutil
import subprocess
import getpass
import ui
import list_maya_info
import maya.cmds as mc
import text_format
import maya.mel as mel
import pymel.core as pm
from DCC_TOOLS.common.dcc_utils import *
from config import GLOBAL
reload(text_format)
reload(list_maya_info)
reload(ui)
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    import PySide.QtGui as QtWidgets
    from PySide import QtCore

# necessary global param
cfg_path = mc.internalVar(usd=True) + 'dsf_playblast_cfg'


class DsfSimplePlayBlast(ui.PlayBlastDialog):
    def __init__(self):
        super(DsfSimplePlayBlast, self).__init__()
        self.setupUi(self)
        self.set_artist()

    def set_artist(self):
        artist = getpass.getuser()
        if os.path.isfile(cfg_path):
            with open(cfg_path, 'r') as f:
                artist = f.read()
        self.artist_le.setText(artist)

    def closeEvent(self, event):
        artist = self.artist_le.text()
        if not artist:
            event.accept()
        with open(cfg_path, 'w') as f:
            f.write(artist)
        event.accept()

    @QtCore.Slot()
    def on_input_mov_name_pb_clicked(self):
        current_file_name = list_maya_info.get_current_file_name().split(".")[0]
        mov_name = current_file_name+'_pv'
        self.mov_name_le.setText(mov_name)
        return current_file_name

    @QtCore.Slot()
    def on_input_cam_name_pb_clicked(self):
        sel = mc.ls(sl=1)
        if sel:
            self.cam_name_le.setText(sel[0])
            return

    @QtCore.Slot()
    def on_input_file_path_pb_clicked(self):
        # set file path
        scene_path = list_maya_info.get_current_file_name(full_path=True, dir_path=True)
        try:
            self.file_path_le.setText(scene_path)
            return True
        except (AttributeError, NameError, TypeError, RuntimeError):
            return False

    @QtCore.Slot()
    def on_select_file_path_pb_clicked(self):
        uwd = list_maya_info.get_current_file_name(full_path=True, dir_path=True)
        try:
            selected_path = mc.fileDialog2(dialogStyle=1, fileMode=3, dir=uwd)[0].encode('utf-8')
            self.file_path_le.setText(selected_path)
            return selected_path
        except IndexError:
            logging.error("Please select a directory!")
            return ""

    @QtCore.Slot(name='on_playblast_doit_clicked')
    @undoable
    def on_playblast_doit_clicked(self, artist=None, mov_name=None, mov_path=None):
        illegal_cams = ['front', 'persp', 'side', 'top']
        cam = ''
        try:
            cam = list_maya_info.get_camera(with_panel=True)
            if not mc.nodeType(cam) == 'camera':
                cam_shape = pm.PyNode(cam).getShape().name()
            else:
                cam_shape = cam
            current_panel = mc.getPanel(withFocus=1)
        except:
            pass
            # logging.error(u'请先激活视图！')
            # return (False, u'请先激活视图！')
        # 根据选中的相机来拍屏
        sel = pm.ls(sl=1) or []
        if self.cam_name_le.text():
            sel = self.cam_name_le.text()
            sel2 = sel
            if mc.nodeType(sel2) == 'transform':
                sel2 = pm.PyNode(sel2).getShape()
            if not pm.nodeType(sel2) == 'camera':
                logging.error(u"输入框输入的物体不是相机，请重新选择或者留空！")
                return
        if sel:
            sel = sel[0] if isinstance(sel, list) else sel
            try:
                sel = pm.PyNode(sel)
            except:
                pass
            if sel.nodeType() == 'transform':
                sel = sel.getShape()
            cam = sel
            cam_shape = sel
            if sel.nodeType() == 'camera':
                for each in mc.getPanel(type='modelPanel'):
                    try:
                        if mc.modelPanel(each, q=1, cam=1) in illegal_cams:
                            continue
                        if pm.PyNode(pm.modelPanel(each, q=1, cam=1)).getShape() == sel:
                            current_panel = each
                            break
                    except:
                        continue
        if cam in illegal_cams:
            if_play = mc.confirmDialog(t="warning", m="current cam is %s\n playblast anyway?" % cam, b=['Yes', 'No'])
            if if_play == "No":
                return (False, u"拍屏失败")
            pass
        if not cam:
            logging.error(u'请先激活视图！')
            return (False, u'请先激活视图！')
        mc.select(cl=1)
        playblast_info_dict = dict()
        cam_t = ''
        if pm.PyNode(cam).nodeType() == 'camera':
            cam_t = pm.PyNode(cam).getParent().name()
        playblast_info_dict['cam'] = cam_t if cam_t else cam
        print playblast_info_dict['cam']
        playblast_info_dict['focal_length'] = str(list_maya_info.get_focal_length(cam))
        playblast_info_dict['date'] = list_maya_info.get_current_date()
        playblast_info_dict['artist'] = artist or ''
        if not artist:
            artist = self.artist_le.text()
            playblast_info_dict['artist'] = artist
        playblast_info_dict['size'] = '2048*858'
        playblast_info_dict['scene_name'] = list_maya_info.get_current_file_name()
        ffmpeg_path = GLOBAL.CURRENTSCRIPTPATH+'/bin/ffmpeg.exe'
        playblast_info_dict['ffmpeg_path'] = ffmpeg_path
        if not mov_name or not mov_path:
            mov_name = self.mov_name_le.text()
            mov_path = self.file_path_le.text()
        print 'prepare...'
        if not artist or not mov_name or not mov_path:
            logging.error(u'请先填入所需的信息！')
            return (False, u'请先填入所需的信息！')
        jpg_path = mov_path + "/oct_playblast_cache_" + mov_name
        start_frame = list_maya_info.get_timeslider_time()[1]
        end_frame = list_maya_info.get_timeslider_time()[2]
        playbackSlider = mel.eval("$temp = $gPlayBackSlider")
        selected_time_range = mc.timeControl(playbackSlider, q=1, ra=1)
        if selected_time_range[1] - selected_time_range[0] > 1:
            start_frame = int(selected_time_range[0])
            end_frame = int(selected_time_range[1])
        time_duation = (end_frame - start_frame + 1.0) / 24.0
        frame = start_frame
        sound_path = "no_sound"
        try:
            soundStr = pm.PyNode(pm.timeControl(playbackSlider, q=1, sound=1, fpn=1))
            print soundStr.getAttr("filename")
            if os.path.isfile(soundStr.getAttr("filename")):
                sound_path = soundStr.getAttr("filename")
        except:
            pass
        # sound_offset = soundStr.getAttr("offset") / fps
        mov_file = mov_path + "/" + mov_name + ".mov"
        if os.path.isfile(mov_file):
            if_cast = mc.confirmDialog(t="warning", m="File:\" %s \" exists, replace it?" % mov_file, b=['Yes', 'No'])
            if if_cast == "Yes":
                try:
                    os.remove(mov_file)
                except WindowsError:
                    logging.error(u"文件正在被占用，请关闭重试！！")
                    return (False, u"文件正在被占用，请关闭重试！！")
            else:
                return False
        if os.path.isdir(jpg_path):
            shutil.rmtree(jpg_path)
        if self.draw_hud_cb.isChecked():
            try:
                mc.modelEditor(current_panel, e=True, hud=False)
                mc.setAttr(cam_shape + '.displayResolution', 0)
            except:
                pass
        while frame < (end_frame + 1):
            picture = self.capture(panel=current_panel, width=2048, height=858, percent=50,
                                           filename=jpg_path + "/" + mov_name, frame=frame,
                                           quality=100, off_screen=1, framePadding=4)
            seq = str(frame).zfill(4)
            info_dict = playblast_info_dict
            info_dict['time_code'] = list_maya_info.get_time_code(current_frame=int(mc.currentTime(q=True)),
                                                                  offset=list_maya_info.get_timeslider_time()[1]-1)
            info_dict['frame'] = str(int(mc.currentTime(q=True))) + "/" + str(list_maya_info.get_timeslider_time()[2])
            info_dict['png_path'] = picture.replace("####", "%s" % seq)
            info_dict['jpg_path'] = info_dict['png_path'].replace(".png", ".jpg")
            cmd = text_format.get_draw_text(info_dict)
            if self.draw_hud_cb.isChecked():
                subprocess.Popen(cmd, shell=True)
            frame += 1
        if self.draw_hud_cb.isChecked():
            try:
                mc.setAttr(cam_shape + '.displayResolution', 1)
                mc.setAttr(cam_shape + '.overscan', 1)
                mc.modelEditor(current_panel, e=1, hud=True)
            except:
                pass
        start_number = str(start_frame).zfill(4)
        time.sleep(0.5)
        print "Drawing HUD done.\nCompressing Video..."
        pic_format = '.jpg' if self.draw_hud_cb.isChecked() else ".png"
        self.compress_video(fps=str(24), time_duation=str(time_duation), start_number=start_number,
                            ffmpeg_path="\"" + ffmpeg_path + "\"",
                            input_path="\"" + jpg_path + "/%s" % (mov_name + ".%04d"+pic_format) + "\"",
                            output_path="\"" + mov_path + "/%s" % (mov_name + ".mov") + "\"",
                            sound="\"" + sound_path + "\"", jpg_path=jpg_path)
        return (True, u'拍屏成功!')

    @staticmethod
    def capture(panel=None, width=None, height=None, percent=100, filename=None, frame=None, form='image',
                compression='png', quality=100, clear_cache=1, off_screen=False, viewer=False, show_ornaments=True,
                overwrite=True, framePadding=4):
        return mc.playblast(editorPanelName=panel, width=width, height=height, percent=percent,
                              filename=filename, startTime=frame, endTime=frame, format=form,
                              compression=compression, quality=quality, clearCache=clear_cache,
                              offScreen=off_screen, viewer=viewer, showOrnaments=show_ornaments,
                              forceOverwrite=overwrite, framePadding=framePadding)

    @staticmethod
    def compress_video(fps, time_duation, start_number, ffmpeg_path, input_path, output_path, jpg_path, sound=None):
        if sound == "\"no_sound\"":
            compress_word = [ffmpeg_path, "-y -framerate", fps, u"-start_number", start_number, "-i", input_path,
                             "-c:v libx264 -profile:v baseline -preset:v superfast -x264opts crf=1 "
                             "-vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -pix_fmt yuv420p",
                             output_path]  # print compress_word
        else:
            compress_word = [ffmpeg_path, "-y -framerate", fps, u"-start_number", start_number, "-i", input_path, "-i",
                             sound, "-ss 0:0:0", "-t", time_duation,
                             "-c:v libx264 -profile:v baseline -preset:v superfast -x264opts crf=1 "
                             "-vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -pix_fmt yuv420p",
                             output_path]
        compress_cmd = " ".join(compress_word)
        # print compress_cmd
        subprocess.call(compress_cmd, shell=True)
        subprocess.Popen("explorer \"%s\"" % os.path.abspath(output_path.strip("\"")))
        if os.path.isdir(jpg_path):
            shutil.rmtree(jpg_path)
        return True
# "-c:v libx264 -profile:v baseline -vf \"pad=ceil(iw/2):ceil(ih/2)\" -pix_fmt yuv420p",







