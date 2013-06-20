
from PySide import QtGui, QtCore
from os import getcwd
from widgets.mlistwidget import ListWidget

class ModelIndex(QtCore.QModelIndex):
    def __init__(self):
        QtCore.QModelIndex.__init__(self)

class FileSystemModel(QtGui.QFileSystemModel):
    def __init__(self):
        QtGui.QFileSystemModel.__init__(self)
        self.test_model_index = ModelIndex()
        self.beginInsertColumns(self.test_model_index,4,4)
        self.insertColumn(4)

class FileTreeWidget(QtGui.QWidget):
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.settings = settings
        self.setup_model()
        self.setup_ui()

    def setup_ui(self):
        layout = QtGui.QGridLayout(self)
        self.setLayout(layout)
        self.tree_view = QtGui.QTreeView(self)
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(getcwd()))
        self.tree_view.doubleClicked.connect(self.item_double_clicked)
        layout.addWidget(self.tree_view,0,0)

    def setup_model(self):
        self.file_system_model = FileSystemModel()
        self.file_system_model.setRootPath("")
        self.file_system_model.dataChanged.connect(self.data_changed)

    def update_columns(self, top_left, bottom_right):
        current_column = top_left.column()
        last_column = bottom_right.column()
        while(current_column < last_column):
            self.tree_view.resizeColumnToContents(current_column)
            current_column+=1

    @QtCore.Slot(QtCore.QModelIndex)
    def item_double_clicked(self, index):
        if not self.file_system_model.isDir(index):
            path = self.file_system_model.fileName(index)
            self.settings.file_path_double_clicked(path)

    @QtCore.Slot(QtCore.QModelIndex, QtCore.QModelIndex)
    def data_changed(self, top_left, bottom_right):
        self.update_columns(top_left, bottom_right)
 
