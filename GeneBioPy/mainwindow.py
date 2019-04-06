import csv, re
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QHeaderView, QTreeWidgetItem
from GeneBioPy.models.annotation import Annotation

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


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
                    anot = Annotation(row['Feature ID'], row['Accession ID'], row['Contig'], row['Strand'], row['Start'], row['Stop'], row['Function'])
                    self.annotations[anot.featureID] = anot
                    self.addAnnotation(anot)
                if 'Features' in row:
                    c = row['Category']
                    for f in row['Features'].split(", "):
                        if f in self.annotations:
                            self.annotations[f].category = row['Category']
                            self.annotations[f].subcategory = row['Subcategory']
                            self.annotations[f].subsystem = row['Subsystem']
                            self.annotations[f].role = row['Role']
                            if c not in self.categories:
                                self.categories[c] = {}
                            self.categories[c][f] = self.annotations[f]
        self.populateTreeWidget()

    def populateTreeWidget(self):
        self.treeWidget.clear()
        for cat in self.categories:
            parent = QTreeWidgetItem(self.treeWidget)
            parent.setText(0, "{} ({})".format(cat,len(self.categories[cat])))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            self.populateTreeWidgetChildren(parent, self.categories[cat])
        if len(self.categories) == 0:
            parent = QTreeWidgetItem(self.treeWidget)
            parent.setText(0, "No Category ({})".format(len(self.annotations)))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            self.populateTreeWidgetChildren(parent, self.annotations)

    def populateTreeWidgetChildren(self, parent, children):
        for ch in children:
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, ch)
            child.setCheckState(0, Qt.Unchecked)

    def createAnnotationModel(self):
        model = QStandardItemModel(0, 7)
        model.setHorizontalHeaderLabels(["Feature ID","Accession ID","Contig","Strand","Start","Stop","Function"])
        header = QHeaderView(Qt.Horizontal, None)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tableView.setHeader(header)
        self.tableView.setModel(model)
        return model

    def addAnnotation(self, annotation):
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), annotation.featureID)
        self.model.setData(self.model.index(0, 1), annotation.accessionID)
        self.model.setData(self.model.index(0, 2), annotation.contig)
        self.model.setData(self.model.index(0, 3), annotation.strand)
        self.model.setData(self.model.index(0, 4), annotation.start)
        self.model.setData(self.model.index(0, 5), annotation.stop)
        self.model.setData(self.model.index(0, 6), annotation.function)
