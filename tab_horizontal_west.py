# cython: language_level=3

from PyQt5 import QtWidgets, QtCore, QtGui


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)

        # 调整每个tab bar的尺寸与布局
        # s.setWidth(s.width() + 30)
        # s.setHeight(s.height() + 50)

        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        # 设置tab的字体
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        painter.setFont(font)

        # 设置tab的位置与尺寸
        self.setGeometry(0, 180, 123, 200)

        for i in range(self.count()):
            self.initStyleOption(opt, i)

            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()

            # 调整这里，使得文字能够完整显示
            s.setWidth(s.width() + 75)
            opt.rect.setSize(s)

            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())

            c = self.tabRect(i).center()


            # 调整x，y坐标来调整文字在tab中的位置
            c.setX(c.x() + 20)
            c.setY(c.y() + 20)

            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

    def tabTextColor(self, index):
        QtWidgets.QTabBar.tabTextColor(self, index)


class HwTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)
