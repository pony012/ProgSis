#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
from Linea import *
import Util

class Ensamblador:
	def __init__(self, rutaTabop):
		self.rutaTabop = rutaTabop
		self.tabop = {}
		if(Util.existeArchivo(self.rutaTabop)):
			self.fileTabop = open(self.rutaTabop, "r")
			self.textTabop = self.fileTabop.read()
			self.fileTabop.close()
			for line in self.textTabop.split('\n'):				
				args = line.split()
				#ahora args contiene algo como
				#[codop,operando,direccionamiento,cod.máquina,total calculados, total por calcular, suma total]
				if not args[0].upper() in self.tabop:
					self.tabop[args[0].upper()] = {'operando' : None, 'modos' : {}}
				self.tabop[args[0].upper()]['operando'] = True if args[1] == '1' else False
				self.tabop[args[0].upper()]['modos'][args[2]] = {'codMaq':args[3],'bCalculados':args[4],'bCalcular':args[5],'bTotal':args[6]}


	def cargarArchivo(self, rutaArchivo):
		banderaEnd = False
		if(Util.existeArchivo(rutaArchivo)):
			archivoCorto = rutaArchivo.split("/")
			archivoCorto = archivoCorto[len(archivoCorto)-1]
			_file = open(rutaArchivo, "r")
			fileText = _file.read()
			_file.close()
			#Leer el archivo de texto y mandarlo a sus respectivos campos de texto
			lineCount = 1
			fileTextBox = ""
			variablesTextBox = ""
			errorTextBox = ""
			for line in fileText.split('\n'):
				fileTextBox += str(lineCount) + "\t" + str( line ) + "\n"
				lineCount += 1
				currentLine = Linea(str(line))
				if (currentLine.comentario) :
					variablesTextBox += "Comentario\n\n"
				else:
					if str(currentLine.codop).upper() == "END":
						banderaEnd = True
					atributos = currentLine.atributos()
					variablesTextBox += atributos[0] + "\n"
					variablesTextBox += atributos[1] + "\n"
					if(currentLine.codop != None):
						if not currentLine.codop.text.upper() in self.tabop:
							currentLine.errores.append(currentLine.codop.text +" no se encuentra en la TABOP")
						else:							
							permiteOperando = self.tabop[currentLine.codop.text.upper()]['operando']
							if permiteOperando and currentLine.operando == None:
								currentLine.errores.append(currentLine.codop.text +" el CODOP debe tener Operando")
							if not permiteOperando and currentLine.operando != None:
								currentLine.errores.append(currentLine.codop.text +" el CODOP NO debe tener Operando")
							variablesTextBox += "  Operando: " + str(permiteOperando) + "\n"
							for modo in sorted(self.tabop[currentLine.codop.text.upper()]['modos'].iteritems()):
								variablesTextBox += "  "+ modo[0] + "-> "
								for propiedad in sorted(modo[1].iteritems(),reverse = True):
									variablesTextBox += propiedad[0] + ": " + propiedad[1] + " "
								variablesTextBox += '\n'

					variablesTextBox += atributos[2] + "\n\n"
					for error in currentLine.getErrores():
						errorTextBox += str(lineCount - 1) + ": " + error + "\n"
			if not banderaEnd:
				errorTextBox += str(lineCount - 1) + ": No se encontró el END\n"
			return archivoCorto, fileTextBox, variablesTextBox, errorTextBox
		else:
			return None
