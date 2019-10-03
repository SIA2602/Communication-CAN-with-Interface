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

Ui_Visualization, _ = uic.loadUiType("visualization.ui")

class Visualization(QDialog, Ui_Visualization):

	def __init__(self, parent=None):

		QDialog.__init__(self, parent=parent)
		Ui_Visualization.__init__(self)
		self.setupUi(self)    	

		self.x = []
		self.y = []
		self.binario = []		

		self.ax = None

		self.radioButton1.setHidden(not False)  #inicialmente oculta opcao do bit anterior	
		self.radioButton2.setHidden(not False)	#inicialmente oculta opcao do bit anterior
		
		self.timer = QTimer(self)		

		self.atualizaOpcoes() #funcao responsavel por criar opcoes do comboBox

		self.createGraph() #ativa caixa do grafico	

		self.events() #atualizacoes altomaticas		

		self.timer.setInterval(300)
		self.timer.start()			

	def events(self):
		self.comboBox1.currentIndexChanged.connect(self.atualizaOpcoes) #faz com que o comboBox seja atualizado automaticamente		
		self.timer.timeout.connect(self.update)		 			
			
	def atualizaOpcoes(self):				
		if(self.comboBox1.currentText() == 'ASCII'):
			self.comboBox2.clear()
			self.comboBox2.addItem("Binario")	
			self.comboBox2.addItem("Hexadecimal")	
			
		elif(self.comboBox1.currentText() == 'Binario'):
			self.comboBox2.clear()
			self.comboBox2.addItem("ASCII")	
			self.comboBox2.addItem("Hexadecimal")			
			
		elif(self.comboBox1.currentText() == 'Hexadecimal'):
			self.comboBox2.clear()
			self.comboBox2.addItem("ASCII")	
			self.comboBox2.addItem("Binario")	

	def gravaMensagem(self):
		global texto	

		texto = self.lineEdit1.text() #recebe a entrada

		if(self.comboBox1.currentText() == 'Binario'): #caso esteja na opcao binario

			self.binario = self.lineEdit1.text() #jogando valor de entrada binario para atualizar no grafico	
			if(self.comboBox2.currentText() == 'Hexadecimal'): #caso a conversao escolhida seja hex
				texto = self.bin_to_hex(texto)
				if texto is None:
					texto = "Entrada Invalida!"
				else:
					texto = '0x' + texto					

			elif(self.comboBox2.currentText() == 'ASCII'): #caso a conversao escolhida seja para ASCII
				if( len(self.return_bin(texto)) % 8 == 0 ):
					texto = self.bin_to_ASCII(texto)					
				else: texto = "Entrada Invalida!"							

		self.label1.setText(texto)	

	def createGraph(self):        
		self.figure = plt.figure()

		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		self.graphLayout.addWidget(self.canvas)
		self.graphLayout.addWidget(self.toolbar)

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
		elif(self.comboBox4.currentText() == 'black'):
			return 'black'
		elif(self.comboBox4.currentText() == 'purple'):
			return 'purple'
		elif(self.comboBox4.currentText() == 'orange'):
			return 'orange'

		return 'black'

	def linesWidth(self):		
		self.label5.setNum(self.horizontalSlider1.value()/20.)
		return self.horizontalSlider1.value()/20.


	def plot(self):		

		self.figure.clear()			
			
		self.ax = self.figure.add_subplot(111)

		if self.checkBox3.isChecked(): self.ax.step(self.x, self.y, color=self.printColor(), linewidth=self.linesWidth()) #opcao ativa imprime grafico		
		else: self.ax.step(self.x, self.y, visible=False) #opcao desativada oculta o grafico

		self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
		self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))		
		self.ax.xaxis.grid(color='gray', linestyle='--', linewidth=0.5)
		self.ax.xaxis.grid(self.checkBox2.isChecked())	
		self.ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)			
		self.ax.yaxis.grid(self.checkBox1.isChecked())		

		self.canvas.draw()		

	def plot_NRZ(self):		
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)	#oculta opcao do bit anterior
		#valores para grafico	
		if(len(self.return_bin(self.lineEdit1.text())) > 2):	
			self.y = self.return_bin(self.binario) #recebe valor binario digitado em uma lista
			self.y = [self.y[0]] + self.y			
			self.x = [ i for i in range(len(self.y)) ]	

	def plot_NRZ_L(self):	
		self.radioButton1.setHidden(not False)
		self.radioButton2.setHidden(not False)	#oculta opcao do bit anterior	

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
				
	
	def update(self):		
		if(self.comboBox3.currentText() == 'NRZ'): self.plot_NRZ()	
		if(self.comboBox3.currentText() == 'NRZ-L'): self.plot_NRZ_L()
		if(self.comboBox3.currentText() == 'NRZ-I'): self.plot_NRZ_I()

		self.gravaMensagem()		
		self.plot()			

	@staticmethod
	def bin_to_hex(binary):        
		binary = '0'*(len(binary) % 4) + binary
		try:
			hx = ""
			for i in range(0, len(binary), 4):
				hx += '{:x}'.format(int(binary[i : i + 4], 2))

		except ValueError:
			return None

		return hx

	@staticmethod
	def bin_to_ASCII(texto):    	
		ASCII = ""

		while texto != "":    		
			j = chr(int(texto[:8],2))    		
			ASCII = ASCII+j
			texto = texto[8:]

		return ASCII

	@staticmethod
	def return_cont(value):
		listValue = []        
		for i in range(value):
			listValue.append(i)		
		return listValue
		
	@staticmethod
	def return_bin(value): #dado um int bin eh retornado uma lista dos valores
		return [int(i) for i in value]

   



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Visualization()
    main.show()

    sys.exit(app.exec_())
