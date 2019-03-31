import csv, re
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QHeaderView

qtCreatorFile = "/home/pablo/github/genebiopy/GeneBioPy/resources/reader.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.browseBtn.clicked.connect(self.browseClick)
        self.model = self.createAnnotationModel()
        self.annotations = {}
        self.categories = {}
        self.subcategories = {}
        self.subsystems = {}

    def browseClick(self):
        name, type = QFileDialog.getOpenFileName(None, "Selecione o arquivo", filter="TSV File (*.tsv)")
        self.browseLine.setText(name)
        match = re.search(".*\.(.*)", name)
        if match:
            if match.group(1)=="tsv":
                self.openTsvFile(name)

    def openTsvFile(self, filename):
        with open(filename,'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for row in csv_reader:
                if 'Feature ID' in row:
                    anot = (row['Feature ID'], row['Contig'], row['Strand'], row['Start'], row['Stop'], row['Function'])
                    self.annotations[0] = anot
                    self.addAnnotation(anot)
                if 'Features' in row:
                    c,sc,ss,r = row['Category'],row['Subcategory'], row['Subsystem'],row['Role']
                    for f in row['Features'].split(", "):
                        if not c in self.categories:
                            self.categories[c] = set()
                        self.categories[c].add(sc)
                        if not sc in self.subcategories:
                            self.subcategories[sc] = set()
                        self.subcategories[sc].add(ss)
                        if not ss in self.subsystems:
                            self.subsystems[ss] = set()
                        self.subsystems[ss].add(f)

    def createAnnotationModel(self):
        model = QStandardItemModel(0, 7)
        model.setHorizontalHeaderLabels(["Feature ID","Ascession ID","Contig","Strand","Start","Stop","Function"])
        header = QHeaderView(Qt.Horizontal, None)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tableView.setHeader(header)
        self.tableView.setModel(model)
        return model

    def addAnnotation(self, annotation):
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), annotation[0])
        self.model.setData(self.model.index(0, 2), annotation[1])
        self.model.setData(self.model.index(0, 3), annotation[2])
        self.model.setData(self.model.index(0, 4), annotation[3])
        self.model.setData(self.model.index(0, 5), annotation[4])
        self.model.setData(self.model.index(0, 6), annotation[5])
