import sys
from PyQt5.QtWidgets import QApplication
from GeneBioPy.mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
