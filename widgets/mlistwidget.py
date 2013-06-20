

from PySide import QtGui, QtCore

class ListWidget(QtGui.QListWidget):

    returnPressed = QtCore.Signal(QtGui.QListWidgetItem)

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self, parent)

    def contextMenuEvent(self, event):
        pos = QtGui.QCursor.pos()
        m = QtGui.QMenu()
        m.addAction("Diff with previous revision")
        m.exec_(pos)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.returnPressed.emit(self.currentItem())
        QtGui.QListWidget.keyPressEvent(self, event)
