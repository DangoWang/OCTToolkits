# ========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Tue Nov 06 11:55:05 2018
# ========================================
from PySide import QtCore, QtGui


# --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class TaskDelegate(QtGui.QStyledItemDelegate):
    '''
    '''
    def __init__(self, items):
        '''
        '''
        super(TaskDelegate, self).__init__()
        self.__items = items


    def createEditor(self, parent, option, index):
        '''
        '''
        combox = QtGui.QComboBox(parent)
        combox.setEditable(1)
        qcom = QtGui.QCompleter(self.__items)
        qcom.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        combox.addItems(self.__items)
        combox.setCompleter(qcom)

        return combox


    def setEditorData(self, editor, index):
        '''
        '''
        # print dir(editor)
        index_num = 0
        try:
            index_num = self.__items.index(u'{}'.format(index.data(QtCore.Qt.DisplayRole)))
        except:
            pass
        editor.setCurrentIndex(index_num)


    def setModelData(self, editor, model, index):
        '''
        '''
        value = editor.currentText()
        model.setData(index, value)