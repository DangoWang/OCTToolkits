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
import ticket_main

def main():
    app = QApplication(sys.argv)
    test = ticket_main.TicketMainUI()
    # from dayu_widgets.theme import MTheme
    from dayu_widgets import dayu_theme
    # theme_temp = MTheme('light', primary_color=MTheme.orange)
    dayu_theme.apply(test)
    test.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
