# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 15:54:26 2016

@author: Dave
"""

import numpy as np
import h5py
from PyQt4 import QtCore, QtGui

class aboutWindow(QtGui.QMessageBox):
    def __init__(self, parent=None):
        super(aboutWindow, self).__init__(parent)
        self.setWindowTitle('About PyHDFView')
        self.setText('''
PyHDFView is a work in progress.

For comments, issues etc contact me at davidpost-1@outlook.com.

I am not responsible for any issues that may arise from the use of this code, including any loss of data etc.
        ''')


class titledTree():
    def __init__(self, title):
        self.list = QtGui.QTreeWidget()
        self.title = QtGui.QLabel(title)
        #self.list.setHeaderLabel(str(title))
        self.list.header().close()

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list)

        self.row_list = []
        self.group_list = []
        self.has_attrs_list = []

        self.icon_closed_group = QtGui.QIcon('images/closed_group.svg')
        self.icon_open_group = QtGui.QIcon('images/open_group.svg')
        self.icon_closed_group_with_attrs = QtGui.QIcon('images/closed_group_with_attrs.svg')
        self.icon_open_group_with_attrs = QtGui.QIcon('images/open_group_with_attrs.svg')

        self.icon_dataset = QtGui.QIcon('images/dataset.svg')
        self.icon_dataset_with_attrs = QtGui.QIcon('images/dataset_with_attrs.svg')


    def clear(self):
        self.row_list = []
        self.group_list = []
        self.has_attrs_list = []
        self.list.clear()


    def add_item(self, parent_index, item, hdf5_file):
        is_group = isinstance(hdf5_file[item], h5py.Group)
        self.group_list.append(is_group)


        has_attrs = len(list(hdf5_file[item].attrs.keys())) > 0
        self.has_attrs_list.append(has_attrs)


        if parent_index == None:
            self.row_list.append(QtGui.QTreeWidgetItem(self.list))

        else:
            self.row_list.append(QtGui.QTreeWidgetItem(self.row_list[parent_index]))

        # Which icon shall we set.
        if is_group == True:
            if has_attrs:
                self.row_list[-1].setIcon(0, self.icon_closed_group_with_attrs)
            else:
                self.row_list[-1].setIcon(0, self.icon_closed_group)
        else:
            if has_attrs:
                self.row_list[-1].setIcon(0, self.icon_dataset_with_attrs)
            else:
                self.row_list[-1].setIcon(0, self.icon_dataset)

        item_text = item.split('/')[-1]
        self.row_list[-1].setText(0, item_text)


    def full_item_path(self, selected_row):
        text = selected_row.text(0)
        parent_row = selected_row.parent()

        while not parent_row == None:
            text = parent_row.text(0) + '/' + text
            parent_row = parent_row.parent()

        return text


    def swap_group_icon(self):
        for i in range(len(self.row_list)):
            if self.row_list[i].isExpanded():
                if self.has_attrs_list[i]:
                        self.row_list[i].setIcon(0, self.icon_open_group_with_attrs)
                else:
                    self.row_list[i].setIcon(0, self.icon_open_group)

            elif self.group_list[i] == True:
                if self.has_attrs_list[i]:
                    self.row_list[i].setIcon(0, self.icon_closed_group_with_attrs)
                else:
                    self.row_list[i].setIcon(0, self.icon_closed_group)
                #self.row_list[i].setIcon(0, self.closed_group_icon)


class titledTable():
    def __init__(self, title):
        self.title = QtGui.QLabel(title)
        self.table = QtGui.QTableWidget()
        self.table.setShowGrid(True)

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.table)


    def clear(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()


    def set_item(self, row, col, item):
        if isinstance(item, str):
            self.table.setItem(row, col, QtGui.QTableWidgetItem(item))
        else:
            print("Type Error: Item must be a str")


    def num_cols(self, values):
        value_shape = np.shape(values)
        numcols = 1

        if len(value_shape) > 1:
            numcols = value_shape[1]

        return numcols
