
from PyQt5.QtWidgets import QSizePolicy, QMessageBox
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class TreePieChartController:
    def __init__(self, MainWindow):
        self.main = MainWindow

    def plotPieChart(self):
        m = PlotCanvas(self.main.pieFrame, width=2, height=2)
        m.move(0,100)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        #sizes = [200, 200, 200, 200]
        #self.axes.pie(sizes, autopct='%1.0f%%')
        #self.draw()
        size = 0.2
        vals = np.array([[100, 32, 60], [37, 40, 30], [29, 10, 87], [29, 10, 24], [10, 20, 10]])

        cmap = plt.get_cmap("tab20c")
        outer_colors = cmap(np.arange(5)*4)
        inner_colors = cmap(np.array([1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]))
        self.axes.pie(vals.sum(axis=1), radius=1-size, colors=outer_colors,
                      wedgeprops=dict(width=size, edgecolor='w'))
        self.axes.pie(vals.flatten(), radius=1, colors=inner_colors,
                      wedgeprops=dict(width=size, edgecolor='w'))
