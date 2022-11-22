#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Sun Dec 29 16:30:20 2019
#========================================
import nuke
try:
    from PySide2 import QtWidgets, QtGui, QtCore
    import aov_qt5_widgets as aov_widgets
except ImportError:
    from PySide import QtGui, QtCore
    QtWidgets = QtGui
    import aov_qt4_widgets as aov_widgets

import aov_core
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
def get_nuke_window():
    app = QtWidgets.QApplication.instance()

    for widget in app.topLevelWidgets():
        if widget.metaObject().className() == 'Foundry::UI::DockMainWindow':
            return widget



class AovWindow(QtWidgets.QMainWindow, aov_widgets.Ui_MainWindow):
    '''
    '''
    def __init__(self, parent=get_nuke_window()):
        '''
        '''
        super(AovWindow, self).__init__(parent)
        self.setupUi(self)

        #-
        self.aov_data  = dict()
        self.read_node = None



    @QtCore.Slot(bool)
    def on_btn_refresh_clicked(self, args=None):
        '''
        '''
        self.read_node = nuke.selectedNode()
        self.aov_data  = aov_core.get_layer_data(self.read_node)

        self.listWidget.clear()
        self.listWidget.addItems(sorted(self.aov_data.keys()))




    @QtCore.Slot(bool)
    def on_btn_CreateNetwok_clicked(self, args=None):
        '''
        '''
        selected_keys = list()
        selected_data = dict()
        for item in self.listWidget.selectedItems():
            selected_keys.append(item.text())
            selected_data.setdefault(item.text(), self.aov_data[item.text()])
        aov_core.create_aov_network(self.read_node, selected_keys, selected_data, self.comboBox.currentIndex())
