
from PySide import QtGui, QtCore
from common.settings import Settings

from widgets.filetree import FileTreeWidget
from widgets.grep import GrepWidget
from widgets.build import BuildWidget

class MainWindow(QtGui.QMainWindow):

    def __init__(self, name, settings):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle(name)
        self.resize(500,650)
        self.tab_widget = QtGui.QTabWidget()
        self.setCentralWidget(self.tab_widget)

    def add_widget(self, name, widget):
        self.tab_widget.addTab(widget, name)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

