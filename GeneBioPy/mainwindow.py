
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from .Controllers import TreeController
from .Controllers import ImportController

#om matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt

qtCreatorFile = "/home/pablo/github/genebiopy/Resources/reader.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.importController = ImportController(self)
        self.treeController = TreeController(self)
        self.annotations = {}
