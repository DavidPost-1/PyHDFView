# PyHDFView

Currently in alpha and should not be used for anything important. Please make appropriate backups if you intend to use this program to avoid any data loss.

Simple python application for viewing HDF5 files in a GUI. File structure can be seen in the tree view. Datasets can be viewed as a table and basic plots can be brought up in a matplotlib window.

### Latest Screenshot
![img](https://github.com/DavidPost-1/PyHDFView/blob/master/screenshots/30-08-2016.png?raw=true)

## System Requirements
- Python (3.5) - other versions untested
- HDF5

## Python Package Requirements
- numpy
- matplotlib
- h5py
- pyqt

## To-do
- Refactor the load_file functions
- When plotting load data from HDF5 file rather than keeping it in memory (self.values)
- Replace matplotlib with PyQtcharts (? maybe ?)
- Make a window icon
- Make tree and table(s) resizable
- Make attributes table stretch to fill available space
- Improve plotting functionality
    - For 2D+ data allow the user to choose the axes
    - Allow the user to choose line styles and point markers (? already can with matplotlib)
- Make double click bring up a table-window
- Add ability to rename groups and datasets from a right click menu
- Add ability to modify data in datasets from table-window
- Add ability to create new group
- Add ability to create new dataset
- Add ability to add and modify attributes

- ~~Choose some colourful icons for the tree view~~
- ~~Add a recent files menu~~
- ~~Show group and dataset attributes on single-click~~
- ~~Make items with attributes have a marker icon~~
- ~~Make tables show up in the table with a single-click~~

## Licence
This program has been distributed under the GPL 3.0+ Licence.


## Thanks
Icons - Thanks to https://www.elegantthemes.com for the GPL flat icons
