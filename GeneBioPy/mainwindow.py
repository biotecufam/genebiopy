
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from .Controllers import TreeController,ImportController,TreePieChartController

qtCreatorFile = "Resources/reader.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.treeChartController = TreePieChartController(self)
        self.importController = ImportController(self)
        self.treeController = TreeController(self)
        self.annotations = {}
        self.contigs = {}
        self.logCount = 0

    def appendLog(self, text):
        self.logCount += 1
        self.consoleText.append("[{}]: {}".format(self.logCount, text))
