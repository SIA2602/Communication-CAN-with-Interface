#!/usr/bin/env python3

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from help import Help
from about import About
from visualization import Visualization
from emissor import Emissor
from receptor import Receptor

Ui_MainWindow, QtBaseClass = uic.loadUiType("principal.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    
	def __init__(self, parent=None):

		QMainWindow.__init__(self, parent=parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self) 			

		self.atualizaOpcoes() #funcao responsavel por criar opcoes do comboBox	
		self.events() #atualizacoes altomaticas		

		self.buttonBox.accepted.connect(self.options)
		self.buttonBox.rejected.connect(self.close)
		#self.buttonBox.helpRequested.connect(self.open_help)

	def events(self):
		self.actionAjuda.triggered.connect(self.open_help)
		self.actionA_Equipe.triggered.connect(self.open_about)
		self.actionO_Trabalho.triggered.connect(self.open_about)
		self.comboBox1.currentIndexChanged.connect(self.atualizaOpcoes) #faz com que o comboBox seja atualizado automaticamente				 			
			
	def atualizaOpcoes(self):				
		if(self.comboBox1.currentText() == 'Select an Option'):				
			self.buttonBox.setHidden(not False)	
		else: self.buttonBox.setHidden(not True)

	def options(self):
		if(self.comboBox1.currentText() == 'Emissor'):
			self.open_emissor()	
		if(self.comboBox1.currentText() == 'Receptor'):
			self.open_receptor()				
		if(self.comboBox1.currentText() == 'Line coding'):
			self.open_visualization()

	def close(self):
		exit()		

	@staticmethod
	def open_help():		
		Help().exec_()   

	@staticmethod
	def open_about():		
		About().exec_()  

	@staticmethod
	def open_emissor():		
		Emissor().exec_()  

	@staticmethod
	def open_receptor():		
		Receptor().exec_() 

	@staticmethod
	def open_visualization():		
		Visualization().exec_() 



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())