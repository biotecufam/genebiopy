
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem


class TreeController:
    def __init__(self, MainWindow):
        self.main = MainWindow

    def getAnotAttr(self, annotation, treeLvl):
        ret = ""
        if treeLvl == 1:
            ret = annotation.category
        elif treeLvl == 2:
            ret = annotation.subcategory
        elif treeLvl == 3:
            ret = annotation.subsystem
        return ret

    def populateTreeWidget(self):
        self.main.treeWidget.clear()
        self.populateNodes(self.main.treeWidget, "All", self.main.annotations.values(), 1)

    def populateNodes(self, parent, groupName, annotations, treeLvl):
        if(groupName==""):
            for annotation in annotations:
                self.populateAnnotation(parent, annotation)
            return
        groupItem = QTreeWidgetItem(parent)
        groupItem.setFlags(groupItem.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        groupItem.setText(0, "{} ({})".format(groupName, len(annotations)))
        children = {}
        for anot in annotations:
            attr = self.getAnotAttr(anot, treeLvl)
            if attr not in children:
                children[attr] = []
            children[attr].append(anot)
        for key, value in children.items():
            self.populateNodes(groupItem, key, value, treeLvl+1)

    def populateAnnotation(self, parent, annotation):
        item = QTreeWidgetItem(parent)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setText(0, "{}".format(annotation.featureID))
        item.setCheckState(0, Qt.Unchecked)
        QTreeWidgetItem(item).setText(0, "Function: {}".format(annotation.function))
        QTreeWidgetItem(item).setText(0, "Contig: {}".format(annotation.contig))
        QTreeWidgetItem(item).setText(0, "Frame: {}".format(annotation.frame))
        QTreeWidgetItem(item).setText(0, "Strand: {}".format(annotation.strand))
        QTreeWidgetItem(item).setText(0, "Start: {}".format(annotation.start))
        QTreeWidgetItem(item).setText(0, "Stop: {}".format(annotation.stop))
