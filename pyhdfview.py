# -*- coding: utf-8 -*-
"""

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
import h5py
import _window_classes as wc
plt.style.use('bmh')


class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.filename = ''
        self.text = ''
        self.values = np.array([])
        self.current_dataset = ''
        self.file_items = []

        self.initialise_user_interface()


    def initialise_user_interface(self):
        '''
        Initialises the main window. '''

        # File structure list and dataset table
        self.file_items_list = wc.titledTree('File Tree')
        self.file_items_list.list.itemDoubleClicked.connect(self.item_double_clicked) # Add double click listener for file structure list
        self.file_items_list.list.itemExpanded.connect(self.file_items_list.swap_group_icon)
        self.file_items_list.list.itemCollapsed.connect(self.file_items_list.swap_group_icon)

        self.dataset_table = wc.titledTable('Values')

        main_content = QtGui.QHBoxLayout()
        main_content.addLayout(self.file_items_list.layout)
        main_content.addLayout(self.dataset_table.layout)

        # Make attribute table
        self.attribute_table = QtGui.QTableWidget()

        # Add 'extra' window components
        self.make_menu_bar()
        button_section = self.initialise_buttons()
        self.filename_label = QtGui.QLabel('')

        # Add the created layouts and widgets to the window
        window_layout = QtGui.QVBoxLayout()
        window_layout.addLayout(button_section)
        window_layout.addWidget(self.filename_label)
        window_layout.addLayout(main_content)
        window_layout.addWidget(self.attribute_table)
        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(window_layout)

        # Other tweaks to the window such as icons etc
        self.setWindowTitle('PyHDFView')
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))



    def initialise_buttons(self):
        '''
        Initialises the buttons in the button bar at the top of the main window. '''

        open_file_btn = QtGui.QPushButton('Open File')
        open_file_btn.clicked.connect(self.choose_file)

        self.plot_btn = QtGui.QPushButton('Plot')
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.hide()

        button_section = QtGui.QHBoxLayout()
        button_section.addWidget(open_file_btn)
        button_section.addStretch()
        button_section.addWidget(self.plot_btn)

        return button_section


    def make_menu_bar(self):
        '''
        Initialises the menu bar at the top. '''
        menubar = self.menuBar()

        # Create a File menu and add an open button
        file_menu = menubar.addMenu('&File')
        open_action = QtGui.QAction('&Open', self)
        open_action.setShortcut('Ctrl+o')
        open_action.triggered.connect(self.choose_file)
        file_menu.addAction(open_action)

        # Add an exit button to the file menu
        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)
        file_menu.addAction(exit_action)

        # Create a Help menu and add an about button
        help_menu = menubar.addMenu('&Help')
        about_action = QtGui.QAction('About PyHDFView', self)
        about_action.setStatusTip('About this program')
        about_action.triggered.connect(self.show_about_menu)
        help_menu.addAction(about_action)


    def show_about_menu(self):
        '''
        Shows the about menu by initialising an about_window object. This class is described in _window_classes.py '''
        self.about_window = wc.aboutWindow()
        self.about_window.show()


    def choose_file(self):
        '''
        Opens a QFileDialog window to allow the user to choose the hdf5 file they would like to view. '''
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home', filter='*.hdf5 *.h5')
        self.filename_label.setText(self.filename.split('/')[-1])
        self.setWindowTitle('PyHDFView - ' + self.filename)

        if len(self.filename) > 0:
            self.file_items_list.clear()
            self.dataset_table.clear()
            self.open_file()


    def open_file(self):
        '''
        Opens the chosen HDF5 file. '''
        self.hdf5_file = h5py.File(self.filename, 'r')
        self.populate_file_file_items_list()


    def find_items(self, hdf_group):
        '''
        Recursive function for all nested groups and datasets. Populates self.file_items.'''
        file_items = []
        for i in hdf_group.keys():
            file_items.append(hdf_group[i].name)
            if isinstance(hdf_group[i], h5py.Group):
                a = self.find_items(hdf_group[i])
                if len(a) >= 1:
                    file_items.append(a)

        return file_items


    def add_item_to_file_list(self, items, item_index, n):
        item_list = items[item_index]

        for i in range(len(item_list)):
            if isinstance(item_list[i], str):
                is_group = isinstance(self.hdf5_file[item_list[i]], h5py.Group)
                self.file_items_list.add_item(n, item_list[i], is_group)
            else:
                self.add_item_to_file_list(item_list, i, n+i)


    def populate_file_file_items_list(self):
        '''
        Function to populate the file structure list on the main window.
        '''
        self.file_items = []
        self.file_items_list.clear()

        # Find all of the items in this file
        file_items = self.find_items(self.hdf5_file)
        self.file_items = file_items
        #print(self.file_items)

        # Add these items to the file_items_list.
        # For clarity only the item name is shown, not the full path.
        # Arrows are used to suggest that an item is contained.
        for i in range(len(self.file_items)):
            if isinstance(self.file_items[i], str):
                is_group = isinstance(self.hdf5_file[file_items[i]], h5py.Group)
                self.file_items_list.add_item(None, self.file_items[i], is_group)
            else:
                self.add_item_to_file_list(self.file_items, i, i-1)


    def plot_graph(self):
        '''
        Plots the data that is currently shown in the dataset table. Currently opens a matplotlib figure and shows using the users current backend.'''
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

    def display_dataset(self):
        selected_row = self.file_items_list.list.currentItem()

        text = self.file_items_list.full_item_path(selected_row)

        # We first want to find out whether this is a new item
        # or if they have double clicked the same item as before.
        # If it is a new item, and that item corresponds to a dataset
        # then repopulate the table and the self.values variable.
        # Otherwise clear the table and self.values, and hide the plot button.
        if (not text == self.current_dataset) and isinstance(self.hdf5_file[text], h5py.Dataset):

            self.current_dataset = text
            self.values = self.hdf5_file[text].value

            if len(self.values) > 0: # If the dataset is not empty
                self.plot_btn.show()
                self.dataset_table.clear()

                numrows = len(self.values)
                numcols = self.dataset_table.num_cols(self.values)
                self.dataset_table.table.setRowCount(numrows)
                self.dataset_table.table.setColumnCount(numcols)

                for i in range(numrows):
                    if numcols > 1:
                        for j in range(numcols):
                            self.dataset_table.set_item(i, j, str(self.values[i,j]))
                    else:
                        self.dataset_table.set_item(0, i, str(self.values[i]))

        elif isinstance(self.hdf5_file[text], h5py.Group):
            self.current_dataset = text
            self.dataset_table.clear()
            self.values = np.array([])
            self.plot_btn.hide()


    def item_double_clicked(self):
        '''
        Responds to a double click on an item in the file_items_list.'''
        self.display_dataset()



def main():
    app = QtGui.QApplication(sys.argv)
    pyhdfview_window = mainWindow()
    pyhdfview_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
