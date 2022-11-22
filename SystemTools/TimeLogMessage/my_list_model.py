# -*- coding: utf-8 -*-
#========================================
#    author: Changlong.Zang
#      mail: zclongpop123@163.com
#      time: Thu Dec 19 16:21:22 2019
#========================================
import datetime
from PySide import QtGui
from PySide import QtCore
#--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class TableModel(QtCore.QAbstractTableModel):
    '''
    '''
    HEAD_DATA = [u'类型', u'任务', u'时间', u'时长(小时:)', u'描述']


    def __init__(self, parent=None, data=None):
        '''
        '''
        super(TableModel, self).__init__(parent)
        self.__data = data or list()



    def rowCount(self, index=QtCore.QModelIndex()):
        '''
        '''
        return len(self.__data)



    def columnCount(self, index=QtCore.QModelIndex()):
        '''
        '''
        return 5



    def data(self, index=QtCore.QModelIndex(), role=QtCore.Qt.DisplayRole):
        '''
        '''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 2 and self.__data[index.row()][index.column()]:
                return self.__data[index.row()][index.column()].strftime('%Y-%m-%d %H:%M:%S')
            else:
                return self.__data[index.row()][index.column()]

        # if role == QtCore.Qt.ForegroundRole:
        #     return QtGui.QColor(255,0,0)



    def headerData(self, sec, oritation, role):
        '''
        '''
        if role == QtCore.Qt.DisplayRole:
            if oritation == QtCore.Qt.Horizontal:
                return self.HEAD_DATA[sec]
            else:
                return sec + 1


    def flags(self, index=QtCore.QModelIndex()):
        '''
        '''
        current_flags = super(TableModel, self).flags(index)
        if index.column() == 2:
            return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
        return current_flags | QtCore.Qt.ItemIsEditable


    def setData(self, index=QtCore.QModelIndex(), value='', role=QtCore.Qt.EditRole):
        '''
        '''
        if role == QtCore.Qt.EditRole:
            if index.column() == 0:
                self.__data[index.row()][index.column()] = u'{0}'.format(value)
            if index.column() == 1:
                self.__data[index.row()][index.column()] = str(value)
            
            
            if index.column() == 3:
                self.__data[index.row()][index.column()] = float(value)
            if index.column() == 4:
                self.__data[index.row()][index.column()] = u'{}'.format(value)
                
            self.dataChanged.emit(index, index)
            return True

    def insertRow(self, row, value, index=QtCore.QModelIndex()):
        self.beginInsertRows(index, row, row)
        self.__data.insert(row, value)
        self.endInsertRows()

    def removeRow(self, row, index=QtCore.QModelIndex()):
        self.beginRemoveRows(index, row, row)
        self.__data.pop(row)
        self.endRemoveRows()

    def clearRow(self):
        while self.rowCount():
            self.removeRow(self.rowCount()-1)

    def setMyData(self, data_list):
        self.clearRow()
        for i, data in enumerate(data_list):
            entity_name = None
            # if data["entity"]:
            try:
                entity_name = data["entity.Task.entity"]# ["name"]
                # print entity_name
            except:
                pass
            self.insertRow(i, [data["sg_type"], entity_name, data["created_at"], data["duration"], data["description"]])
