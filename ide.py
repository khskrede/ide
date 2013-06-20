#!/usr/bin/python3

import sys
from subprocess import call
from PySide import QtGui, QtCore
from widgets.main import MainWindow
from widgets.filetree import FileTreeWidget
from widgets.grep import GrepWidget
from widgets.build import BuildWidget
from common.settings import Settings

def file_path_double_clicked(path):
    call(["vim", "--servername", "myIde", "--remote", path])

def line_nr_double_clicked(path):
    call(["vim", "--servername", "myIde", "--remote-send", ":e " + self.file_result.currentItem().text() + "<CR>"+":"+item.text()+"<CR>"])

def main():
    app = QtGui.QApplication(sys.argv)

    vim_controller_settings = Settings()

    vim_controller_settings.file_path_double_clicked = file_path_double_clicked
    vim_controller_settings.line_nr_double_clicked = line_nr_double_clicked

    file_tree_widget = FileTreeWidget(vim_controller_settings)
    grep_widget = GrepWidget(vim_controller_settings)
    build_widget = BuildWidget(vim_controller_settings)

    window = MainWindow("Vim Controller", vim_controller_settings)
    window.add_widget("Files", file_tree_widget)
    window.add_widget("Grep", grep_widget)
    window.add_widget("Build", build_widget)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

