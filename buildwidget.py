
from PySide import QtGui, QtCore
from subprocess import call

from mlistwidget import MListWidget

class Builder(QtCore.QObject):

    new_build_errors = QtCore.Signal(list)
    build_finished = QtCore.Signal()

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.build_process = QtCore.QProcess()
        self.build_process.readyReadStandardOutput.connect(self.handle_build_stdout)
        self.build_process.readyReadStandardError.connect(self.handle_build_stderr)
        self.build_process.finished.connect(self.handle_build_finished)

    def build(self, expr):
        options = ["-c", expr]
        self.build_process.start("/bin/sh", options)

    def stop(self):
        self.build_process.terminate()

    def handle_build_stdout(self):
        self.build_process.setReadChannel(QtCore.QProcess.StandardOutput)
        while self.build_process.canReadLine():
            try:
                line = str(self.build_process.readLine())
                print(line)
            except:
                pass

    def handle_build_stderr(self):
        errors = []
        self.build_process.setReadChannel(QtCore.QProcess.StandardError)
        while self.build_process.canReadLine():
            try:
                line = str(self.build_process.readLine())
                errors.append(line)
            except Exception as e:
                print("Failed to read line of data from build:")
                print(str(e))
        self.new_build_errors.emit(errors)

    def handle_build_finished(self):
        self.build_finished.emit()



class BuildWidget(QtGui.QWidget):

    def __init__(self, settings, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setup_ui()
        self.builder = Builder()
        self.builder.new_build_errors.connect(self.handle_new_errors)

    def setup_ui(self):
        layout = QtGui.QGridLayout(self)
        self.setLayout(layout)

        self.build_command = QtGui.QLineEdit(self)
        layout.addWidget(self.build_command,0,0,1,1)

        self.build_button = QtGui.QPushButton("Build", self)
        layout.addWidget(self.build_button,0,1,1,1)
        QtCore.QObject.connect(self.build_button, QtCore.SIGNAL('clicked()'), self.build)

        self.result = MListWidget(self)
        layout.addWidget(self.result,1,0,1,2)

    @QtCore.Slot(list)
    def handle_new_errors(self, lines):
        print("STDERR")
        for line in lines:
            self.result.addItem(line)

    def build(self):
        build_cmd = self.build_command.text()
        headline = "Starting build: " + build_cmd
        print("")
        print(headline)
        print("="*len(headline))
        print("")
        self.builder.build(build_cmd)

