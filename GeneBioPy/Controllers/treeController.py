
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog


class TreeController:
    def __init__(self, MainWindow):
        self.main = MainWindow
        self.main.treeWidget.headerItem().setHidden(True)
        self.main.gffBtn.clicked.connect(self.saveCheckedAnnotation)
        self.clearTree()

    def clearTree(self):
        self.main.treeWidget.clear()
        self.root = MyTreeWidgetItem(self.main.treeWidget, "All", Types.CATEGORY)
        self.root.setFlags(self.root.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.noCat = self.root.addChild("No Category", Types.CATEGORY)
        self.noCat.setFlags(self.noCat.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.root.setExpanded(True)

    def saveCheckedAnnotation(self):
        filename, type = QFileDialog.getSaveFileName(None, "Salvar o arquivo",
                                                     filter="GFF File (*.gff)")
        if not filename.endswith(".gff"):
            filename = filename + ".gff"
        with open(filename, 'w') as file:
            file.write("﻿##gff-version 3\n")
            for annotation in self.getCheckedAnnotations():
                file.write(annotation.getGffText() + "\n")

    def getCheckedAnnotations(self):
        it = QTreeWidgetItemIterator(self.main.treeWidget,
                                     QTreeWidgetItemIterator.Checked)
        checkedAnnotations = []
        while it.value():
            item = it.value()
            if isinstance(item, MyTreeWidgetItem) and item.type == Types.ANNOTATION:
                if item.name in self.main.annotations:
                    checkedAnnotations.append(self.main.annotations[item.name])
            it += 1
        return checkedAnnotations

    def addCategoriesToTree(self, c, sc, ss, r, f):
        category = self.root.addChild(c, Types.CATEGORY)
        subcategory = category.addChild(sc, Types.SUBCATEGORY)
        subsystem = subcategory.addChild(ss, Types.SUBSYSTEM)
        role = subsystem.addChild(r, Types.ROLE)
        for a in f:
            role.addChild(a, Types.ANNOTATION)

    def addAnnotationsToTree(self):
        self.noCat.removeChildren()
        self.root.updateSubtree(self.main.annotations)
        for a in self.main.annotations.values():
            if a.roleCount == 0:
                self.noCat.addChild(a.featureID, Types.ANNOTATION)
        self.noCat.updateSubtree(self.main.annotations)
        self.root.updateNameCounter(self.noCat.leafCount)


from enum import Enum
class Types(Enum):
    NO_TYPE, CATEGORY, SUBCATEGORY, SUBSYSTEM, ROLE, ANNOTATION = range(6)


class MyTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, parent, name, type=Types.NO_TYPE):
        super().__init__(parent)
        self.name = name
        self.type = type
        self.children = {}
        self.leafCount = 0
        self.setText(0, name)

    def removeChildren(self):
        self.takeChildren()
        self.children = {}
        self.leafCount = 0

    def addChild(self, name, type):
        if name not in self.children:
            self.children[name] = MyTreeWidgetItem(self, name, type)
        return self.children[name]

    def updateNameCounter(self, leafCount=0):
        self.leafCount += leafCount
        self.setText(0, "{} ({})".format(self.name, self.leafCount))

    def updateSubtree(self, annotations):
        self.leafCount = 0
        for item in self.children.values():
            if item.type == Types.ANNOTATION:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(0, Qt.Unchecked)
                self.leafCount += 1
                if item.name in annotations and item.childCount() == 0:
                    a = annotations[item.name]
                    if self.type == Types.ROLE:
                        a.roleCount += 1
                    MyTreeWidgetItem(item, "Function: {}".format(a.function))
                    MyTreeWidgetItem(item, "Contig: {}".format(a.contig))
                    MyTreeWidgetItem(item, "Frame: {}".format(a.frame))
                    MyTreeWidgetItem(item, "Strand: {}".format(a.strand))
                    MyTreeWidgetItem(item, "Start: {}".format(a.start))
                    MyTreeWidgetItem(item, "Stop: {}".format(a.stop))
            elif not item.type == Types.NO_TYPE:
                item.updateSubtree(annotations)
                self.leafCount += item.leafCount
        self.setFlags(self.flags() | Qt.ItemIsTristate |Qt.ItemIsUserCheckable)
        self.setCheckState(0, Qt.Unchecked)
        self.updateNameCounter()
