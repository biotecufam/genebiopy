
import csv, re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QHeaderView

from ..Models import Annotation


class ImportController():
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.main.browseBtn.clicked.connect(self.browseClick)
        self.model = self.createAnnotationModel()
        self.main.tableView.setModel(self.model)

    def browseClick(self):
        name, type = QFileDialog.getOpenFileName(None, "Selecione o arquivo",
                                                 filter="TSV File (*.tsv)")
        self.main.browseLine.setText(name)
        match = re.search(".*\.(.*)", name)
        if match:
            if match.group(1)=="tsv":
                self.openTsvFile(name)

    def openTsvFile(self, filename):
        with open(filename,'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for row in csv_reader:
                if 'Feature ID' in row:
                    anot = Annotation(row['Feature ID'], row['Accession ID'],
                                      row['Contig'], row['Frame'], row['Strand'],
                                      row['Start'], row['Stop'], row['Function'])
                    self.main.annotations[anot.featureID] = anot
                    self.addAnnotation(anot)
                if 'Features' in row:
                    c = row['Category']
                    for f in row['Features'].split(", "):
                        if f in self.main.annotations:
                            annotation = self.main.annotations[f]
                            annotation.category = row['Category']
                            annotation.subcategory = row['Subcategory']
                            annotation.subsystem = row['Subsystem']
                            annotation.role = row['Role']
        self.main.treeController.populateTreeWidget()

    def createAnnotationModel(self):
        model = QStandardItemModel(0, 7)
        model.setHorizontalHeaderLabels(["Feature ID","Contig","Frame","Strand",
                                         "Start","Stop","Function"])
        header = QHeaderView(Qt.Horizontal, None)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tableView.setHeader(header)
        return model

    def addAnnotation(self, annotation):
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), annotation.featureID)
        self.model.setData(self.model.index(0, 1), annotation.contig)
        self.model.setData(self.model.index(0, 2), annotation.frame)
        self.model.setData(self.model.index(0, 3), annotation.strand)
        self.model.setData(self.model.index(0, 4), annotation.start)
        self.model.setData(self.model.index(0, 5), annotation.stop)
        self.model.setData(self.model.index(0, 6), annotation.function)
