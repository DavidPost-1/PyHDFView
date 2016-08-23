# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 15:54:26 2016

@author: Dave
"""

import numpy as np
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


class titledList():
    def __init__(self, title):
        self.title = QtGui.QLabel(title)
        self.list = QtGui.QTreeWidget()
        self.list.setMaximumWidth(300)
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list)
        
    
    def clear(self):
        self.list.clear()
        
    
    def add_item(self, item):
        if isinstance(item, str):
            row = QtGui.QTreeWidgetItem(self.list)
            row.setText(0, item)
            #self.list.addItem(item)
        else:
            print("Type Error: Only strings can be added to lists.")

        
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
