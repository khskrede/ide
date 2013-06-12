
import sys
from PySide import QtGui, QtCore

from settings import Settings

from grepwidget import GrepWidget
from buildwidget import BuildWidget

class IdeMainWindow(QtGui.QMainWindow):

    def __init__(self, settings):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("MyIDE")
        self.resize(500,650)

        self.tab_widget = QtGui.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.grep_widget = GrepWidget(settings, self)
        self.tab_widget.addTab(self.grep_widget, "Grep")

        self.build_widget = BuildWidget(settings, self)
        self.tab_widget.addTab(self.build_widget, "Build")

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

def main():
    app = QtGui.QApplication(sys.argv)

    my_ide_setup = Settings()

    window = IdeMainWindow(my_ide_setup)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

