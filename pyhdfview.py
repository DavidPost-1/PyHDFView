# -*- coding: utf-8 -*-
"""

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
import functools as ft
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
        self.recent_files_path = 'recent_files.txt'

        self.initialise_user_interface()

    def _ctx_menu_cb(self, pos):
        print("pos:", pos)

        row = self.file_items_list.list.currentItem()
        print(self.file_items_list.full_item_path(row))

    def initialise_user_interface(self):
        '''
        Initialises the main window. '''
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)


        # File structure list and dataset table
        self.file_items_list = wc.titledTree('File Tree')
        self.file_items_list.list.itemClicked.connect(self.item_clicked)
        self.file_items_list.list.itemExpanded.connect(self.file_items_list.swap_group_icon)
        self.file_items_list.list.itemCollapsed.connect(self.file_items_list.swap_group_icon)

        # Context menu
        self.file_items_list.list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.file_items_list.list.customContextMenuRequested.connect(self._ctx_menu_cb)


        # Make dataset table
        self.dataset_table = wc.titledTable('Values')

        # Make attribute table
        self.attribute_table = QtGui.QTableWidget()
        self.attribute_table.setShowGrid(True)

        # Initialise all buttons
        self.general_buttons = self.initialise_general_buttons()
        self.dataset_buttons = self.initialise_dataset_buttons()

        # Add 'extra' window components
        self.make_menu_bar()
        self.load_recent_files_list()
        self.filename_label = QtGui.QLabel('')

        # Add the created layouts and widgets to the window
        grid.addLayout(self.general_buttons, 1, 0)
        grid.addLayout(self.dataset_buttons, 1, 1)
        grid.addWidget(self.filename_label, 2, 0)
        grid.addLayout(self.file_items_list.layout, 3, 0)
        grid.addLayout(self.dataset_table.layout, 3, 1)
        grid.addWidget(self.attribute_table, 4, 0, 1, 2)

        self.setCentralWidget(QtGui.QWidget(self))
        self.centralWidget().setLayout(grid)

        # Other tweaks to the window such as icons etc
        self.setWindowTitle('PyHDFView')
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))



    def initialise_general_buttons(self):
        '''
        Initialises the buttons in the button bar at the top of the main window. '''
        open_file_btn = QtGui.QPushButton('Open')
        open_file_btn.clicked.connect(self.choose_file)

        button_section = QtGui.QHBoxLayout()
        button_section.addWidget(open_file_btn)
        button_section.addStretch(0)

        return button_section


    def initialise_dataset_buttons(self):
        self.plot_btn = QtGui.QPushButton('Plot')
        self.plot_btn.clicked.connect(self.plot_graph)
        self.plot_btn.hide()

        button_section = QtGui.QHBoxLayout()
        button_section.addWidget(self.plot_btn)
        button_section.addStretch()
        return button_section


    def make_menu_bar(self):
        '''
        Initialises the menu bar at the top. '''
        menubar = self.menuBar()


        # Create a File menu and add an open button
        self.file_menu = menubar.addMenu('&File')
        open_action = QtGui.QAction('&Open', self)
        open_action.setShortcut('Ctrl+o')
        open_action.triggered.connect(self.choose_file)
        self.file_menu.addAction(open_action)

        # Add the recent files menu, but don't populate it yet
        self.recent_files_menu = self.file_menu.addMenu('&Recent Files')

        # Add an exit button to the file menu
        exit_action = QtGui.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)
        self.file_menu.addAction(exit_action)

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


    def load_recent_files_list(self):
        '''
        Reads recent files from the recent_files.txt file and adds items to the
        Recent Files menu.
        '''
        lines = []

        # Open the recent_files file and load in the filename
        with open(self.recent_files_path, 'r') as rf:
            for i in rf:
                if not (i == '\n' or i == '\r' or i =='\r\n'):
                    item = i.replace('\r', '')
                    item = item.replace('\n', '')
                    lines.append(item)

        self.recent_files_list = []
        for i in range(len(lines)):
            # make a new menu item
            self.recent_files_list.append(QtGui.QAction(lines[i], self))
            self.recent_files_list[i].triggered.connect(ft.partial(self.open_recent_file, lines[i]))

            # add it to the menu
            self.recent_files_menu.addAction(self.recent_files_list[i])


    def recent_files_reset(self):
        '''
        When a user opens a new file we have to reset the recent files list
        in the menu, and also update the recent files file.
        '''
        self.recent_files_menu.clear()

        in_position = -1
        lines = []
        filename_str = self.filename+'\n'

        # Open the recent_files file and load in the filename
        with open(self.recent_files_path, 'r') as rf:
            for i in rf:
                if not (i == '\n' or i == '\r' or i =='\r\n'):
                    item = i.replace('\r', '')
                    item = item.replace('\n', '')
                    lines.append(item)

        num_appearances = lines.count(self.filename)
        if num_appearances > 0:
            for i in range(num_appearances):
                in_position = lines.index(self.filename)
                lines.pop(in_position)

        # Insert the current filename the first item in the list
        lines.insert(0, self.filename)

        self.write_recent_files_file(lines)
        self.load_recent_files_list()


    def open_recent_file(self, filename):
        '''
        Function to run when a recent file is clicked
        '''
        self.initiate_file_open(filename)


    def write_recent_files_file(self, lines):
        '''
        Function to write the recent files list to recent_files.txt
        just writes lines to a file up to a max number
        '''
        max_recent_files = 5
        with open(self.recent_files_path, 'w') as rf:
            for i in lines[0:max_recent_files]:
                rf.write(i+'\n')


    def choose_file(self):
        '''
        Opens a QFileDialog window to allow the user to choose the hdf5 file they would like to view. '''
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                '/home', filter='*.hdf5 *.h5')
        self.initiate_file_open(filename)


    def initiate_file_open(self, filename):
            old_filename = self.filename
            self.filename = filename

            try:
                self.open_file(filename)
                self.recent_files_reset()
                self.clear_file_items()
                self.dataset_table.clear()
                self.populate_file_file_items_list()

                self.filename_label.setText(filename.split('/')[-1])
                self.setWindowTitle('PyHDFView - ' + filename)
            except:
                self.recent_files_reset()
                self.clear_file_items()
                self.dataset_table.clear()
                self.filename = '' # if it didn't work keep the old value
                print("Error opening file")



    def open_file(self, filename):
        '''
        Opens the chosen HDF5 file. '''
        self.hdf5_file = h5py.File(filename, 'r')


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


    def clear_file_items(self):
        self.file_items = []
        self.file_items_list.clear()


    def add_item_to_file_list(self, items, item_index, n):
        item_list = items[item_index]

        for i in range(len(item_list)):
            if isinstance(item_list[i], str):
                self.file_items_list.add_item(n, item_list[i], self.hdf5_file)
            else:
                self.add_item_to_file_list(item_list, i, n+i)


    def populate_file_file_items_list(self):
        '''
        Function to populate the file structure list on the main window.
        '''
        # Find all of the items in this file
        file_items = self.find_items(self.hdf5_file)
        self.file_items = file_items

        # Add these items to the file_items_list.
        # For clarity only the item name is shown, not the full path.
        # Arrows are used to suggest that an item is contained.
        for i in range(len(self.file_items)):
            if isinstance(self.file_items[i], str):
                self.file_items_list.add_item(None, self.file_items[i], self.hdf5_file)
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
                        self.dataset_table.set_item(i, 0, str(self.values[i]))

        elif isinstance(self.hdf5_file[text], h5py.Group):
            self.current_dataset = text
            self.dataset_table.clear()
            self.values = np.array([])
            self.plot_btn.hide()


    def display_attributes(self):
        # reset the value
        self.attribute_table.clear()

        # Find the path of the selected item and extract attrs
        selected_row = self.file_items_list.list.currentItem()
        path = self.file_items_list.full_item_path(selected_row)
        attributes = list(self.hdf5_file[path].attrs.items())
        num_attributes = len(attributes)

        # Prepare the table by setting the appropriate row number
        self.attribute_table.setRowCount(num_attributes)
        self.attribute_table.setColumnCount(0)
        if num_attributes > 0:
            self.attribute_table.setColumnCount(2)

        # Populate the table
        for i in range(num_attributes):
            self.attribute_table.setItem(i, 0, QtGui.QTableWidgetItem(attributes[i][0]))
            value = attributes[i][1]

            # h5py gives strings come as encoded numpy arrays,
            # extract if necessary.
            if isinstance(value, np.ndarray):
                self.attribute_table.setItem(i, 1, QtGui.QTableWidgetItem(str(value[0].decode())))
            else:
                self.attribute_table.setItem(i, 1, QtGui.QTableWidgetItem(str(value)))



    def item_double_clicked(self):
        '''
        Responds to a double click on an item in the file_items_list.'''
        # self.display_dataset()


    def item_clicked(self):
        self.display_attributes()
        self.display_dataset()


def main():
    app = QtGui.QApplication(sys.argv)
    pyhdfview_window = mainWindow()
    pyhdfview_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
