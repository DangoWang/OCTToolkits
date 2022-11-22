#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dayu_widgets import dayu_theme
import datetime


def change_sg_publish_version_to_green(x, y):
    if x:
        return dayu_theme.green
    return None


def change_start_date_to_green(x, y):
    if x:
        if int(str(x).replace(' ', '').replace('-', '')) < int(str(datetime.date.today()).replace(' ', '').replace('-', '')):
            return dayu_theme.green
        return None
    return None
