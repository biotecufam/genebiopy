
import csv, re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QTableWidgetItem

from ..Models import Annotation


class ImportController():
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.main.clearBtn.clicked.connect(self.clearClick)
        self.main.browseBtn.clicked.connect(self.browseClick)
        self.main.tableWidget.setColumnCount(7)
        self.main.tableWidget.setWordWrap(False)
        self.main.tableWidget.setShowGrid(False)
        self.main.tableWidget.setSortingEnabled(True)
        self.main.tableWidget.verticalHeader().setVisible(False)
        #self.main.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.main.tableWidget.setColumnWidth(5, 80)
        self.main.tableWidget.setColumnWidth(0, 200)
        self.main.tableWidget.setColumnWidth(1, 200)
        self.main.tableWidget.setColumnWidth(2, 60)
        self.main.tableWidget.setColumnWidth(3, 60)
        self.main.tableWidget.setColumnWidth(4, 60)
        self.main.tableWidget.setColumnWidth(5, 60)
        self.main.tableWidget.setColumnWidth(6, 300)
        self.main.tableWidget.setHorizontalHeaderLabels(
            ["Feature ID","Contig","Frame","Strand","Start","Stop","Function"])

    def clearClick(self):
        self.main.treeController.clearTree()
        self.main.annotations.clear()
        self.main.tableWidget.clear()
        self.main.tableWidget.setRowCount(0)
        self.main.tableWidget.setHorizontalHeaderLabels(
            ["Feature ID","Contig","Frame","Strand","Start","Stop","Function"])

    def browseClick(self):
        name, type = QFileDialog.getOpenFileName(
            None, "Selecione o arquivo", filter="TSV GFF File (*.tsv *gff);;"+
                                                "All Files (*.*)")
        self.main.browseLine.setText(name)
        self.main.appendLog("Importando arquivo {}.".format(name))
        if name.endswith("gff"):
            self.openGffFile(name)
        if name.endswith("tsv"):
            self.openTsvFile(name)
        if name.endswith("fa"):
            self.openFastaFile(name)

    def openGffFile(self, filename):
        annotationsAdded, annotationsExisted, annotationsMalformed = 0, 0, 0
        with open(filename,'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            for row in csv_reader:
                if (row[0].startswith("#") or not len(row) == 9):
                    continue
                d = dict((k, v) for k,v in (item.split("=") for item
                                            in row[8].split(";")))
                if ('ID' in d and 'Name' in d):
                    if(self.createAddAnnotation(d['ID'],"",row[0],row[7],row[6],
                                                row[3], row[4], d['Name'])):
                        annotationsAdded += 1
                    else:
                        annotationsExisted += 1
                else:
                    annotationsMalformed += 1
        self.main.appendLog("Foram adicionados {} Anotações.".format(annotationsAdded))
        self.main.appendLog("{} Anotações já existinham e não foram adicionadas.".format(annotationsExisted))
        self.main.appendLog("{} Anotações não reconhecidas.".format(annotationsMalformed))
        self.main.treeController.addAnnotationsToTree()

    def openTsvFile(self, filename):
        annotationsAdded, annotationsExisted, annotationsMalformed = 0, 0, 0
        with open(filename,'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t")
            for row in csv_reader:
                if 'Feature ID' in row:
                    length, frame = int(row['Length (bp)']), int(row['Frame'])
                    frame = (length+frame+1)%3
                    if(self.createAddAnnotation(row['Feature ID'], row['Accession ID'],
                                                row['Contig'], str(frame), row['Strand'],
                                                row['Start'], row['Stop'], row['Function'])):
                        annotationsAdded += 1
                    else:
                        annotationsExisted += 1
                elif 'Features' in row:
                    c, sc = row['Category'], row['Subcategory']
                    ss, r = row['Subsystem'], row['Role']
                    f = list(map(str.strip, row['Features'].split(",")))
                    self.main.treeController.addCategoriesToTree(c,sc,ss,r,f)
                else:
                    annotationsMalformed += 1
        self.main.appendLog("Foram adicionados {} Anotações.".format(annotationsAdded))
        self.main.appendLog("{} Anotações já existinham e não foram adicionadas.".format(annotationsExisted))
        self.main.appendLog("{} Anotações não reconhecidas.".format(annotationsMalformed))
        self.main.treeController.addAnnotationsToTree()

    def openFastaFile(self, filename):
        currentContig = None
        with open(filename,'r') as file:
            for line in file:
                if line.startswith(">"):
                    currentContig = line[1:]
                    if(currentContig not in self.main.contigs):
                        self.main.contigs[currentContig] = ""
                    else:
                        pass
                else:
                    if(currentContig):
                        self.main.contigs[currentContig] += line.strip()
                    else:
                        pass        

    def createAddAnnotation(self, feature, ascession, contig, frame,
                            strand, start, stop, function):
        if(feature not in self.main.annotations):
            annotation = Annotation(feature, ascession, contig, frame,
                                    strand, start, stop, function)
            self.main.annotations[annotation.featureID] = annotation
            self.addAnnotationToTableView(annotation)
        else:
            return False
        return True

    def addAnnotationToTableView(self, annotation):
        length = self.main.tableWidget.rowCount()
        self.main.tableWidget.insertRow(length)
        self.main.tableWidget.setItem(length, 0, QTableWidgetItem(annotation.featureID))
        self.main.tableWidget.setItem(length, 1, QTableWidgetItem(annotation.contig))
        self.main.tableWidget.setItem(length, 2, QTableWidgetItem(annotation.frame))
        self.main.tableWidget.setItem(length, 3, QTableWidgetItem(annotation.strand))
        self.main.tableWidget.setItem(length, 4, QTableWidgetItem(annotation.start))
        self.main.tableWidget.setItem(length, 5, QTableWidgetItem(annotation.stop))
        self.main.tableWidget.setItem(length, 6, QTableWidgetItem(annotation.function))
        self.main.tableWidget.item(length, 2).setTextAlignment(Qt.AlignCenter)
        self.main.tableWidget.item(length, 3).setTextAlignment(Qt.AlignCenter)
