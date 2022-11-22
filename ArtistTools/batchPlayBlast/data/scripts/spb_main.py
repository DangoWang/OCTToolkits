#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/10


__author__ = "dango wang"

import re
import os
import sys
import time
import logging
import shutil
import subprocess
import getpass
import maya.cmds as mc
import maya.cmds as cmds
import text_format
import maya.mel as mel
import pymel.core as pm

reload(text_format)
try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    import PySide.QtGui as QtWidgets
    from PySide import QtCore

# necessary global param
file_path = str(os.path.split(os.path.realpath(__file__))[0])
# ffmpeg_exe_path = os.path.dirname(__file__) + "/bin/ffmpeg.exe"


def set_rnd_attr():
    cams = pm.ls(type='camera')
    default_cams = ['perspShape', 'sideShape', 'topShape', 'frontShape', 'backShape', 'bottomShape', 'leftShape']
    usefull_cams = [cam for cam in cams if cam.name() not in default_cams]
    final_cam = usefull_cams[0]
    for each in usefull_cams:
        if not len(re.findall('\d+', each.name())) < 2:
            final_cam = each
    for c in cams:
        pm.setAttr(c.rnd, 0)
    pm.setAttr(final_cam.rnd, 1)
    playblast_win = cmds.window()
    layout_temp = cmds.paneLayout()
    cam_panel = cmds.modelPanel(parent=layout_temp)
    cmds.modelEditor(cam_panel, e=True, allObjects=True, nurbsCurves=False, deformers=False, joints=False, dim=False, lc=False, 
                     hud=False, displayAppearance="smoothShaded", displayTextures=True, camera=final_cam.name())
    cmds.showWindow(playblast_win)
    return final_cam.name(), cam_panel


def get_current_file_name():
    import maya.OpenMaya as om
    return om.MFileIO().currentFile()


def get_focal_length(camera_name):
    return int(mc.getAttr(camera_name+".focalLength"))


def get_current_date():
    weekDayDict = {1: u'Mon', 2: u'Tue', 3: u'Wed', 4: u'Thu', 5: u'Fri', 6: u'Sat', 0: u'Sun'}
    localTime = time.localtime()
    dayForMat = '%Y/%m/%d'
    dayValue = time.strftime(dayForMat, localTime)
    weekForMat = '%w'
    weekValue = str(time.strftime(weekForMat, localTime))
    timeForMat = '%H:%M'
    timeValue = time.strftime(timeForMat, localTime)
    timeString = dayValue + " " + weekDayDict[int(weekValue)] + " " + timeValue.replace(":", "`")
    return timeString


def get_timeslider_time():
    return [int(pm.playbackOptions(ast=True, query=True)),int(pm.playbackOptions(min=True, query=True)),\
    int(pm.playbackOptions(max=True, query=True)),int(pm.playbackOptions(aet=True, query=True))]


def get_time_code(current_frame, offset=0):
    current_frame2 = current_frame - offset
    data = divmod(current_frame2, 24)
    return str(int(data[0])) + "s" + str(int(data[1])) + "f"


class DsfSimplePlayBlast(object):
    def __init__(self, exe_file_path):
        super(DsfSimplePlayBlast, self).__init__()
        self.ffmpeg_path = exe_file_path+"ffmpeg.exe"

    def play_blast(self, artist, mov_name, mov_path):
        mov_name += '_pv'
        cam, cam_panel = set_rnd_attr()
        self.cam_panel = cam_panel
        playblast_info_dict = dict()
        cam_t = ''
        if pm.PyNode(cam).nodeType() == 'camera':
            cam_t = pm.PyNode(cam).getParent().name()
        playblast_info_dict['cam'] = cam_t if cam_t else cam
        playblast_info_dict['focal_length'] = str(get_focal_length(cam))
        playblast_info_dict['date'] = get_current_date()
        playblast_info_dict['artist'] = artist or ''
        playblast_info_dict['size'] = '2048*858'
        playblast_info_dict['scene_name'] = get_current_file_name().split('/')[-1].split('.')[0]
        playblast_info_dict['ffmpeg_path'] = self.ffmpeg_path
        jpg_path = mov_path + "/oct_playblast_cache_" + mov_name
        start_frame = get_timeslider_time()[1]
        end_frame = get_timeslider_time()[2]
        playbackSlider = mel.eval("$temp = $gPlayBackSlider")
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
            try:
                os.remove(mov_file)
            except WindowsError:
                return
        if os.path.isdir(jpg_path):
            try:
                shutil.rmtree(jpg_path)
            except WindowsError:
                return
        while frame < (end_frame + 1):
            picture = self.capture(width=2048, height=858, percent=50,
                                           filename=jpg_path + "/" + mov_name, frame=frame,
                                           quality=100, off_screen=1, framePadding=4)
            # print picture
            seq = str(frame).zfill(4)
            info_dict = playblast_info_dict
            info_dict['time_code'] = get_time_code(current_frame=int(mc.currentTime(q=True)),
                                                                  offset=get_timeslider_time()[1]-1)
            info_dict['frame'] = str(int(mc.currentTime(q=True))) + "/" + str(get_timeslider_time()[2])
            info_dict['png_path'] = picture.replace("####", "%s" % seq)
            info_dict['jpg_path'] = info_dict['png_path'].replace(".png", ".jpg")
            # print info_dict['png_path']
            cmd = text_format.get_draw_text(info_dict)
            subprocess.Popen(cmd, shell=True)
            frame += 1
        start_number = str(start_frame).zfill(4)
        time.sleep(0.5)
        print "Drawing HUD done.\nCompressing Video..."
        pic_format = '.jpg'
        self.compress_video(fps=str(24), time_duation=str(time_duation), start_number=start_number,
                            ffmpeg_path="\"" + self.ffmpeg_path + "\"",
                            input_path="\"" + jpg_path + "/%s" % (mov_name + ".%04d"+pic_format) + "\"",
                            output_path="\"" + mov_path + "/%s" % (mov_name + ".mov") + "\"",
                            sound="\"" + sound_path + "\"", jpg_path=jpg_path)
        return

    def capture(self, width=None, height=None, percent=100, filename=None, frame=None, form='image',
                compression='png', quality=100, clear_cache=1, off_screen=False, viewer=False, show_ornaments=True,
                overwrite=True, framePadding=4):
        # print "-----------------------",width,height,percent,filename,frame,form,compression,quality,clear_cache,off_screen,viewer,show_ornaments,overwrite,framePadding
        return mc.playblast(editorPanelName=self.cam_panel, width=width, height=height, percent=percent,
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

