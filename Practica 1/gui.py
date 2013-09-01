#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
import tkFileDialog
import tkMessageBox
from Linea import *
import Util

class GUI:
	def __init__(self):
		self.gui = Tk()
		self.gui.title("Práctica 1")

		try:
			self.gui.iconbitmap(default = "favicon.ico")
		except:
			pass

		#FILE
		self.fileName = ""

		#Menu
		self.menu = Menu( self.gui )
		self.gui.config( menu = self.menu )
		#Menu archivo
		self.menuArchivo = Menu( self.menu, tearoff = 0 )
		self.menu.add_cascade( label = "Archivo", menu = self.menuArchivo )
		self.menuArchivo.add_command( label = "Cargar archivo", command = self.cargarArchivo )
		self.menuArchivo.add_separator()
		self.menuArchivo.add_command( label = "Salir", command = self.exit )

		#Frame que engloba al archivo asm y las variables (ambos cuadros de texto)
		self.frameUp = Frame( self.gui , width = 150, height = 500, relief = FLAT, bd = 0 , padx = 20 , pady = 10 )
		self.frameUp.grid( row = 0 , column = 0 )

		#Frame que engloba el log de errores
		self.frameDown = Frame( self.gui , width = 500, height = 50, relief = FLAT, bd = 0 , padx = 20 , pady = 5 )
		self.frameDown.grid( row = 1 , column = 0 )

		#Frame del archivo
		self.frameArchivo = LabelFrame( self.frameUp , width = 150, height = 500, relief = GROOVE, bd = 3 , padx = 20 , pady = 10 ,
										 text = "Archivo")
		self.frameArchivo.grid( row = 0 , column = 0 )

		#Frame de variables
		self.frameVariables = LabelFrame( self.frameUp , width = 350, height = 500, relief = GROOVE, bd = 3 , padx = 10 , pady = 10 ,
										 text = "Salida")
		self.frameVariables.grid( row = 0 , column = 1 )

		#Frame del log de errores
		self.frameErrorConsole = LabelFrame( self.frameDown , width = 500, height = 50, relief = GROOVE, bd = 3 , padx = 10 , pady = 10 ,
											 text = "Error Log")
		self.frameErrorConsole.grid( row = 0 , column = 0 )

		#Scroll del texto del archivo asm
		self.fileXScroll = Scrollbar( self.frameArchivo , orient = HORIZONTAL)
		self.fileXScroll.pack( side = BOTTOM , fill= X )
		self.fileYScroll = Scrollbar( self.frameArchivo , orient = VERTICAL)
		self.fileYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se vaciará el archivo asm
		self.fileTextBox	 = Text( self.frameArchivo , bg = "#272821" , fg="#F8F8F2", width = 80 , height = 26 , relief = SUNKEN , bd = 3 ,
									 padx = 10 , pady = 10 , state = DISABLED , wrap = NONE, xscrollcommand = self.fileXScroll.set,
									 yscrollcommand = self.fileYScroll.set )
		self.fileXScroll.config(command = self.fileTextBox.xview)
		self.fileYScroll.config(command = self.fileTextBox.yview)
		self.fileTextBox.pack()

		#Scroll del texto de las variables
		self.variablesXScroll = Scrollbar( self.frameVariables , orient = HORIZONTAL)
		self.variablesXScroll.pack( side = BOTTOM , fill= X )
		self.variablesYScroll = Scrollbar( self.frameVariables , orient = VERTICAL)
		self.variablesYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se mostrarán las variables
		self.variablesTextBox	 = Text( self.frameVariables , bg = "#272821" , fg="#F8F8F2", width = 40 , height = 26 , relief = SUNKEN , bd = 3 ,
									 padx = 10 , pady = 10 , state = DISABLED , wrap = NONE, xscrollcommand = self.variablesXScroll.set,
									 yscrollcommand = self.variablesYScroll.set )
		self.variablesXScroll.config(command = self.variablesTextBox.xview)
		self.variablesYScroll.config(command = self.variablesTextBox.yview)
		self.variablesTextBox.pack()

		#Scroll del texto de los errores
		self.errorXScroll = Scrollbar( self.frameErrorConsole , orient = HORIZONTAL)
		self.errorXScroll.pack( side = BOTTOM , fill= X )
		self.errorYScroll = Scrollbar( self.frameErrorConsole , orient = VERTICAL)
		self.errorYScroll.pack( side = RIGHT , fill= Y )
		#Textbox donde se mostrarán lss errores
		self.errorTextBox	 = Text( self.frameErrorConsole , bg = "#272821" , fg="#F8F8F2", width = 131 , height = 4 , relief = SUNKEN , bd = 3 ,
									 padx = 10 , pady = 10 , state = DISABLED , wrap = NONE, xscrollcommand = self.errorXScroll.set,
									 yscrollcommand = self.errorYScroll.set )
		self.errorXScroll.config(command = self.errorTextBox.xview)
		self.errorYScroll.config(command = self.errorTextBox.yview)
		self.errorTextBox.pack()

	def run(self):
		self.gui.mainloop()

	def cargarArchivo(self):
		banderaEnd = False
		self.fileName = tkFileDialog.askopenfilename( filetypes =[("","*.asm *.txt")]  )
		if(Util.existeArchivo(self.fileName)):
			archivoCorto = self.fileName.split("/")
			archivoCorto = archivoCorto[len(archivoCorto)-1]
			self.frameArchivo.config( text = archivoCorto )
			_file = open(self.fileName, "r")
			self.fileText = _file.read()
			_file.close()
			#Leer el archivo de texto y mandarlo a sus respectivos campos de texto
			self.fileTextBox.config( state = NORMAL )
			self.variablesTextBox.config( state = NORMAL )
			self.errorTextBox.config( state = NORMAL )
			self.fileTextBox.delete( 1.0, END )
			self.variablesTextBox.delete( 1.0, END )
			self.errorTextBox.delete( 1.0, END )
			lineCount = 1
			for line in self.fileText.split('\n'):
				self.fileTextBox.insert(END, str(lineCount) + "\t" )
				lineCount = lineCount+1
				self.fileTextBox.insert( END , str( line ) + "\n" )
				currentLine = Linea(str(line))
				if (currentLine.comentario) :
					self.variablesTextBox.insert(END, "Comentario\n\n")
				else:
					if str(currentLine.codop).upper() == "END":
						banderaEnd = True
					self.variablesTextBox.insert(END, currentLine.atributos() + "\n")
					for error in currentLine.getErrores():
						self.errorTextBox.insert(END, str(lineCount - 1) + ": " + error + "\n" )
			if not banderaEnd:
				self.errorTextBox.insert(END, str(lineCount - 1) + ": No se encontró el END\n" )
			self.fileTextBox.config( state = DISABLED )
			self.variablesTextBox.config( state = DISABLED )
			self.errorTextBox.config( state = DISABLED )
	def exit(self):
		self.gui.quit()

gui = GUI()
gui.run()