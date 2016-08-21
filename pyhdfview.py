# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

test test test
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
import h5py
import _window_classes as wc
plt.style.use('bmh')


class main_window(QtGui.QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.filename = ''
        self.initui()
        self.text = ''
        self.values = np.array([])
        self.current_selection = ''
    
        
    def initui(self):
        self.make_menu_bar()
        
        window_layout = QtGui.QVBoxLayout()
        
        # Button Section
        button_section = self.initialise_buttons()
        
        # Window title bit
        self.filename_label = QtGui.QLabel('')
        
        # Main Window
        hbox = QtGui.QHBoxLayout()
        self.group_list = wc.titled_list('File Tree (* - Dataset)')
        self.group_list.list.itemDoubleClicked.connect(self.ItemDoubleClicked)
        
        self.dataset_tab = wc.dataset_table('Values')
        hbox.addLayout(self.group_list.layout)
        hbox.addLayout(self.dataset_tab.layout)
        
        # Bottom Section
        self.lbl = QtGui.QLabel(self)
        self.lbl.hide()
        
        window_layout.addLayout(button_section)
        window_layout.addWidget(self.filename_label)
        window_layout.addLayout(hbox)
        window_layout.addWidget(self.lbl)
        
        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(window_layout)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        self.setWindowTitle('PyHDFView')
    
        
    def initialise_buttons(self):
        button_section = QtGui.QHBoxLayout()        
        
        open_file_btn = QtGui.QPushButton('Open File')
        open_file_btn.clicked.connect(self.choose_file)
        button_section.addWidget(open_file_btn)
        
        button_section.addStretch()    
        
        self.plot_btn = QtGui.QPushButton('Plot')
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.hide()
        button_section.addWidget(self.plot_btn)
        
        return button_section
    
    
    def make_menu_bar(self):
        openAction = QtGui.QAction('&Open', self)
        openAction.setShortcut('Ctrl+o')
        openAction.triggered.connect(self.choose_file)
        
        exitAction = QtGui.QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        aboutAction = QtGui.QAction('About PyHDFView    ', self)
        aboutAction.setStatusTip('About this program')
        aboutAction.triggered.connect(self.show_about_menu)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)
             
        
    def show_about_menu(self):
        self.about_menu = wc.about_window()
        self.about_menu.show()
    
    
    def choose_file(self):       
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home', filter='*.hdf5 *.h5')
        self.filename = fname
        self.filename_label.setText(fname.split('/')[-1])
        self.setWindowTitle('PyHDFView - ' + self.filename)
        if len(fname) > 0:
            self.group_list.clear()
            self.dataset_tab.clear()
            self.populate_groups()
            
            
    def plot_graph(self):
        plt.ion()
        plt.close('all')
        if len(self.values) > 0:
            if len(np.shape(self.values)) > 1:
                plt.figure()
                for i in range(len(self.values)):
                    plt.plot(self.values[i], '-o', label=str(i))
                
                plt.legend(loc=0)
                plt.show()
                
            else:
                plt.figure()
                plt.plot(self.values, '-o')
                plt.show()
        
        
    def ItemDoubleClicked(self):
        selected_row = self.group_list.list.currentRow()
        text = str(self.groups[int(selected_row)])
        
        if (not text == self.current_selection) and isinstance(self.hdf5_file[text], h5py.Dataset):
            self.current_selection = text
            self.values = self.hdf5_file[text].value
               
            if len(self.values) > 0:
                self.plot_btn.show()
                
                self.dataset_tab.clear()
                numrows = len(self.values)                    
                numcols = self.dataset_tab.numCols(self.values)
                self.dataset_tab.table.setRowCount(numrows)
                self.dataset_tab.table.setColumnCount(numcols)
                
                for i in range(numrows):
                    if numcols > 1:
                        for j in range(numcols):
                            self.dataset_tab.setItem(i, j, str(self.values[i,j]))
                    else:
                        self.dataset_tab.setItem(0, i, str(self.values[i]))
        else:
            self.dataset_tab.clear()
            self.values = np.array([])
            self.plot_btn.hide()

                
    def find_items(self, item):
        for i in item.keys():
            self.groups.append(item[i].name)
            if isinstance(item[i], h5py.Group):
                self.find_items(item[i])
                
                
    def populate_groups(self):
        self.groups = []
        self.group_list.clear()
        
        self.hdf5_file = h5py.File(self.filename, 'r')
        self.find_items(self.hdf5_file)

        for i in self.groups:
            num_intents = (i.count('/')-1) * ' -> '
            group_name = i.split('/')[-1]
            text = num_intents + group_name
            if isinstance(self.hdf5_file[i], h5py.Dataset):
                text = num_intents + ' * ' + group_name
                
            self.group_list.list.addItem(text)
        

def main():
    app = QtGui.QApplication(sys.argv)
    w = main_window()
    w.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    main()