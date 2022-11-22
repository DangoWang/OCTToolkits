#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: huangna
# Date  : 2019.9
###################################################################
import os
import sys
sys.path.append(os.environ['oct_toolkits_path'])
sys.path.append(os.environ['oct_tooltikts_thirdparty'])
sys.path.append(os.environ['utils_path'])
from config.GLOBAL import *
from dayu_widgets.qt import *
from ArtistTools.change_tex_size import change_tex_size


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = change_tex_size.ChangeTexSize()
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    test.show_log()
    sys.exit(app.exec_())
