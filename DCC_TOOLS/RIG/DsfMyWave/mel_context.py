#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/6/17


add_attr = "addAttr -ln \"tx_amplitude\" -at double -min 0 -max 100 -dv 3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.tx_amplitude;" \
           "addAttr -ln \"ty_amplitude\" -at double -min 0 -max 100 -dv 3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.ty_amplitude;" \
           "addAttr -ln \"tz_amplitude\" -at double -min 0 -max 100 -dv 3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.tz_amplitude;" \
           "addAttr -ln \"t_frequency\" -at double -min 0.001 -max 1 -dv 0.1 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.t_frequency;" \
           "addAttr -ln \"sx_amplitude\" -at double -min 0 -max 100 -dv 0.3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.sx_amplitude;" \
           "addAttr -ln \"sy_amplitude\" -at double -min 0 -max 100 -dv 0.3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.sy_amplitude;" \
           "addAttr -ln \"sz_amplitude\" -at double -min 0 -max 100 -dv 0.3 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.sz_amplitude;" \
           "addAttr -ln \"s_frequency\" -at double -min 0.001 -max 1 -dv 0.1 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.s_frequency;" \
           "addAttr -ln \"s_min\" -at double -min 0 -max 10 -dv 1 {ctrl};" \
           "setAttr -e -keyable true {ctrl}.s_min;"
blink_attr = 'select -r {ctrl};addAttr -ln "random_blink"  -at bool  "{ctrl}";'\
             'setAttr -e -keyable true {ctrl}.random_blink;'\
             'addAttr -ln "random_blink_speed"  -at long  -min 0 -dv 8 "{ctrl}";'\
             'setAttr -e -keyable true {ctrl}.random_blink_speed;'\
             'addAttr -ln "random_blink_offset"  -at long  -min 0 -dv 0 "{ctrl}";'\
             'setAttr -e -keyable true {ctrl}.random_blink_offset;'\
             'addAttr -ln "random_blink_interval"  -at long  -min 0 -dv 2 "{ctrl}";'\
             'setAttr -e -keyable true {ctrl}.random_blink_interval;'


def get_mel_text(ctrl):
    return add_attr.format(**ctrl)

