import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory

from file import FileOperation

app = QtWidgets.QApplication(sys.argv)
app.setStyle(QStyleFactory.create("Fusion"))
file_widget = FileOperation()
file_widget.set_up_ui()
file_widget.show()

sys.exit(app.exec_())
