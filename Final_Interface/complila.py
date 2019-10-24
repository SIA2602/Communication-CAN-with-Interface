#!/usr/bin/env python3

import sys
import numpy as np

from PIL import Image, ImageFilter

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, qApp, QFileDialog, QApplication

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import sip

Ui_MainWindow, QtBaseClass = uic.loadUiType("principal.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    
	def __init__(self, parent=None):

		QMainWindow.__init__(self, parent=parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		#variaveis para a resolucao da tela
		self.width = 1080
		self.height = 900
		self.height_main = 350
		self.controle = False

		self.actions()
		self.incializationMain()		

		#caso escolha a opcao ASCII
		self.pushButton1.clicked.connect(self.optionASCII)
		#fixando o tamanho da janela inicial
		self.resize(self.width, self.height_main)

		self.timer = QTimer(self)	
		self.events()
		self.timer.setInterval(300)
		self.timer.start()		

	def events(self):		
		self.timer.timeout.connect(self.checkBoxGraph)	

	def serialPort(self):
		#deixando menu de opcoes disponiveis
		self.label1.setEnabled(not False)
		self.label1.setText("Select an Option to Emissor or Receptor")		
		self.pushButton1.setEnabled(not False)
		self.pushButton2.setEnabled(not False)
		self.pushButton3.setEnabled(not False)

	def activateMain(self):	
		#fixando o tamanho da janela inicial
		self.resize(self.width, self.height_main)
		#colocando opcoes do menu principal visiveis
		self.label1.setText("Select an Option to Emissor or Receptor")
		self.label1.setHidden(False)		
		self.pushButton1.setHidden(False)
		self.pushButton2.setHidden(False)
		self.pushButton3.setHidden(False)
		#deixando menu de opcoes indisponiveis ate ser escolhida a porta serial
		self.pushButton1.setEnabled(False)
		self.pushButton2.setEnabled(False)
		self.pushButton3.setEnabled(False)		
		#ocultando itens que nao pertencem ao menu principal		
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)

		self.label2.setHidden(not False)
		self.label3.setHidden(not False)
		self.lineEdit1.setHidden(not False)
		self.comboBox1.setHidden(not False)
		self.comboBox2.setHidden(not False)		
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)
		self.checkBox1.setHidden(not False)

		self.label4.setHidden(not False)
		self.label5.setHidden(not False)
		self.label6.setHidden(not False)
		self.label7.setHidden(not False)
		self.label8.setHidden(not False)
		self.label9.setHidden(not False)
		self.label10.setHidden(not False)		
		self.comboBox3.setHidden(not False)
		self.comboBox4.setHidden(not False)
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)
		self.checkBox2.setHidden(not False)
		self.checkBox3.setHidden(not False)
		self.horizontalSlider1.setHidden(not False)

		if (self.checkBox1.isChecked() and self.controle == True):
			#tirando a opcao de esta ativado
			self.checkBox1.setChecked(False)
			#apagando grafico caso esteja ativado
			self.graphLayout.removeWidget(self.canvas)
			sip.delete(self.canvas)
			self.canvas = None
			self.graphLayout.removeWidget(self.toolbar)
			sip.delete(self.toolbar)
			self.toolbar = None
			self.controle = False
		
	def actions(self):
		self.serialPort = QAction("&vazio", self, triggered=self.serialPort)
		self.Main = QAction("&Main...", self, shortcut="Ctrl+M", triggered=self.activateMain)
	
	def incializationMain(self):
		#ativando main
		#deixando menu de opcoes indisponiveis ate ser escolhida a porta serial
		self.pushButton1.setEnabled(False)
		self.pushButton2.setEnabled(False)
		self.pushButton3.setEnabled(False)		
		#ocultando itens que nao pertencem ao menu principal		
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)

		self.label2.setHidden(not False)
		self.label3.setHidden(not False)
		self.lineEdit1.setHidden(not False)
		self.comboBox1.setHidden(not False)
		self.comboBox2.setHidden(not False)		
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)
		self.checkBox1.setHidden(not False)

		self.label4.setHidden(not False)
		self.label5.setHidden(not False)
		self.label6.setHidden(not False)
		self.label7.setHidden(not False)
		self.label8.setHidden(not False)
		self.label9.setHidden(not False)
		self.label10.setHidden(not False)		
		self.comboBox3.setHidden(not False)
		self.comboBox4.setHidden(not False)
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)
		self.checkBox2.setHidden(not False)
		self.checkBox3.setHidden(not False)
		self.horizontalSlider1.setHidden(not False)
		#criando menu da porta serial
		self.tools = QMenu("&Tools", self)
		self.menuBar().addMenu(self.tools)
		self.tools.addSeparator()
		self.select = self.tools.addMenu(" Select Serial Port ")
		self.select.addAction(self.serialPort)		
		self.tools.addSeparator()
		self.returnMain = self.tools.addMenu(" Return Main ")
		self.returnMain.addAction(self.Main)        
		self.tools.addSeparator()		

	def optionSendASCII(self):
		#ajustando janela
		self.resize(self.width, self.height_main)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)

		#mostrando itens pertencentes ao menu
		self.label2.setHidden(False)
		self.label3.setHidden(False)
		self.label10.setHidden(False)
		self.lineEdit1.setHidden(False)
		self.comboBox1.setHidden(False)
		self.comboBox2.setHidden(False)
		self.pushButton6.setHidden(False)
		self.pushButton7.setHidden(False)
		self.checkBox1.setHidden(False)		

	def optionReceiveASCII(self):
		return

	def optionASCII(self):				
		#apagando Menu anterior
		self.pushButton1.setHidden(not False)
		self.pushButton2.setHidden(not False)
		self.pushButton3.setHidden(not False)		
		#ativando opcoes do proximo menu		
		self.label1.setText("Select an Option to Emissor or Receptor")
		self.pushButton4.setHidden(False)
		self.pushButton5.setHidden(False)
		#caso escolha uma das opcoes disponiveis
		self.pushButton4.clicked.connect(self.optionSendASCII)	
		self.pushButton5.clicked.connect(self.optionReceiveASCII)		

	def clearGrafico(self):
		self.graphLayout.removeWidget(self.canvas)
		sip.delete(self.canvas)
		self.canvas = None
		self.graphLayout.removeWidget(self.toolbar)
		sip.delete(self.toolbar)
		self.toolbar = None
		self.controle = False

	def createGraph(self):        
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		self.graphLayout.addWidget(self.canvas)
		self.graphLayout.addWidget(self.toolbar)
		self.controle = True

	def plot(self):		
		self.figure.clear()				
		self.ax = self.figure.add_subplot(111)
		self.ax.step([0,1,2], [1,2,3]) #opcao ativa imprime grafico
		self.canvas.draw()	

	def checkBoxGraph(self):
		if (self.checkBox1.isChecked() and self.controle == False):			
			self.createGraph() #ativa caixa do grafico	
			self.plot()
			self.label4.setHidden(False)
			self.label5.setHidden(False)
			self.label6.setHidden(False)
			self.label7.setHidden(False)
			self.label8.setHidden(False)
			self.label9.setHidden(False)
			self.label10.setHidden(False)		
			self.comboBox3.setHidden(False)
			self.comboBox4.setHidden(False)
			self.radioButton1.setHidden(False)
			self.radioButton2.setHidden(False)
			self.checkBox2.setHidden(False)
			self.checkBox3.setHidden(False)
			self.horizontalSlider1.setHidden(False)
			#fixando o tamanho da janela inicial
			self.resize(self.width, self.height)

		elif (not(self.checkBox1.isChecked()) and self.controle == True):			
			self.clearGrafico()
			self.label4.setHidden(not False)
			self.label5.setHidden(not False)
			self.label6.setHidden(not False)
			self.label7.setHidden(not False)
			self.label8.setHidden(not False)
			self.label9.setHidden(not False)
			self.comboBox3.setHidden(not False)
			self.comboBox4.setHidden(not False)
			self.radioButton1.setHidden(not False)
			self.radioButton2.setHidden(not False)
			self.checkBox2.setHidden(not False)
			self.checkBox3.setHidden(not False)
			self.horizontalSlider1.setHidden(not False)
			#fixando o tamanho da janela inicial
			self.resize(self.width, self.height_main)

	
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())