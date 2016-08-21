# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 15:54:26 2016

@author: Dave
"""

import numpy as np
from PyQt4 import QtCore, QtGui

class about_window(QtGui.QMessageBox):
    def __init__(self, parent=None):
        super(about_window, self).__init__(parent)
        self.setWindowTitle('About PyHDFView')    
        self.setText('''
PyHDFView is a work in progress.
        
For comments, issues etc contact me at davidpost-1@outlook.com.
        
I am not responsible for any issues that may arise from the use of this code, including any loss of data etc.
        ''')


class titled_list():
    def __init__(self, title):
        self.title = QtGui.QLabel(title)
        self.list = QtGui.QListWidget()
        self.list.setMaximumWidth(300)
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.list)
        
    
    def clear(self):
        self.list.clear()
        
    
    def addItem(self, item):
        if isinstance(item, str):
            self.list.addItem(item)
        else:
            print("Type Error: Only strings can be added to lists.")

        
class dataset_table():
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
    
        
    def setItem(self, row, col, item):
        if isinstance(item, str):
            self.table.setItem(row, col, QtGui.QTableWidgetItem(item))
        else:
            print("Type Error: Item must be a str")
    
            
    def numCols(self, values):
        value_shape = np.shape(values)
        numcols = 1
        
        if len(value_shape) > 1:
            numcols = value_shape[1]
        
        return numcols
