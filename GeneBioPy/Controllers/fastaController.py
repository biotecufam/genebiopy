
import csv, re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QTableWidgetItem

from ..Models import Annotation


class ImportController():
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.main.fastaBtn.clicked.connect(self.fastaClick)

    def fastaBtn(self):
        for (anot in self.main.treeController.getCheckedAnnotations()):
            self.fastaText.append(">{}".format(anot.featureID))
            if(anot.contig in self.main.contigs):
                contig = self.main.contigs[anot.contig]
                if (len(contig)+1 > anot.start and len(contig)+1 > anot.stop):
                    if(anot.stop < anot.start):
                        self.fastaText.append(contig[anot.start:anot.stop])
