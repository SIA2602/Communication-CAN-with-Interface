#!/usr/bin/env python3

# -*- coding: iso-8859-1 -*-
import time
import serial

import sys, os

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QKeyEvent

from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QLabel, QMainWindow, QAction, QFileDialog

from returnSerialPort import serialPorts

Ui_Emissor, _ = uic.loadUiType("emissor.ui")

class Emissor(QDialog, Ui_Emissor):

	def __init__(self, parent=None):

		QDialog.__init__(self, parent=parent)
		Ui_Emissor.__init__(self)
		self.setupUi(self)		

		self.lineEdit1.setHidden(not False)	
		self.label1.setHidden(not False)	
		self.label2.setHidden(not False)
		self.comboBox1.setHidden(not False)
		self.pushButton2.setHidden(not False)

		self.timer = QTimer(self)

		self.events()
		self.recebePortasSeriais()
			
		self.pushButton2.clicked.connect(self.singleBrowse)	
		self.pushButton1.clicked.connect(self.lerEntrada) 					

		self.timer.setInterval(300)
		self.timer.start()	

	def recebePortasSeriais(self):
		listaPortas = serialPorts()		
		if(self.comboBox3.count() == 1):
			self.comboBox3.clear()
			self.comboBox3.addItem("Select Serial Port", None)	
			for i in range(0,len(listaPortas)):
				self.comboBox3.addItem(listaPortas[i])

	def singleBrowse(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
		with open(filename[0], 'r') as f:
			file_text = f.read()
			self.label1.setText(file_text)			

	def enviaCaracter(self, PARAM_CARACTER):

		# Time entre a conexao serial e o tempo para escrever (enviar algo)
		time.sleep(0.1)
		
		self.comport.write(str.encode(PARAM_CARACTER))
		
		VALUE_SERIAL=self.comport.readline()		

		return(VALUE_SERIAL)
		


	def lerEntrada(self):
		# Iniciando conexao serial		
		self.comport = serial.Serial(self.comboBox3.currentText(), self.comboBox4.currentText(), timeout=0.5, write_timeout=0.5)			
		
		#PARAM_STRING="Ola como vai? Oi estou bem, e voce?" #recebe a entrada
		PARAM_STRING = " "
		PARAM_STRING += str(self.lineEdit1.text())		
		if(self.comboBox1.currentText() == "Entrada em Arquivo"):
			PARAM_STRING=str(self.label1.text())		
		
		if(len(PARAM_STRING) > 0):		
			Frase = " "
			for i in range(0,len(PARAM_STRING)):
				Frase += self.enviaCaracter(PARAM_STRING[i])	

			if(self.comboBox1.currentText() == "Entrada em Arquivo"):
				self.label2.setText(Frase)
			else: self.label1.setText(str(Frase))
		# Fechando conexao serial
		self.comport.close()

	def events(self):
		self.timer.timeout.connect(self.atualizaOpcoes)						

	def atualizaOpcoes(self):				
		if(self.radioButton1.isChecked()):	

			self.comboBox1.setHidden(not True)
			if(self.comboBox1.count() == 0):
				self.comboBox1.clear()
				self.comboBox1.addItem("Selecione")	
				self.comboBox1.addItem("Entrada em Texto")	
				self.comboBox1.addItem("Entrada em Arquivo")

			if(self.comboBox1.currentText() == "Selecione"):
				self.lineEdit1.setHidden(not False)	
				self.label1.setHidden(not False)
				self.label2.setHidden(not False)
				self.pushButton2.setHidden(not False)

			if(self.comboBox1.currentText() == "Entrada em Texto"):
				self.lineEdit1.setHidden(not True)	
				self.label1.setHidden(not True)	
				self.label2.setHidden(not False)
				self.pushButton2.setHidden(not False)
			

			if(self.comboBox1.currentText() == "Entrada em Arquivo"):
				self.lineEdit1.setHidden(not False)	
				self.label1.setHidden(not True)
				self.label2.setHidden(not True)
				self.pushButton2.setHidden(not True)

		else:
			self.lineEdit1.setHidden(not False)	
			self.label1.setHidden(not False)
			self.label2.setHidden(not False)			
			self.comboBox1.setHidden(not False)	
			self.pushButton2.setHidden(not False)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Emissor()
    main.show()

    sys.exit(app.exec_())