#!/usr/bin/env python

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeyEvent

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

Ui_Help, _ = uic.loadUiType("help.ui")

class Help(QDialog, Ui_Help):

	def __init__(self, parent=None):

		QDialog.__init__(self, parent=parent)
		Ui_Help.__init__(self)
		self.setupUi(self)	
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Help()
    main.show()

    sys.exit(app.exec_())