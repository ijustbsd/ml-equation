from PyQt6 import QtWidgets

from app.gui import MainWindow

app = QtWidgets.QApplication([])

w = MainWindow()
w.show()

app.exec()
