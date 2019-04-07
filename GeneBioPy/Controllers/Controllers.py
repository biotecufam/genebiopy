from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem


class TreeController:
    def __init__(self, MainWindow):
        self.main = MainWindow

    def getAnotAttr(self, annotation, treeLvl):
        if treeLvl == 1:
            return annotation.category
        if treeLvl == 2:
            return annotation.subcategory
        if treeLvl == 3:
            return annotation.subsystem

    def populateAnnotation(self, parent, annotation):
        item = QTreeWidgetItem(parent)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setText(0, "{}".format(annotation.featureID))
        item.setCheckState(0, Qt.Unchecked)
        QTreeWidgetItem(item).setText(0, "Function: {}".format(annotation.function))
        QTreeWidgetItem(item).setText(0, "Contig: {}".format(annotation.contig))
        QTreeWidgetItem(item).setText(0, "Strand: {}".format(annotation.strand))
        QTreeWidgetItem(item).setText(0, "Start: {}".format(annotation.start))
        QTreeWidgetItem(item).setText(0, "Stop: {}".format(annotation.stop))

    def populateTree(self, parent, name, annotations, treeLvl):
        if(name=="" or treeLvl > 3):
            for annotation in annotations:
                self.populateAnnotation(parent, annotation)
            return
        treeItem = QTreeWidgetItem(parent)
        treeItem.setFlags(treeItem.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        treeItem.setText(0, "{} ({})".format(name,len(annotations)))
        children = {}
        for anot in annotations:
            attr = self.getAnotAttr(anot, treeLvl)
            if attr not in children:
                children[attr] = []
            children[attr].append(anot)
        for ch in children.keys():
            self.populateTree(treeItem, ch, children[ch], treeLvl+1)

    def populateTreeWidget(self):
        self.main.treeWidget.clear()
        self.populateTree(self.main.treeWidget, "All", self.main.annotations.values(), 1)
