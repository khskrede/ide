

from PySide import QtGui, QtCore

class MListWidget(QtGui.QListWidget):

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self, parent)

    def contextMenuEvent(self, event):
        pos = QtGui.QCursor.pos()
        m = QtGui.QMenu()
        m.addAction("Diff with previous revision")
        m.exec_(pos)


