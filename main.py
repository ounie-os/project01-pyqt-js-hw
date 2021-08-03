import sys
import typing

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QStyleFactory, QProxyStyle, QStyle, QStyleOptionTab, QTabBar, QWidget, QStyleOption

from file import FileOperation


class CustomStyle(QProxyStyle):
    def sizeFromContents(type_, option, size, widget):
        s = QProxyStyle.sizeFromContents(type_, option, size, widget)
        if type_ == QStyle.CT_TabBarTab:
            s.transpose()
        return s

    def drawControl(self, element: QStyle.ControlElement, option: 'QStyleOption', painter: QtGui.QPainter, widget: typing.Optional[QWidget] = ...) -> None:
        if element == QStyle.CE_TabBarTabLabel:
            if isinstance(option, QStyleOptionTab):
                option.shape = QTabBar.RoundedWest
                super().drawControl(element, option, painter, widget)

        super().drawControl(element, option, painter, widget)





app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
file_widget = FileOperation()
file_widget.set_up_ui()
file_widget.show()

sys.exit(app.exec_())
