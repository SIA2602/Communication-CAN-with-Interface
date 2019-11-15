# Communication-CAN-with-Interface

INSTRUCOES GERAIS:
Obs.: Por questoes de Compatibilidade no envio e recebimento se optou em usar o python 2, logo o programa DEVE ser executado em python 2.

A pasta: Communication_CAN_with_Interface contem:
	-Arquivos_Arduino
		-RX_frase_serial [onde contem o programa relativo ao arduino que recebera a informacao]
		-TX_frase_serial [onde contem o programa relativo ao arduino que enviara a informacao]
		-CAN_BUS_Shield-master [.zip da biblioteca necessaria para execucao dos programas arduino, tal zip deve ser descompactado e colocado na biblioteca arduino. Para mais detalhes da implementacao do programa em arduino para o Modulo CAN consultar o site onde o programa foi baseado: https://www.electronicshub.org/arduino-mcp2515-can-bus-tutorial/ ]
	-Image_Test [Biblioteca de Imagens para Testar o envio e Recebimento de Imagem. Atencao se recomenda o envio de Imagens menor que 50x50 pixels.]
	-Imagens [Biblioteca de Imagens Relativo aos Icones do Sofware]
	-Text_Test [Biblioteca com Arquivo de texto para Testar o envio e Recebimento de Texto. Atencao o Software nao aceita arquivos de texto com quebra de linha. ]
	-compila.py [Implementacao da Interface Grafica em python]
	-LICENSE [Licensa gerada pelo GitHub]
	-principal.ui [Design da Interface Grafica Desenvolvidada no Qt5 Designer]
	-README.md [Arquivo contendo as Instrucoes]
	-returnSerialPort.py [Implementacao para deteccao da porta serial pelo software. Obs.: Biblioteca Implementada por um terceiro.]
	-help.py [Implementacao da Janela de Ajuda]
	-help.ui [Design da Interface Grafica da Janela de Ajuda Desenvolvidada no Qt5 Designer]

EXECUCAO DO PROGRAMA:
Obs.: Para uma correta execucao do programa, verificar se as bibliotecas minimas para a sua compilacao estao devidamentes instaladas. As bibliotecas minimas requeridas estao listadas abaixo.
	-Bibliotecas Minimas Requeridas: [Obs.: Eventualmente pode-se precisar de instalar biblioteca adicionais nao listadas abaixo.]
		-serial
		-sip
		-pil
		-PyQt5
		-numpy
		-matplotlib
		-time
		-sys
		-PyCRC [https://pycrc.readthedocs.io/en/latest/readme.html]
	-Execucao do Programa:
		-Dentro da Pasta Principal digitar no terminal: python compila.py
		[Obs.: Para Detalhes de como usar o software consultar o menu help ao executar o programa.]
		