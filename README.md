# PyHDFView

Currently in BETA and should not be used for anything important. Please make appropriate backups if you intend to use this program to avoid any data loss.

Simple python application for viewing HDF5 files in a GUI. File structure can be seen in the tree view. Datasets can be viewed as a table and basic plots can be brought up in a matplotlib window.

## System Requirements
- Python (3.5) - other versions untested
- HDF5


## Python Package Requirements
- numpy
- matplotlib
- h5py
- pyqt


## To-do
- Show group and dataset attributes on single-click
- Replace QTable with vtable
- Replace matplotlib with PyQtcharts
- Choose some colourful icons for the tree view
- Make a window icon
- Make tree and table resizable
- Improve plotting functionality
    - For 2D+ data allow the user to choose the axes
    - Allow the user to choose line styles and point markers
- Make tables show up in the table with a single-click
- Make double click bring up a table-window
- Add ability to rename groups and datasets from a right click menu
- Add ability to modify data in datasets from table-window
- Add ability to create new group
- Add ability to create new dataset
