#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
import tkFileDialog
import tkMessageBox
from Ensamblador import *
import Util

class GUI:
	def __init__(self):
		self.gui = Tk()
		self.gui.title("Práctica 8")

		try:
			self.gui.iconbitmap(default = "favicon.ico")
		except:
			pass

		#Ensamblador
		self.rutaTABOP = "TABOP.txt"
		self.ensamblador = Ensamblador(self.rutaTABOP)
		#FILE
		self.fileName = ""

		#Menu
		self.menu = Menu( self.gui )
		self.gui.config( menu = self.menu )
		#Menu archivo
		self.menuArchivo = Menu( self.menu, tearoff = 0 )
		self.menu.add_cascade(label = "Archivo", menu = self.menuArchivo )
		self.menuArchivo.add_command(label = "Cargar archivo", 
									 command = self.cargarArchivo )
		self.menuArchivo.add_separator()
		self.menuArchivo.add_command(label = "Salir",
									 command = self.exit )

		#Frame que engloba al archivo asm y las variables (ambos cuadros de texto)
		self.frameUp = Frame(self.gui , width = 150, height = 500,
							 relief = FLAT, bd = 0 , padx = 20 ,
							 pady = 10 )
		self.frameUp.grid( row = 0 , column = 0 )

		#Frame que engloba el log de errores
		self.frameDown = Frame(self.gui , width = 500, height = 50,
							   relief = FLAT, bd = 0 , padx = 20 , 
							   pady = 5 )
		self.frameDown.grid( row = 1 , column = 0 )

		#Frame del archivo
		self.frameArchivo = LabelFrame(self.frameUp , width = 150,
									   height = 500, relief = GROOVE,
									   bd = 3 , padx = 20 , pady = 10 ,
									   text = "Archivo")
		self.frameArchivo.grid( row = 0 , column = 0 )

		#Frame de variables
		self.frameVariables = LabelFrame(self.frameUp , width = 350,
										 height = 500, relief = GROOVE,
										 bd = 3 , padx = 10 , pady = 10,
										 text = "Salida")
		self.frameVariables.grid( row = 0 , column = 1 )

		#Frame del log de errores
		self.frameErrorConsole = LabelFrame(self.frameDown , width = 243,
											height = 50, relief = GROOVE,
											bd = 3 , padx = 10 , pady = 10 ,
											text = "Error Log")
		self.frameErrorConsole.grid( row = 0 , column = 0 )

		#Frame del codMaq y Contloc
		self.frameCodMaq = LabelFrame(self.frameDown, width = 243,
											height = 50, relief = GROOVE,
											bd = 3, padx = 10, pady = 10,
											text = "Código Generado")
		self.frameCodMaq.grid( row = 0, column = 1)

		#Scroll del texto del archivo asm
		self.fileXScroll = Scrollbar( self.frameArchivo , orient = HORIZONTAL)
		self.fileXScroll.pack( side = BOTTOM , fill= X )
		self.fileYScroll = Scrollbar( self.frameArchivo , orient = VERTICAL)
		self.fileYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se vaciará el archivo asm
		self.fileTextBox = Text(self.frameArchivo , bg = "#272821", 
								fg="#F8F8F2", width = 80 , height = 26 ,
								relief = SUNKEN , bd = 3 , padx = 10 ,
								pady = 10 , state = DISABLED ,
								wrap = NONE,
								xscrollcommand = self.fileXScroll.set,
								yscrollcommand = self.fileYScroll.set)
		self.fileXScroll.config(command = self.fileTextBox.xview)
		self.fileYScroll.config(command = self.fileTextBox.yview)
		self.fileTextBox.pack()

		#Scroll del texto de las variables
		self.variablesXScroll = Scrollbar(self.frameVariables ,
										  orient = HORIZONTAL)
		self.variablesXScroll.pack( side = BOTTOM , fill= X )
		self.variablesYScroll = Scrollbar(self.frameVariables ,
										  orient = VERTICAL)
		self.variablesYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se mostrarán las variables
		self.variablesTextBox = Text(
				self.frameVariables, bg = "#272821",
				fg="#F8F8F2", width = 40, height = 26,
				relief = SUNKEN, bd = 3, padx = 10, 
				pady = 10, state = DISABLED,
				wrap = NONE,
				xscrollcommand = self.variablesXScroll.set,
				yscrollcommand = self.variablesYScroll.set)
		self.variablesXScroll.config(command = self.variablesTextBox.xview)
		self.variablesYScroll.config(command = self.variablesTextBox.yview)
		self.variablesTextBox.pack()

		#Scroll del texto de los errores
		self.errorXScroll = Scrollbar(self.frameErrorConsole,
									  orient = HORIZONTAL)
		self.errorXScroll.pack( side = BOTTOM , fill= X )
		self.errorYScroll = Scrollbar(self.frameErrorConsole,
									  orient = VERTICAL)
		self.errorYScroll.pack( side = RIGHT , fill= Y )
		
		#Textbox donde se mostrarán los errores
		self.errorTextBox	 = Text(self.frameErrorConsole, bg = "#272821",
									fg="#F8F8F2", width = 78, height = 4,
									relief = SUNKEN, bd = 3 , padx = 10 ,
									pady = 10, state = DISABLED, wrap = NONE,
									xscrollcommand = self.errorXScroll.set,
									yscrollcommand = self.errorYScroll.set)
		self.errorXScroll.config(command = self.errorTextBox.xview)
		self.errorYScroll.config(command = self.errorTextBox.yview)
		self.errorTextBox.pack()

		#Scroll del texto del código generado
		self.codMaqXScroll = Scrollbar(self.frameCodMaq,
									  orient = HORIZONTAL)
		self.codMaqXScroll.pack( side = BOTTOM , fill= X )
		self.codMaqYScroll = Scrollbar(self.frameCodMaq,
									  orient = VERTICAL)
		self.codMaqYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se mostrará el código generado
		self.codMaqTextBox	 = Text(self.frameCodMaq, bg = "#272821",
									fg="#F8F8F2", width = 45, height = 4,
									relief = SUNKEN, bd = 3 , padx = 10 ,
									pady = 10, state = DISABLED, wrap = NONE,
									xscrollcommand = self.codMaqXScroll.set,
									yscrollcommand = self.codMaqYScroll.set)
		self.codMaqXScroll.config(command = self.codMaqTextBox.xview)
		self.codMaqYScroll.config(command = self.codMaqTextBox.yview)
		self.codMaqTextBox.pack()		


	def run(self):
		self.gui.mainloop()

	def cargarArchivo(self): 
		self.fileName =	tkFileDialog.askopenfilename(filetypes =[("",  "*.asm *.txt" )])
		tuplaASM = self.ensamblador.cargarArchivo(self.fileName)
		if(tuplaASM != None):
			self.frameArchivo.config( text = tuplaASM[0] ) 
			self.fileTextBox.config(state = NORMAL )
			self.variablesTextBox.config( state = NORMAL )
			self.errorTextBox.config( state = NORMAL )
			self.codMaqTextBox.config( state = NORMAL )
			self.fileTextBox.delete( 1.0,END ) 
			self.variablesTextBox.delete( 1.0, END )
			self.errorTextBox.delete(1.0, END )
			self.codMaqTextBox.delete(1.0, END )
			self.fileTextBox.insert( END, tuplaASM[1] )
			self.variablesTextBox.insert(END, tuplaASM[2] )
			self.errorTextBox.insert(END, tuplaASM[3] )
			self.codMaqTextBox.insert(END, tuplaASM[4] )
			self.fileTextBox.config( state = DISABLED ) 
			self.variablesTextBox.config( state = DISABLED )
			self.errorTextBox.config( state = DISABLED ) 
			self.codMaqTextBox.config( state = DISABLED )
	
	def exit(self):
		self.gui.quit()

gui = GUI()
gui.run()