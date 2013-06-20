
from PySide import QtGui, QtCore
from subprocess import call
from widgets.mlistwidget import ListWidget

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
    def __init__(self, settings):
        QtGui.QWidget.__init__(self)
        self.settings = settings
        self.setup_ui()
        self.add_grep_functionality()

    def setup_ui(self):
        self.layout = QtGui.QGridLayout(self)
        self.setLayout(self.layout)

        self.add_grep_input_line()
        self.add_grep_button()
        self.add_splitter()
        self.add_list_for_files()
        self.add_list_for_lines()
    
    def add_grep_button(self):
        self.grep_button = QtGui.QPushButton("Grep", self)
        self.grep_button.clicked.connect(self.grep_button_clicked)
        self.layout.addWidget(self.grep_button, 0, 1, 1, 1)

    def add_grep_input_line(self):
        self.grep_line = QtGui.QLineEdit(self)
        self.grep_line.returnPressed.connect(self.start_grep)
        self.grep_line.setText("grep -RHn ")
        self.layout.addWidget(self.grep_line, 0, 0, 1, 1)

    def add_splitter(self):
        self.splitter = QtGui.QSplitter(self)
        self.layout.addWidget(self.splitter, 1, 0, 1, 2)

    def add_list_for_files(self):
        self.file_result = ListWidget(self)
        self.file_result.itemDoubleClicked.connect(self.file_double_clicked)
        self.file_result.returnPressed.connect(self.file_double_clicked)
        self.file_result.currentItemChanged.connect(self.file_item_changed)
        self.splitter.addWidget(self.file_result)

    def add_list_for_lines(self):
        self.line_result = ListWidget(self)
        self.line_result.itemDoubleClicked.connect(self.line_nr_double_clicked)
        self.line_result.returnPressed.connect(self.line_nr_double_clicked)
        self.splitter.addWidget(self.line_result)

    def add_grep_functionality(self):
        self.grepping = False
        self.grep = Grep()
        self.grep.new_grep_results.connect(self.handle_new_results)
        self.grep.grep_finished.connect(self.handle_grep_finished)

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
        self.settings.file_path_double_clicked(item.text())

    def line_nr_double_clicked(self, item):
        self.settings.line_nr_double_clicked(item.text())

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

    @QtCore.Slot()
    def handle_grep_finished(self):
        self.grepping = False
        self.grep_button.setText("Grep")


