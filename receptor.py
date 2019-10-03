#!/usr/bin/env python3

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeyEvent

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

Ui_Receptor, _ = uic.loadUiType("receptor.ui")

class Receptor(QDialog, Ui_Receptor):

	def __init__(self, parent=None):

		QDialog.__init__(self, parent=parent)
		Ui_Receptor.__init__(self)
		self.setupUi(self)
		
		self.label1.setHidden(not False)
		self.label2.setHidden(not False)	

		self.timer = QTimer(self)

		self.events() 

		self.timer.setInterval(300)
		self.timer.start()

	def events(self):
		self.timer.timeout.connect(self.atualizaOpcoes)		 			

	def atualizaOpcoes(self):				
		if(self.radioButton1.isChecked()):			
			self.label1.setHidden(not True)
			self.label2.setHidden(not True)

		else:			
			self.label1.setHidden(not False)	
			self.label2.setHidden(not False)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Receptor()
    main.show()

    sys.exit(app.exec_())