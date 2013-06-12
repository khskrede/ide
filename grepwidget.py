
from PySide import QtGui, QtCore
from subprocess import call

from mlistwidget import MListWidget

class Grep(QtCore.QObject):

    new_grep_results = QtCore.Signal(list)
    grep_finished = QtCore.Signal()

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.grep_process = QtCore.QProcess()
        self.grep_process.readyReadStandardOutput.connect(self.handle_grep_output)
        self.grep_process.finished.connect(self.handle_grep_finished)

    def grep(self, expr):
        options = ["-c", expr]
        self.grep_process.start("/bin/sh", options)

    def stop(self):
        self.grep_process.terminate()

    def handle_grep_output(self):
        results = []
        while self.grep_process.canReadLine():
            try:
                line = str(self.grep_process.readLine())
                results.append(line)
            except Exception as e:
                print("Failed to read line of data from grep:")
                print(str(e))
        self.new_grep_results.emit(results)

    def handle_grep_finished(self):
        self.grep_finished.emit()


class GrepWidget(QtGui.QWidget):

    def __init__(self, settings, parent):
        QtGui.QWidget.__init__(self, parent)

        self.setup_ui()

        self.grepping = False
        self.grep = Grep()
        self.grep.new_grep_results.connect(self.handle_new_results)
        self.grep.grep_finished.connect(self.handle_grep_finished)

    def setup_ui(self):
        self.layout = QtGui.QGridLayout(self)
        self.setLayout(self.layout)

        self.grep_line = QtGui.QLineEdit(self)
        self.grep_line.returnPressed.connect(self.start_grep)
        self.grep_line.setText("grep -RHn ")
        self.layout.addWidget(self.grep_line, 0, 0, 1, 1)

        self.grep_button = QtGui.QPushButton("Grep", self)
        self.grep_button.clicked.connect(self.grep_button_clicked)
        self.layout.addWidget(self.grep_button, 0, 1, 1, 1)

        self.file_result = MListWidget(self)
        self.file_result.itemDoubleClicked.connect(self.file_double_clicked)
        self.file_result.currentItemChanged.connect(self.file_item_changed)

        self.line_result = MListWidget(self)
        self.line_result.itemDoubleClicked.connect(self.line_nr_double_clicked)

        self.splitter = QtGui.QSplitter(self)
        self.splitter.addWidget(self.file_result)
        self.splitter.addWidget(self.line_result)
        self.layout.addWidget(self.splitter, 1, 0, 1, 2)

    @QtCore.Slot(list)
    def handle_new_results(self, lines):
        for line in lines:
            try:
                split_line = str(line).split(":")
                if len(split_line) > 1:
                    file_name = split_line[0]
                    line_number = int(split_line[1])
                    if not file_name in self.grep_results:
                        self.grep_results[file_name] = []
                        self.add_file_name(file_name)
                    self.grep_results[file_name].append(str(line_number))

            except Exception as e:
                print("Something went wrong: " + str(e))

    def grep_button_clicked(self):
        if not self.grepping:
            self.start_grep()
        else:
            self.stop_grep()

    def start_grep(self):
        self.grep_results = {}
        self.grepping = True
        self.grep_button.setText("Stop")
        self.file_result.clear()
        self.line_result.clear()
        result = self.grep.grep( self.grep_line.text() )

    def stop_grep(self):
        self.grep.stop()

    @QtCore.Slot()
    def handle_grep_finished(self):
        self.grepping = False
        self.grep_button.setText("Grep")

    def add_file_name(self, file_name):
        file_info = QtCore.QFileInfo(file_name)
        file_icon = QtGui.QFileIconProvider().icon(file_info)
        item = QtGui.QListWidgetItem(file_icon, file_name)
        self.file_result.addItem(item)

    def file_item_changed(self, current, previous):
        self.line_result.clear()
        if not current:
            return
        value = self.grep_results[current.text()]
        for nr in value:
            try:
                item = QtGui.QListWidgetItem(nr)
                self.line_result.addItem(item)
            except Exception as e:
                print("Failed to handle line numbers: " + str(e))

    def file_double_clicked(self, item):
        call(["vim", "--servername", "myIde", "--remote", item.text()])

    def line_nr_double_clicked(self, item):
        call(["vim", "--servername", "myIde", "--remote-send", ":e " + self.file_result.currentItem().text() + "<CR>"+":"+item.text()+"<CR>"])
        print(item.text())


