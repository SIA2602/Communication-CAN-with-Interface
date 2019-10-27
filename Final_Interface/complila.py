#!/usr/bin/env python3

import sys, os
import sip #usado para deletar o grafico da
import numpy as np

import binascii

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

from returnSerialPort import serialPorts

Ui_MainWindow, QtBaseClass = uic.loadUiType("principal.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    
	def __init__(self, parent=None):

		QMainWindow.__init__(self, parent=parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.x = []
		self.y = []
		self.binario = []
		self.listaPortas = []

		#variaveis para a resolucao da tela
		self.width = 1080
		self.height = 1000
		self.height_main = 500
		self.controle = False #variavel que controla a exclusao do grafico		

		self.timer = QTimer(self)	

		self.actions()
		self.incializationMain()	
		self.createGraph()		
		#caso escolha a opcao ASCII
		self.pushButton1.clicked.connect(self.optionASCII)
		self.pushButton6.clicked.connect(self.browseASCII)
		#fixando o tamanho da janela inicial
		self.resize(self.width, self.height_main)		
		self.events()

		self.timer.setInterval(100)
		self.timer.start()		

	def events(self):
		self.timer.timeout.connect(self.update)

	def selectSerialPort(self):		
		#deixando menu de opcoes disponiveis
		self.label1.setEnabled(not False)
		self.label1.setText("Select an Option to Emissor or Receptor")		
		self.pushButton1.setEnabled(not False)
		self.pushButton2.setEnabled(not False)
		self.pushButton3.setEnabled(not False)

	def unselectSerialPort(self):		
		return

	def recebePortasSeriais(self):		
		self.listaPortas = serialPorts()		

	def activateMain(self):
		#voltando a habilitar serial
		self.select.setEnabled(not False)
		self.select.clear()
		self.select.removeAction(self.serialPort)				
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
		self.scrollArea1.setHidden(not False)
		self.scrollArea2.setHidden(not False)

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

		#apagando grafico
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

		#criando menu da porta serial		
		self.select.addAction(self.serialPort)			
		
	def actions(self):	
		#carregando porta serial
		self.recebePortasSeriais()
		#print self.listaPortas			
		if(len(self.listaPortas) > 0): self.serialPort = QAction("&"+self.listaPortas[0], self, triggered=self.selectSerialPort)	
		else: self.serialPort = QAction("&no serial ports", self, triggered=self.unselectSerialPort)	
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
		self.scrollArea1.setHidden(not False)
		self.scrollArea2.setHidden(not False)

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
		self.scrollArea1.setHidden(False)
		self.scrollArea2.setHidden(False)	

	def optionReceiveASCII(self):
		#ajustando janela
		self.resize(self.width, self.height_main)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)

		self.label3.setHidden(not False)
		self.lineEdit1.setHidden(not False)
		self.comboBox2.setHidden(not False)
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)

		#mostrando itens pertencentes ao menu
		self.label2.setHidden(False)		
		self.label10.setHidden(False)		
		self.comboBox1.setHidden(False)				
		self.checkBox1.setHidden(False)		

	def optionASCII(self):
		#por seguranca deixando menu da serial desabilitado
		self.select.setEnabled(False)						
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

	def atualizaOpcoesASCII(self):		
		if(self.comboBox2.count() == 0):
			self.comboBox2.clear()
			self.comboBox2.addItem("Selecione")	
			self.comboBox2.addItem("Entrada em Texto")	
			self.comboBox2.addItem("Entrada em Arquivo")

		elif(self.comboBox2.currentText() == "Selecione"):
			self.lineEdit1.setHidden(not False)	
			self.label2.setHidden(not False)
			self.label3.setHidden(not False)
			self.pushButton6.setHidden(not False)

		elif(self.comboBox2.currentText() == "Entrada em Texto"):
			self.lineEdit1.setHidden(False)	
			self.label2.setHidden(False)	
			self.label3.setHidden(False)
			self.pushButton6.setHidden(not False)
		

		elif(self.comboBox2.currentText() == "Entrada em Arquivo"):
			self.lineEdit1.setHidden(False)	
			self.label2.setHidden(False)
			self.label3.setHidden(False)
			self.pushButton6.setHidden(False)

		else:
			self.lineEdit1.setHidden(not False)	
			self.label2.setHidden(not False)
			self.label3.setHidden(not False)				
			self.pushButton6.setHidden(not False)	

	def browseASCII(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
		with open(filename[0], 'r') as f:
			file_text = f.read()
			self.lineEdit1.setText(file_text)

	def printColor(self):
		if(self.comboBox4.currentText() == 'blue'):
			return 'b'
		if(self.comboBox4.currentText() == 'cian'):
			return 'c'
		elif(self.comboBox4.currentText() == 'yellow'):
			return 'y'
		elif(self.comboBox4.currentText() == 'pink'):
			return 'm'
		elif(self.comboBox4.currentText() == 'green'):
			return 'g'
		elif(self.comboBox4.currentText() == 'red'):
			return 'r'
		elif(self.comboBox4.currentText() == 'white'):
			return 'white'
		elif(self.comboBox4.currentText() == 'purple'):
			return 'purple'
		elif(self.comboBox4.currentText() == 'orange'):
			return 'orange'
		return 'white'

	def linesWidth(self):		
		self.label9.setNum(self.horizontalSlider1.value()/20.)
		return self.horizontalSlider1.value()/20.

	def clearGrafico(self):
		self.graphLayout.removeWidget(self.canvas)
		sip.delete(self.canvas)
		self.canvas = None
		self.graphLayout.removeWidget(self.toolbar)
		sip.delete(self.toolbar)
		self.toolbar = None
		self.controle = False

	def createGraph(self):  
		if self.checkBox1.isChecked():      
			self.figure = plt.figure()
			self.canvas = FigureCanvas(self.figure)
			self.toolbar = NavigationToolbar(self.canvas, self)
			self.graphLayout.addWidget(self.canvas)
			self.graphLayout.addWidget(self.toolbar)
			self.controle = True		

	#apenas para teste do grafico
	def plot(self):
		self.figure.clear()				
		self.ax = self.figure.add_subplot(111)
		self.ax.step(self.x, self.y, color=self.printColor(), linewidth=self.linesWidth()) #opcao ativa imprime grafico	
		self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
		self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))		
		self.ax.xaxis.grid(color='gray', linestyle='--', linewidth=0.5)
		self.ax.xaxis.grid(self.checkBox3.isChecked())	
		self.ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)			
		self.ax.yaxis.grid(self.checkBox2.isChecked())
		self.ax.set_facecolor((39./256.,40./256.,34./256.))	
		self.figure.set_facecolor((39./256.,40./256.,34./256.))
		color = "white"	
		self.ax.spines['bottom'].set_color(color)
		self.ax.spines['top'].set_color(color)
		self.ax.spines['left'].set_color(color)
		self.ax.spines['right'].set_color(color)
		for t in self.ax.xaxis.get_ticklines(): t.set_color(color)
		for t in self.ax.yaxis.get_ticklines(): t.set_color(color)
		for t in self.ax.xaxis.get_ticklines(): t.set_color(color)
		for t in self.ax.yaxis.get_ticklines(): t.set_color(color)
		for label in self.ax.get_yticklabels():
			label.set_color(color)
		for label in self.ax.get_xticklabels():
			label.set_color(color)
		self.canvas.draw()	

	#faz o controle tanto das opcoes quanto do tamanho da tela quando o grafico for solicitado
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

	def update(self):
		if(self.comboBox3.currentText() == 'NRZ'): self.plot_NRZ()	
		if(self.comboBox3.currentText() == 'NRZ-L'): self.plot_NRZ_L()
		if(self.comboBox3.currentText() == 'NRZ-I'): self.plot_NRZ_I()
		if self.controle == True: self.plot()
		self.checkBoxGraph()
		self.gravaMensagem()	
		self.actions()	
		self.atualizaOpcoesASCII()		

	def gravaMensagem(self):
		global texto		

		if(self.lineEdit1.text() != ""):			 			
			texto = self._hex_to_binary(self._word_to_hex(self.lineEdit1.text()))	
			self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista
			#print self.binario			
			self.label2.setText(texto)	

	def ASCII_to_Bin(self, texto):		
		return bin(int(binascii.hexlify(texto), 16))	

	def plot_NRZ(self):					
		#valores para grafico	
		if(self.lineEdit1.text() != "" and len(self.binario) > 0):	
			self.y = self.binario
			self.y = [self.y[0]] + self.y
			self.x = [ i for i in range(len(self.y)) ]

	@staticmethod
	def return_bin(value): #dado um int bin eh retornado uma lista dos valores
		return [int(i) for i in value]

	@staticmethod
	def _word_to_hex(word):
		values = ''
		for letter in word:
			values += '{:2x}'.format(ord(letter))
		return values

	@staticmethod
	def _hex_to_binary(hex_):
		try:
			values = ""
			for hex_char in hex_:
					values += "{:0=4b}".format(int(hex_char, 16))
		except ValueError:
			return None
		return values


	
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())