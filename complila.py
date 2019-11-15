#!/usr/bin/env python3

import time
import serial
import random

import sys, os
import sip #usado para deletar o grafico
import numpy as np

import binascii

from PIL import Image, ImageFilter

from PyCRC.CRCCCITT import CRCCCITT #CRC para deteccao de erro

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor, QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, qApp, QFileDialog, QApplication, QMdiSubWindow

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from returnSerialPort import serialPorts

from help import Help

Ui_MainWindow, QtBaseClass = uic.loadUiType("principal.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    
	def __init__(self, parent=None):

		QMainWindow.__init__(self, parent=parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		#area exclusiva para a imagem
		self.R = []
		self.G = []
		self.B = []
		self.R_envio = []
		self.G_envio = []
		self.B_envio = []
		#criando o label da imagem
		self.labelIMAGE = QLabel()		
		self.labelIMAGE.setBackgroundRole(QPalette.Base)
		self.labelIMAGE.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		self.labelIMAGE.setScaledContents(True)
		#criando uma area para por o label e configurar sua escala
		self.scrollAreaIMAGE = QScrollArea()
		self.scrollAreaIMAGE.setBackgroundRole(QPalette.Dark)
		self.scrollAreaIMAGE.setWidget(self.labelIMAGE)
		self.scrollAreaIMAGE.setVisible(False)
		#self.mdi = QMdiArea()      	
		self.sub = QMdiSubWindow()
		self.sub.setWidget(self.scrollAreaIMAGE)
		self.sub.resize(400,400)
		self.sub.setWindowTitle("Image Viewer")
		self.mdiArea.addSubWindow(self.sub)
		#criando menus para imagem
		self.createActions()
		self.createMenus()
		#deixando menu grafico indisponivel
		self.fileMenu.setEnabled(False)
		self.viewMenu.setEnabled(False)

		self.x = []
		self.y = []
		self.x_bin = []
		self.y_bin = []
		self.x_noise = []
		self.y_noise = []
		self.binario = []
		self.binario_noise = []		
		self.listaPortas = []	

		#variaveis para a resolucao da tela
		self.width = 1080
		self.height = 950
		self.height_main = 500
		self.controle = False #variavel que controla a exclusao do grafico
		self.controleReceive = False	
		self.controleSend = False	

		self.timer = QTimer(self)	

		self.actions()
		self.incializationMain()	
		self.createGraph()		
		#caso escolha a opcao ASCII
		self.pushButton1.clicked.connect(self.optionASCII)
		self.pushButton2.clicked.connect(self.optionIMAGE)
		self.pushButton6.clicked.connect(self.browseASCII)
		self.pushButton7.clicked.connect(self.lerEntrada)
		self.pushButton8.clicked.connect(self.lerEntradaRecebida)
		self.pushButton10.clicked.connect(self.lerEntradaIMG)
		self.pushButton11.clicked.connect(self.lerEntradaRecebidaIMG)
		self.pushButtonCRC.clicked.connect(self.verificaCRC_ASCII)
		self.pushButtonCRC_IMG.clicked.connect(self.verificaCRC_IMG)
		#fixando o tamanho da janela inicial
		self.resize(self.width, self.height_main)		
		self.events()

		self.timer.setInterval(300)
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
		#deixando desativado
		self.checkBoxASCII.setChecked(False)
		self.checkBoxIMAGE.setChecked(False)

		#limpando comboBox
		self.comboBox2.clear()
		self.comboBox2.addItem("Selecione")
		self.comboBox2.addItem("Entrada em Texto")
		self.comboBox2.addItem("Entrada em Arquivo")		

		#limpando coisas digitadas
		self.lineEdit1.clear()
		self.label2.clear()			
		self.labelIMAGE.clear()
		self.x = []
		self.y = []
		self.R = []
		self.G = []
		self.B = []
		self.R_envio = []
		self.G_envio = []
		self.B_envio = []
		self.texto = []
		self.binario = []
		#deixando menu grafico indisponivel
		self.visualizar_grafico.setEnabled(False)		
		self.fileMenu.setEnabled(False)
		self.viewMenu.setEnabled(False)
		#variavel de controle para a func atualizaOpcoesASCII
		self.controleSend = False
		self.controleReceive = False
		#voltando a habilitar serial e apagando menu
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

		self.pushButton10.setHidden(not False)
		self.pushButton11.setHidden(not False)

		self.label2.setHidden(not False)	
		self.label2.setStyleSheet('color: black')	
		self.lineEdit1.setHidden(not False)
		self.comboBox1.setHidden(not False)
		self.comboBox2.setHidden(not False)		
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)
		self.pushButton8.setHidden(not False)
		self.checkBox6.setHidden(not False)
		self.checkBox1.setHidden(not False)
		self.scrollArea1.setHidden(not False)		
		self.mdiArea.setHidden(not False)
		self.labelPORCENTAGEM.setHidden(not False)
		self.spinBoxPORCENTAGEM.setHidden(not False)
		self.labelRGB.setHidden(not False)
		self.radioButtonR.setHidden(not False)
		self.radioButtonG.setHidden(not False)
		self.radioButtonB.setHidden(not False)
		self.pushButtonCRC.setHidden(not False)		
		self.pushButtonCRC_IMG.setHidden(not False)
		self.pushButtonCRC.setEnabled(False)
		self.pushButtonCRC_IMG.setEnabled(False)		
		self.labelDeteccao1.setHidden(not False)
		self.labelDeteccao2.setHidden(not False)		
		
		self.label5.setHidden(not False)
		self.label6.setHidden(not False)
		self.label7.setHidden(not False)
		self.label8.setHidden(not False)
		self.label9.setHidden(not False)
		self.label10.setHidden(not False)	
		self.label11.setHidden(not False)
		self.label12.setHidden(not False)	
		self.spinBox1.setHidden(not False)	
		self.comboBox3.setHidden(not False)
		self.comboBox4.setHidden(not False)
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)
		self.checkBox2.setHidden(not False)
		self.checkBox3.setHidden(not False)
		self.checkBox4.setHidden(not False)
		self.checkBox5.setHidden(not False)
		self.checkBoxIMAGE.setHidden(not False)
		self.checkBoxASCII.setHidden(not False)
		self.horizontalSlider1.setHidden(not False)
		self.horizontalSlider2.setHidden(not False)

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

		#recriando menu da porta serial		
		self.select.addAction(self.serialPort)	

	def functionViewsGraph(self):
		#deixando ativado
		self.checkBox1.setChecked(not False)
		self.horizontalSlider2.setHidden(False)	

	def functionClearGraph(self):
		#tirando a opcao de esta ativado
		self.checkBox1.setChecked(False)
		self.horizontalSlider2.setHidden(not False)	

	def functionViewPainel(self):
		self.label5.setHidden(False)
		self.label6.setHidden(False)
		self.label7.setHidden(False)
		self.label8.setHidden(False)
		self.label9.setHidden(False)
		self.label10.setHidden(False)
		self.label11.setHidden(False)	
		self.label12.setHidden(False)	
		self.spinBox1.setHidden(False)		
		self.comboBox3.setHidden(False)
		self.comboBox4.setHidden(False)
		self.radioButton1.setHidden(False)
		self.radioButton2.setHidden(False)
		self.checkBox2.setHidden(False)
		self.checkBox3.setHidden(False)
		self.checkBox4.setHidden(False)
		if(self.controleReceive == False):
			self.checkBox5.setHidden(False)
		else:
			self.checkBox5.setHidden(True)
		self.horizontalSlider1.setHidden(False)
		
	def functionClearPainel(self):
		self.label5.setHidden(not False)
		self.label6.setHidden(not False)
		self.label7.setHidden(not False)
		self.label8.setHidden(not False)
		self.label9.setHidden(not False)
		self.label11.setHidden(not False)
		self.label12.setHidden(not False)		
		self.spinBox1.setHidden(not False)
		self.comboBox3.setHidden(not False)
		self.comboBox4.setHidden(not False)
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)
		self.checkBox2.setHidden(not False)
		self.checkBox3.setHidden(not False)
		self.checkBox4.setHidden(not False)
		self.checkBox5.setHidden(not False)
		self.horizontalSlider1.setHidden(not False)			

	@staticmethod
	def open_help():		
		Help().exec_()  
		
	def actions(self):	
		#carregando porta serial
		self.recebePortasSeriais()
		#print self.listaPortas			
		if(len(self.listaPortas) > 0): self.serialPort = QAction("&"+self.listaPortas[0], self, triggered=self.selectSerialPort)	
		else: self.serialPort = QAction("&no serial ports", self, triggered=self.unselectSerialPort)
		self.Main = QAction("&Main...", self, shortcut="Ctrl+M", triggered=self.activateMain)
		self.viewGraph = QAction("&View Graph", self, shortcut="Ctrl+G", triggered=self.functionViewsGraph)	
		self.clearGraph = QAction("&Clear Graph", self, shortcut="Ctrl+K", triggered=self.functionClearGraph)
		self.viewPainel = QAction("&View customization panel", self, shortcut="Ctrl+P", triggered=self.functionViewPainel)	
		self.clearPainel = QAction("&Clear customization panel", self, shortcut="Ctrl+L", triggered=self.functionClearPainel)
		self.instrucoes = QAction("&Uso do Software", self, shortcut="Ctrl+H", triggered=self.open_help)
	
	def incializationMain(self):
		#variavel de controle para a func atualizaOpcoesASCII
		self.controleSend = False
		self.controleReceive = False	
		#ativando main
		#deixando menu de opcoes indisponiveis ate ser escolhida a porta serial
		self.pushButton1.setEnabled(False)
		self.pushButton2.setEnabled(False)
		self.pushButton3.setEnabled(False)		
		#ocultando itens que nao pertencem ao menu principal		
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)

		self.pushButton10.setHidden(not False)
		self.pushButton11.setHidden(not False)

		self.label2.setHidden(not False)		
		self.lineEdit1.setHidden(not False)
		self.comboBox1.setHidden(not False)
		self.comboBox2.setHidden(not False)		
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)
		self.pushButton8.setHidden(not False)
		self.checkBox6.setHidden(not False)
		self.checkBox1.setHidden(not False)
		self.scrollArea1.setHidden(not False)		
		self.mdiArea.setHidden(not False)
		self.labelPORCENTAGEM.setHidden(not False)
		self.spinBoxPORCENTAGEM.setHidden(not False)
		self.labelRGB.setHidden(not False)
		self.radioButtonR.setHidden(not False)
		self.radioButtonG.setHidden(not False)
		self.radioButtonB.setHidden(not False)
		self.pushButtonCRC.setHidden(not False)		
		self.pushButtonCRC_IMG.setHidden(not False)
		self.pushButtonCRC.setEnabled(False)
		self.pushButtonCRC_IMG.setEnabled(False)		
		self.labelDeteccao1.setHidden(not False)
		self.labelDeteccao2.setHidden(not False)
		
		self.label5.setHidden(not False)
		self.label6.setHidden(not False)
		self.label7.setHidden(not False)
		self.label8.setHidden(not False)
		self.label9.setHidden(not False)
		self.label10.setHidden(not False)	
		self.label11.setHidden(not False)
		self.label12.setHidden(not False)	
		self.spinBox1.setHidden(not False)
		self.comboBox3.setHidden(not False)
		self.comboBox4.setHidden(not False)
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)
		self.checkBox2.setHidden(not False)
		self.checkBox3.setHidden(not False)
		self.checkBox4.setHidden(not False)
		self.checkBox5.setHidden(not False)
		self.checkBoxIMAGE.setHidden(not False)
		self.checkBoxASCII.setHidden(not False)
		self.horizontalSlider1.setHidden(not False)
		self.horizontalSlider2.setHidden(not False)
		#criando menu da porta serial
		self.tools = QMenu("&Tools", self)
		self.menuBar().addMenu(self.tools)
		self.tools.addSeparator()

		self.select = self.tools.addMenu(" Select Serial Port ")
		self.select.addAction(self.serialPort)		
		self.tools.addSeparator()

		self.visualizar_grafico = self.tools.addMenu(" Graph ")
		self.visualizar_grafico.addAction(self.viewGraph)
		self.visualizar_grafico.addSeparator()
		self.visualizar_grafico.addAction(self.clearGraph)
		self.visualizar_grafico.addSeparator()
		self.visualizar_grafico.addAction(self.viewPainel)
		self.visualizar_grafico.addSeparator()
		self.visualizar_grafico.addAction(self.clearPainel)		
		#deixando menu grafico indisponivel
		self.visualizar_grafico.setEnabled(False)				

		self.tools.addSeparator()		
		self.returnMain = self.tools.addMenu(" Return Main ")
		self.returnMain.addAction(self.Main)        
		self.tools.addSeparator()

		#criando menu help
		self.help = QMenu("&Help", self)
		self.menuBar().addMenu(self.help)
		self.help.addSeparator()

		self.selectHelp = self.help.addMenu(" Instrucoes de Uso ")
		self.selectHelp.addAction(self.instrucoes)		
		self.help.addSeparator()		

	def optionSendASCII(self):
		#deixando ativado ASCII e sativando Imagem
		self.checkBoxASCII.setChecked(not False)
		self.checkBoxIMAGE.setChecked(False)
		#variavel de controle para a func atualizaOpcoesASCII	
		self.controleSend = True	
		#ajustando janela
		self.resize(self.width, self.height_main)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)
		self.mdiArea.setHidden(not False)
		self.checkBoxIMAGE.setHidden(not False)
		self.labelPORCENTAGEM.setHidden(not False)
		self.spinBoxPORCENTAGEM.setHidden(not False)
		self.labelRGB.setHidden(not False)
		self.radioButtonR.setHidden(not False)
		self.radioButtonG.setHidden(not False)
		self.radioButtonB.setHidden(not False)
		self.pushButton8.setHidden(not False)
		self.pushButton10.setHidden(not False)
		self.pushButton11.setHidden(not False)

		#mostrando itens pertencentes ao menu
		self.label2.setHidden(False)		
		self.label10.setHidden(False)
		self.lineEdit1.setHidden(False)
		self.comboBox1.setHidden(False)
		self.comboBox2.setHidden(False)
		self.pushButton6.setHidden(False)
		self.pushButton7.setHidden(False)
		self.checkBox6.setHidden(False)
		self.checkBox1.setHidden(not False)	
		self.scrollArea1.setHidden(False)		

	def optionSendIMAGE(self):
		#deixando ativado Imagem e desativando ASCII
		self.checkBoxIMAGE.setChecked(not False)
		self.checkBoxASCII.setChecked(False)		
		#deixando menu grafico disponivel
		self.fileMenu.setEnabled(not False)
		self.viewMenu.setEnabled(not False)
		#ajustando janela
		self.resize(self.width, self.height)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)					
		self.lineEdit1.setHidden(not False)		
		self.comboBox2.setHidden(not False)
		self.pushButton6.setHidden(not False)		
		self.checkBox1.setHidden(not False)		
		self.checkBoxIMAGE.setHidden(not False)
		self.pushButton8.setHidden(not False)

		#mostrando itens pertencentes ao menu	
		self.scrollArea1.setHidden(False)
		self.label2.setHidden(False)
		self.mdiArea.setHidden(False)	
		self.label10.setHidden(False)		
		self.comboBox1.setHidden(False)			
		self.pushButton7.setHidden(not False)
		self.pushButton10.setHidden(False)
		self.pushButton11.setHidden(not False)
		self.checkBox6.setHidden(False)		
		self.labelPORCENTAGEM.setHidden(False)
		self.spinBoxPORCENTAGEM.setHidden(False)
		self.labelRGB.setHidden(False)
		self.radioButtonR.setHidden(False)
		self.radioButtonG.setHidden(False)
		self.radioButtonB.setHidden(False)				

	def optionReceiveASCII(self):
		#variavel de controle para a func atualizaOpcoesASCII
		self.controleReceive = True
		#ajustando janela
		self.resize(self.width, self.height_main)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)
		self.pushButton10.setHidden(not False)
		self.pushButton11.setHidden(not False)

		self.mdiArea.setHidden(not False)
		self.comboBox2.setHidden(not False)
		self.pushButton6.setHidden(not False)
		self.pushButton7.setHidden(not False)
		self.checkBox6.setHidden(not False)
		self.checkBoxIMAGE.setHidden(not False)
		self.labelPORCENTAGEM.setHidden(not False)
		self.spinBoxPORCENTAGEM.setHidden(not False)
		self.labelRGB.setHidden(not False)
		self.radioButtonR.setHidden(not False)
		self.radioButtonG.setHidden(not False)
		self.radioButtonB.setHidden(not False)	

		#mostrando itens pertencentes ao menu
		self.lineEdit1.setHidden(False)
		self.lineEdit1.setEnabled(False)		
		self.label2.setHidden(False)
		self.scrollArea1.setHidden(False)		
		self.label10.setHidden(False)		
		self.comboBox1.setHidden(False)	
		self.pushButton8.setHidden(False)		
		self.checkBox1.setHidden(not False)		
		self.pushButtonCRC.setHidden(False)		
		self.pushButtonCRC_IMG.setHidden(not False)		
		self.labelDeteccao1.setHidden(False)
		self.labelDeteccao2.setHidden(not False)		

	def optionReceiveIMAGE(self):
		#deixando ativado Imagem e desativando ASCII
		self.checkBoxIMAGE.setChecked(not False)
		self.checkBoxASCII.setChecked(False)		
		#deixando menu grafico disponivel
		self.fileMenu.setEnabled(not False)
		self.viewMenu.setEnabled(not False)
		#ajustando janela
		self.resize(self.width, self.height)
		#ocultando menus que nao pertencem ao menu selecionado		
		self.label1.setHidden(not False)
		self.pushButton4.setHidden(not False)
		self.pushButton5.setHidden(not False)					
		self.lineEdit1.setHidden(not False)		
		self.comboBox2.setHidden(not False)
		self.pushButton6.setHidden(not False)		
		self.checkBox1.setHidden(not False)		
		self.checkBoxIMAGE.setHidden(not False)
		self.pushButton8.setHidden(not False)		

		#mostrando itens pertencentes ao menu	
		self.scrollArea1.setHidden(False)
		self.label2.setHidden(False)
		self.mdiArea.setHidden(False)	
		self.label10.setHidden(False)		
		self.comboBox1.setHidden(False)
		self.pushButton10.setHidden(not False)
		self.pushButton11.setHidden(False)			
		self.pushButton8.setHidden(not False)
		self.checkBox6.setHidden(not False)		
		self.labelPORCENTAGEM.setHidden(not False)
		self.spinBoxPORCENTAGEM.setHidden(not False)
		self.labelRGB.setHidden(not False)
		self.radioButtonR.setHidden(not False)
		self.radioButtonG.setHidden(not False)
		self.radioButtonB.setHidden(not False)
		self.pushButtonCRC_IMG.setHidden(False)		
		self.pushButtonCRC.setHidden(not False)		
		self.labelDeteccao1.setHidden(not False)
		self.labelDeteccao2.setHidden(False)

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

	def optionIMAGE(self):
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
		self.pushButton4.clicked.connect(self.optionSendIMAGE)	
		self.pushButton5.clicked.connect(self.optionReceiveIMAGE)	

	def atualizaOpcoesASCII(self):		
		if(self.controleSend == True):				
			if(self.comboBox2.currentText() == "Selecione"):
				self.lineEdit1.setHidden(not False)	
				self.label2.setHidden(not False)				
				self.pushButton6.setHidden(not False)

			elif(self.comboBox2.currentText() == "Entrada em Texto"):
				self.lineEdit1.setEnabled(not False)
				self.lineEdit1.setHidden(False)	
				self.label2.setHidden(False)					
				self.pushButton6.setHidden(not False)			

			elif(self.comboBox2.currentText() == "Entrada em Arquivo"):
				self.lineEdit1.setEnabled(False)
				self.lineEdit1.setHidden(False)	
				self.label2.setHidden(False)				
				self.pushButton6.setHidden(False)
		if(self.controleSend == True or self.controleReceive == True):
			#deixando menu grafico indisponivel
			self.visualizar_grafico.setEnabled(not False)		

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
			self.figure.subplots_adjust(left=0.070, bottom=0.085, right=0.99, top=0.97, hspace=0.13)
			self.canvas = FigureCanvas(self.figure)
			self.toolbar = NavigationToolbar(self.canvas, self)
			self.graphLayout.addWidget(self.canvas)
			self.graphLayout.addWidget(self.toolbar)
			self.controle = True		

	#apenas para teste do grafico
	def plot(self):
		self.figure.clear()	
		
		if(len(self.x) > 0):
			#controle para imprimir a quantidade de bits desajado
			self.horizontalSlider2.setMaximum(100)	
			value = (self.x[-1] - 19*self.spinBox1.value()/20)*self.horizontalSlider2.value()/99
			start = value - self.spinBox1.value()/20
			end = start + 21*self.spinBox1.value()/20
			#nao deixando ultrapassar o numero maximo de bits para visualizacao
			if(self.spinBox1.value()+1 > len(self.y)): self.spinBox1.setValue(len(self.y))
			else:
				if(self.checkBox4.isChecked() and self.checkBox5.isChecked()): self.ax = self.figure.add_subplot(313)
				elif(self.checkBox4.isChecked() or self.checkBox5.isChecked()): self.ax = self.figure.add_subplot(212)			
				else:
					#primeiro grafico default
					self.ax = self.figure.add_subplot(111)
				#ajustando eixo de visualizacao			
				self.ax.set_xlim(start, end)			
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
				self.ax.set_ylabel(self.comboBox3.currentText(), color=color, size=15)
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

				#caso se deseje o grafico binario	
				if self.checkBox4.isChecked():							
					if self.checkBox5.isChecked(): self.ax1 = self.figure.add_subplot(311)	
					else: self.ax1 = self.figure.add_subplot(211)							
					#ajustando eixo de visualizacao			
					self.ax1.set_xlim(start, end)			
					self.ax1.step(self.x_bin, self.y_bin, color=self.printColor(), linewidth=self.linesWidth()) #opcao ativa imprime grafico	
					self.ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
					self.ax1.xaxis.set_major_locator(MaxNLocator(integer=True))		
					self.ax1.xaxis.grid(color='gray', linestyle='--', linewidth=0.5)
					self.ax1.xaxis.grid(self.checkBox3.isChecked())	
					self.ax1.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)			
					self.ax1.yaxis.grid(self.checkBox2.isChecked())
					self.ax1.set_facecolor((39./256.,40./256.,34./256.))	
					self.figure.set_facecolor((39./256.,40./256.,34./256.))
					color = "white"	
					self.ax1.set_ylabel("Binario", color=color, size=15)
					self.ax1.spines['bottom'].set_color(color)
					self.ax1.spines['top'].set_color(color)
					self.ax1.spines['left'].set_color(color)
					self.ax1.spines['right'].set_color(color)
					for t in self.ax1.xaxis.get_ticklines(): t.set_color(color)
					for t in self.ax1.yaxis.get_ticklines(): t.set_color(color)
					for t in self.ax1.xaxis.get_ticklines(): t.set_color(color)
					for t in self.ax1.yaxis.get_ticklines(): t.set_color(color)
					for label in self.ax1.get_yticklabels():
						label.set_color(color)
					for label in self.ax1.get_xticklabels():
						label.set_color(color)	
					#ocultando valores do eixo x				
					self.ax1.set_xticklabels([])		

				#caso se deseje o grafico do ruido	
				if self.checkBox5.isChecked():							
					if self.checkBox4.isChecked(): self.ax2 = self.figure.add_subplot(312)
					else: self.ax2 = self.figure.add_subplot(211)							
					#ajustando eixo de visualizacao			
					self.ax2.set_xlim(start, end)			
					self.ax2.step(self.x_noise, self.y_noise, color=self.printColor(), linewidth=self.linesWidth()) #opcao ativa imprime grafico	
					self.ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
					self.ax2.xaxis.set_major_locator(MaxNLocator(integer=True))		
					self.ax2.xaxis.grid(color='gray', linestyle='--', linewidth=0.5)
					self.ax2.xaxis.grid(self.checkBox3.isChecked())	
					self.ax2.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)			
					self.ax2.yaxis.grid(self.checkBox2.isChecked())
					self.ax2.set_facecolor((39./256.,40./256.,34./256.))	
					self.figure.set_facecolor((39./256.,40./256.,34./256.))
					color = "white"	
					self.ax2.set_ylabel("Ruido", color=color, size=15)
					self.ax2.spines['bottom'].set_color(color)
					self.ax2.spines['top'].set_color(color)
					self.ax2.spines['left'].set_color(color)
					self.ax2.spines['right'].set_color(color)
					for t in self.ax2.xaxis.get_ticklines(): t.set_color(color)
					for t in self.ax2.yaxis.get_ticklines(): t.set_color(color)
					for t in self.ax2.xaxis.get_ticklines(): t.set_color(color)
					for t in self.ax2.yaxis.get_ticklines(): t.set_color(color)
					for label in self.ax2.get_yticklabels():
						label.set_color(color)
					for label in self.ax2.get_xticklabels():
						label.set_color(color)	
					#ocultando valores do eixo x				
					self.ax2.set_xticklabels([])	

				self.canvas.draw()	
		else: return

	#faz o controle tanto das opcoes quanto do tamanho da tela quando o grafico for solicitado
	def checkBoxGraph(self):
		if (self.checkBox1.isChecked() and self.controle == False):			
			self.createGraph() #ativa caixa do grafico	
			self.plot()				
			#fixando o tamanho da janela inicial
			self.resize(self.width, self.height)

		elif (not(self.checkBox1.isChecked()) and self.controle == True):			
			self.clearGrafico()				
			#fixando o tamanho da janela inicial
			if (self.checkBoxIMAGE.isChecked()): self.resize(self.width, self.height)	
			else: self.resize(self.width, self.height_main)

	def update(self):
		if(self.comboBox3.currentText() == 'NRZ'): self.plot_NRZ()	
		if(self.comboBox3.currentText() == 'NRZ-L'): self.plot_NRZ_L()
		if(self.comboBox3.currentText() == 'NRZ-I'): self.plot_NRZ_I()
		if self.controle == True: self.plot()
		self.checkBoxGraph()
		self.gravaMensagem()	
		self.actions()	
		if (self.checkBoxASCII.isChecked()): self.atualizaOpcoesASCII()
		if (self.checkBoxIMAGE.isChecked()): self.convertIMAGE_to_Binary_in_label()
		if (self.lineEdit1.text() != ""):
			self.pushButtonCRC.setEnabled(not False)
		if (self.label2.text() != ""):
			self.pushButtonCRC_IMG.setEnabled(not False)		

	def gravaMensagem(self):
		global texto			

		if(self.lineEdit1.text() != ""):			 			
			texto = self._hex_to_binary(self._word_to_hex(self.lineEdit1.text()))	
			self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista

			if(len(self.binario) != len(self.binario_noise)):
				self.lista_ASCII_error = [i for i in self.lineEdit1.text()]
				#print self.lista_ASCII_error
				self.noise_ASCII(10)
				texto = self._hex_to_binary(self._word_to_hex(self.lista_ASCII_error))				
				self.binario_noise = self.return_bin(texto) #pegando valores binario e jogando em uma lista
				#print self.binario_noise
				#print self.binario											
			self.label2.setText(texto)		

	def ASCII_to_Bin(self, texto):		
		return bin(int(binascii.hexlify(texto), 16))	

	def plot_NRZ(self):	
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)	#oculta opcao do bit anterior				
		#valores para grafico	
		if((self.lineEdit1.text() != "" and len(self.binario) > 0) or (self.checkBoxIMAGE.isChecked() and len(self.binario) > 0)) :	
			self.y = [int(i) for i in self.binario]
			self.y = [self.y[0]] + self.y
			self.x = [ i for i in range(len(self.y)) ]

			self.y_bin = [int(i) for i in self.binario]
			self.y_bin = [self.y_bin[0]] + self.y_bin
			self.x_bin = [ i for i in range(len(self.y_bin)) ]

			self.y_noise = [int(i) for i in self.binario_noise]
			self.y_noise = [self.y_noise[0]] + self.y_noise
			self.x_noise = [ i for i in range(len(self.y_noise))]

	def plot_NRZ_L(self):
		#valores para grafico		
		self.plot_NRZ()

		for i in range(len(self.y)):
			if(self.y[i] == 0): self.y[i] = 1
			elif(self.y[i] == 1): self.y[i] = -1	
		self.x = [ i for i in range(len(self.y)) ]	

	def plot_NRZ_I_1(self):		
		self.plot_NRZ()
		self.radioButton1.setHidden(not True)
		self.radioButton2.setHidden(not True)
		for i in range(1,len(self.y)):	
			if(self.y[i] == 1):
				if(self.y[i-1] == 0): self.y[i] = 1
				else: self.y[i] = 0
			else: self.y[i] = self.y[i-1]

		for i in range(len(self.y)):
			if(self.y[i] == 0): self.y[i] = -1 

	def plot_NRZ_I(self):
		
		self.radioButton1.setHidden(not True)
		self.radioButton2.setHidden(not True)
			
		if(self.radioButton1.isChecked()):
			self.plot_NRZ_I_1()

		if(self.radioButton2.isChecked()):
			self.plot_NRZ_I_1()	
			for i in range(len(self.y)):
				if(self.y[i] == 1): self.y[i] = -1
				else: self.y[i] = 1 

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

	#funcoes apenas para a visualizacao da imagem
	def zoomIn(self):
		self.scaleImage(1.25)

	def zoomOut(self):
		self.scaleImage(0.8)

	def normalSize(self):
		self.labelIMAGE.adjustSize()
		self.scaleFactor = 1.0

	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollAreaIMAGE.setWidgetResizable(fitToWindow)
		if not fitToWindow:
			self.normalSize()

		self.updateActions()

	def open(self):
		#limpando tela
		self.label2.clear()			
		self.labelIMAGE.clear()
		self.x = []
		self.y = []
		self.R = []
		self.G = []
		self.B = []
		self.R_envio = []
		self.G_envio = []
		self.B_envio = []
		self.texto = []		
		self.x_noise = []
		self.y_noise = []		
		self.binario_noise = []

		if (self.checkBoxIMAGE.isChecked()):		    
		    options = QFileDialog.Options()
		    # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
		    fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '','Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)

		    if(fileName != ' '):		    	
		        image = QImage(fileName)		        
		        if image.isNull():
		            QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
		            return		            
		        self.labelIMAGE.setPixmap(QPixmap.fromImage(image))
		        self.scaleFactor = 1.0

		        self.scrollAreaIMAGE.setVisible(True)
		        self.fitToWindowAct.setEnabled(True)
		        self.updateActions()

	            if not self.fitToWindowAct.isChecked():
		            self.labelIMAGE.adjustSize()	           
		        #carregando a imagem e salvando em lista R,G e B
	            im = Image.open(fileName)
	            rgb_im = im.convert('RGB')
	            self.image_width = image.width()
	            self.image_height = image.height()
	            #print image_width, image_height 	            
	            #guardando imagem de impressao inicial na tela          
	            for i in range(0,self.image_width):
	            	for j in range(0,self.image_height):
						r,g,b = rgb_im.getpixel((i,j))
						#print i,j,r,g,b
						self.R_envio.append(r)
						self.G_envio.append(g)
						self.B_envio.append(b)						
						#para visualizacao grafica
						if(i < int((self.spinBoxPORCENTAGEM.value()/100.)*self.image_width)):
							if(j < int((self.spinBoxPORCENTAGEM.value()/100.)*self.image_height)):	            		
								self.R.append(r)
								if(r == 0): 
									self.R.append(r)
								self.G.append(g)
								if(g == 0): 
									self.G.append(g)
								self.B.append(b)
								if(b == 0): 
									self.B.append(b)								      		
	            I = np.array(im) #convetendo em vertor numpy	            
	            arr2im = Image.fromarray(I) #voltando para imagem   
	            #arr2im.show() #imprimindo imagem
	            #print self.return_bin(self._hex_to_binary(hex(R[0])[2:]))	                       

	def convertIMAGE_to_Binary_in_label(self):		
		if(self.radioButtonR.isChecked()):
			if(len(self.R) > 0):
				texto = self._hex_to_binary([hex(x)[2:] for x in self.R])	
				self.binario = []
				self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista
				#print self.binario			
				self.label2.setText(texto)
				self.plot_NRZ()
		elif(self.radioButtonG.isChecked()):
			if(len(self.G) > 0):
				texto = self._hex_to_binary([hex(x)[2:] for x in self.G])
				self.binario = []	
				self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista
				#print self.binario			
				self.label2.setText(texto)
				self.plot_NRZ()
		elif(self.radioButtonB.isChecked()):
			if(len(self.B) > 0):
				texto = self._hex_to_binary([hex(x)[2:] for x in self.B])	
				self.binario = []
				self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista
				#print self.binario			
				self.label2.setText(texto)
				self.plot_NRZ() 

	def functionViewsImage(self):
		#ajustando janela
		if(self.checkBoxIMAGE.isChecked()): self.resize(self.width, self.height)
		else: self.resize(self.width, self.height_main)		
		self.mdiArea.setHidden(False)

	def functionClearImage(self):
		#ajustando janela
		if(self.checkBox1.isChecked()): self.resize(self.width, self.height)
		else: self.resize(self.width, self.height_main)
		self.mdiArea.setHidden(not False)               	               

	def createActions(self):
		self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
		self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
		self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
		self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
		self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
		self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
		self.viewImage = QAction("&View Image", self, shortcut="Ctrl+I", triggered=self.functionViewsImage)	
		self.clearImage = QAction("&Clear Image", self, shortcut="Ctrl+U", triggered=self.functionClearImage)

	def createMenus(self):
		self.fileMenu = QMenu("&File", self)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.openAct)        
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.exitAct)
		self.fileMenu.addSeparator()

		self.viewMenu = QMenu("&View", self)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.viewImage)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.clearImage)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.zoomInAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.zoomOutAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.normalSizeAct)
		self.viewMenu.addSeparator()
		self.viewMenu.addAction(self.fitToWindowAct)
		self.viewMenu.addSeparator()

		self.menuBar().addMenu(self.fileMenu)
		self.menuBar().addMenu(self.viewMenu)

	def updateActions(self):
		self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
		self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

	def scaleImage(self, factor):
		self.scaleFactor *= factor
		self.labelIMAGE.resize(self.scaleFactor * self.labelIMAGE.pixmap().size())

		self.adjustScrollBar(self.scrollAreaIMAGE.horizontalScrollBar(), factor)
		self.adjustScrollBar(self.scrollAreaIMAGE.verticalScrollBar(), factor)

		self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
		self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

	def adjustScrollBar(self, scrollBar, factor):
		scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep() / 2)))

	#funcoes para o emissor em ASCII
	def enviaCaracter(self, PARAM_CARACTER):
		# Time entre a conexao serial e o tempo para escrever (enviar algo)
		time.sleep(0.2)
		self.comport.write(str.encode(PARAM_CARACTER))		

	def lerEntrada(self):		
		# Iniciando conexao serial		
		self.comport = serial.Serial(self.listaPortas[0], self.comboBox1.currentText(), timeout=0.2, write_timeout=0.2)			
		#PARAM_STRING="Ola como vai? Oi estou bem, e voce?" #recebe a entrada	
		value_CRC = CRCCCITT().calculate(str(self.lineEdit1.text())) #calculando valor CRC				

		if(self.checkBox6.isChecked()):	
			PARAM_STRING = "   " + ">" + str(value_CRC) + ">" + str(''.join(self.lista_ASCII_error)) + "<" + "   "
		else:
			PARAM_STRING = "   " + ">" + str(value_CRC) + ">" + str(self.lineEdit1.text()) + "<" + "   "			
		
		if(len(PARAM_STRING) > 0):				
			for i in range(0,len(PARAM_STRING)):
				self.enviaCaracter(PARAM_STRING[i])				
		# Fechando conexao serial
		self.comport.close()

	#funcoes para o receptor em ASCII
	def recebeCaracter(self):
		controle_entrada = 0		
		self.myText = []
		self.myCRC = []
		# Time entre a conexao serial e o tempo para escrever (enviar algo)
		time.sleep(0.2)
		VALUE_SERIAL=self.comport.readline()
		while(VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("<")):

			if(VALUE_SERIAL.encode("hex")[:2] == self._word_to_hex(">")): controle_entrada += 1
			elif(controle_entrada == 1 and (VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("\n"))): self.myCRC += VALUE_SERIAL[:1]
			elif(controle_entrada == 2 and (VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("\n"))): self.myText += VALUE_SERIAL[:1] 	
			# Time entre a conexao serial e o tempo para escrever (enviar algo)
			time.sleep(0.2)
			VALUE_SERIAL=self.comport.readline()		
			#print VALUE_SERIAL
		self.myCRC = int(''.join(self.myCRC))	
		#print myText
		#print CRCCCITT().calculate(str(''.join(myText)))
		self.label2.setStyleSheet('color: black')					
		return(''.join(self.myText))		

	def lerEntradaRecebida(self):		
		# Iniciando conexao serial		
		self.comport = serial.Serial(self.listaPortas[0], self.comboBox1.currentText(), timeout=0.2, write_timeout=0.2)				
		Frase = self.recebeCaracter()			
		self.lineEdit1.setText(str(Frase))
		self.comport.close()

		texto = self._hex_to_binary(self._word_to_hex(self.lineEdit1.text()))	
		self.binario = self.return_bin(texto) #pegando valores binario e jogando em uma lista	
		self.label2.setText(texto)	
		self.plot_NRZ() 

	#funcoes para o emissor em imagem
	def lerEntradaIMG(self):		
		# Iniciando conexao serial		
		self.comport = serial.Serial(self.listaPortas[0], self.comboBox1.currentText(), timeout=0.2, write_timeout=0.2)	
		self.strIMAGE = [] #vetor que guardara o valor inteiro da imagem como um char		
		for i in range(0, len(self.R_envio)):
			self.strIMAGE.append(hex(self.R_envio[i])[2:])
			if(hex(self.R_envio[i])[2:] == '0'): self.strIMAGE.append(hex(self.R_envio[i])[2:])		 
		#print self.strIMAGE
		value_CRC = CRCCCITT().calculate(str(''.join(self.strIMAGE)))
		if(self.image_height <= 10 or self.image_width <= 10):
			PARAM_STRING = "   " + ">" + str(value_CRC) + ">" + "0" + hex(self.image_height)[2:] + "0" + hex(self.image_width)[2:] + str(''.join(self.strIMAGE)) + "<" + "   "	
		else:
			PARAM_STRING = "   " + ">" + str(value_CRC) + ">" + hex(self.image_height)[2:] + hex(self.image_width)[2:] + str(''.join(self.strIMAGE)) + "<" + "   "		
		#print PARAM_STRING	
		
		if(len(PARAM_STRING) > 0):				
			for i in range(0,len(PARAM_STRING)):
				self.enviaCaracter(PARAM_STRING[i])				
		# Fechando conexao serial
		self.comport.close()

	#funcoes para o receptor em imagem
	def recebeIMG(self):
		controle_entrada = 0		
		self.myText = []
		self.myCRC = []
		# Time entre a conexao serial e o tempo para escrever (enviar algo)
		time.sleep(0.2)
		VALUE_SERIAL=self.comport.readline()
		while(VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("<")):

			if(VALUE_SERIAL.encode("hex")[:2] == self._word_to_hex(">")): controle_entrada += 1
			elif(controle_entrada == 1 and (VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("\n"))): self.myCRC += VALUE_SERIAL[:1] 
			elif(controle_entrada == 2 and (VALUE_SERIAL.encode("hex")[:2] != self._word_to_hex("\n"))): self.myText += VALUE_SERIAL[:1] 	
			# Time entre a conexao serial e o tempo para escrever (enviar algo)
			time.sleep(0.2)
			VALUE_SERIAL=self.comport.readline()		
			#print VALUE_SERIAL
		self.myCRC = int(''.join(self.myCRC))
		#print self.myCRC
		#print CRCCCITT().calculate(str(''.join(self.myText)[4:]))						
		return(''.join(self.myText))		

	def lerEntradaRecebidaIMG(self):		
		# Iniciando conexao serial		
		self.comport = serial.Serial(self.listaPortas[0], self.comboBox1.currentText(), timeout=0.2, write_timeout=0.2)				
		Frase = self.recebeIMG()			
		self.comport.close()

		self.vetorINT = [] #vetor servira para recuperar a imagem recebida
		for i in range(0, len(Frase), 2):
			self.vetorINT.append(int(Frase[i:i+2], 16))
		#print self.vetorINT
		#print len(self.vetorINT)
		self.binario = []
		self.lineEdit1.clear()
		#self.lineEdit1.setText(str(self.vetorINT))
		for i in range(2, len(self.vetorINT)):
			self.binario += '{0:08b}'.format(self.vetorINT[i])	
		#print self.binario			
		self.label2.setText(str(''.join(self.binario)))
		self.plot_NRZ()

		#gerando imagem
		self.recuperaIMG()

	def recuperaIMG(self):	
		#print self.vetorINT[0],self.vetorINT[1]
		self.vetorIMG = np.zeros((self.vetorINT[0],self.vetorINT[1]))
		incremento = 0
		for i in range(0,self.vetorINT[1]):
			for j in range(0,self.vetorINT[0]):
				self.vetorIMG[j][i] = self.vetorINT[j+incremento+2]				
			incremento += self.vetorINT[0]
		image = QImage()
		arr2im = Image.fromarray(self.vetorIMG) #convertendo matriz para imagem		#
		arr2im.save("recebido.gif")

		self.labelIMAGE.setPixmap(QPixmap('recebido.gif'))		
		self.scaleFactor = 1.0
		self.scrollAreaIMAGE.setVisible(True)
		self.fitToWindowAct.setEnabled(True)
		self.updateActions()
		if not self.fitToWindowAct.isChecked():
			self.labelIMAGE.adjustSize()

	#Deteccao de Erros
	def verificaCRC_ASCII(self):
		if(CRCCCITT().calculate(str(''.join(self.myText))) == self.myCRC):
			self.label2.setStyleSheet('color: green')
		else:
			self.label2.setStyleSheet('color: red')	
	
	def verificaCRC_IMG(self):
		if(CRCCCITT().calculate(str(''.join(self.myText)[4:])) == self.myCRC):
			self.label2.setStyleSheet('color: green')
		else:
			self.label2.setStyleSheet('color: red')	

	#Insercao de Erro		
	def noise_ASCII(self, max_):
		if(len(self.lista_ASCII_error) > 1):
			noise = np.random.normal(0,max_,100)
			tam = len(self.lista_ASCII_error)

			var = random.randint(1,tam-1)

			for i in range(0, var):
				value = random.randint(0, tam-1)
				value_noise = random.randint(0, 99)
				aux = abs(ord(self.lista_ASCII_error[value]) + int(noise[value_noise])) 	
				if(aux == 76 or aux==74):
					aux = aux + 1
				self.lista_ASCII_error[value] = chr(aux)		 		

	
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())