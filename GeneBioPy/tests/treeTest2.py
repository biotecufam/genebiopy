import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def main():
    app     = QApplication (sys.argv)
    tree    = QTreeWidget ()

    for i in xrange(3):
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "Parent {}".format(i))
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        for x in xrange(5):
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, "Child {}".format(x))
            child.setCheckState(0, Qt.Unchecked)
    tree.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
