import sys
import typing

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QStyleFactory, QProxyStyle, QStyle, QStyleOptionTab, QTabBar, QWidget, QStyleOption

from file import FileOperation


app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
file_widget = FileOperation()
file_widget.set_up_ui()
file_widget.show()

sys.exit(app.exec_())
