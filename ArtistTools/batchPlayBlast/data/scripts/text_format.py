#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/4/10


__author__ = "dango wang"


__doc__ = '这个是drawtext的信息'

'''
需要的信息有：
{time_code}, {frame}, {png_path}, {jpg_path}, 
{date}, {artist}, {size}, {scene_name},{ffmpeg_path}, {cam}, {focal_length}
'''

drawing_text = '{ffmpeg_path} -y -i {png_path} -vf ' \
               'drawtext=fontfile=simhei.ttf:text="{time_code}"' \
               ':x=927.415308642:y=410.428571429:fontsize=14:fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="TimeCode:":x=836.39308642:y=410.428571429:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{focal_length}":' \
               'x=590.380246914:y=410.428571429:fontsize=14:fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="FocalLength:":x=461.432098765:y=410.428571429:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{date}":x=120.857283951:y=410.428571429:' \
               'fontsize=14:fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="Date:":x=17.1930864198:y=410.428571429:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{frame}":x=927.415308642:y=393.228076099:fontsize=14:' \
               'fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="Frame:":x=836.39308642:y=393.228076099:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{cam}":x=590.380246914:y=393.228076099:fontsize=14:' \
               'fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="Cam:":x=461.432098765:y=393.228076099:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{artist}":x=120.857283951:y=393.228076099:' \
               'fontsize=14:fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="Artist:":x=17.1930864198:y=393.228076099:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{size}":x=590.380246914:y=7.24285714286:fontsize=14:' \
               'fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="Size:":x=461.432098765:y=7.24285714286:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="{scene_name}":x=120.857283951:y=7.24285714286:fontsize=14:' \
               'fontcolor=ffff00@1.0:box=True:boxcolor=1e1e1e@0.6,' \
               'drawtext=fontfile=simhei.ttf:text="SceneName:":x=17.1930864198:y=7.24285714286:fontsize=14:' \
               'fontcolor=55ffff@1.0:box=True:boxcolor=1e1e1e@0.6 {jpg_path}'


def get_draw_text(draw_info_dict):
    return drawing_text.format(**draw_info_dict)
