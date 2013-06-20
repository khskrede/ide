
from PySide import QtGui, QtCore
from subprocess import call

from widgets.mlistwidget import ListWidget

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
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.setup_ui()
        self.add_build_functionality()

    def setup_ui(self):
        self.layout = QtGui.QGridLayout(self)
        self.setLayout(self.layout)
        self.add_build_command_input()
        self.add_build_button()
        self.add_error_list()

    def add_build_functionality(self):
        self.builder = Builder()
        self.builder.new_build_errors.connect(self.handle_new_errors)

    def add_build_command_input(self):
        self.build_command = QtGui.QLineEdit(self)
        self.build_command.returnPressed.connect(self.start_build)
        self.layout.addWidget(self.build_command,0,0,1,1)

    def add_build_button(self):
        self.build_button = QtGui.QPushButton("Build", self)
        self.layout.addWidget(self.build_button,0,1,1,1)
        QtCore.QObject.connect(self.build_button, QtCore.SIGNAL('clicked()'), self.start_build)

    def add_error_list(self):
        self.error_list = ListWidget(self)
        self.layout.addWidget(self.error_list,1,0,1,2)

    @QtCore.Slot(list)
    def start_build(self):
        self.error_list.clear()
        build_cmd = self.build_command.text()
        headline = "Starting build: " + build_cmd
        print("\n" + headline)
        print("="*len(headline)+"\n")
        self.builder.build(build_cmd)

    @QtCore.Slot(list)
    def handle_new_errors(self, lines):
        print("STDERR")
        for line in lines:
            self.error_list.addItem(line)

