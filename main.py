import sys, time
from PyQt5.QtWidgets import QApplication, QMessageBox
from GeneBioPy import MainWindow

"""
def excepthook(excType, excValue, tracebackobj):

    Global function to catch unhandled exceptions.
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object

    QMessageBox.critical(None, "Critical Error", text=excValue).show()
    time.sleep(1000000)

sys.excepthook = excepthook
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
