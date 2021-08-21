# cython: language_level=3

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QFont


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)

        s.transpose()

        s.setWidth(123)
        s.setHeight(40)

        return s

    def repaint_text(self, painter, i):
        text_option = QtGui.QTextOption()
        text_option.setAlignment(QtCore.Qt.AlignCenter)
        new_rect = QRectF(self.tabRect(i))
        painter.drawText(new_rect, self.tabText(i), text_option)

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        option = QtWidgets.QStyleOptionTab()

        color = QtGui.QColor()

        font = QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.setFont(font)

        self.setGeometry(0, 325, 123, 200)

        for i in range(self.count()):
            self.initStyleOption(option, i)
            the_rect = option.rect

            # 被选中
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.save()
                # 白色
                color.setRgb(255, 255, 255)
                painter.fillRect(the_rect, color)
                painter.restore()
                painter.save()
                color.setRgb(10, 145, 217)
                painter.setPen(color)
                self.repaint_text(painter, i)
                painter.restore()
            else:
                painter.save()
                color.setRgb(255, 255, 255)
                painter.fillRect(the_rect, color)
                painter.restore()

                painter.save()
                color.setRgb(10, 145, 217)
                painter.fillRect(the_rect.adjusted(0, 1, 0, -1), color)
                painter.restore()

                painter.save()
                color.setRgb(255, 255, 255)
                painter.setPen(color)
                self.repaint_text(painter, i)
                painter.restore()


class HwTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)
