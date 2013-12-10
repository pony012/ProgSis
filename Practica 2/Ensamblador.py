#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
from Linea import *
import Util

class Ensamblador:
	def __init__(self, rutaTabop):
		"""
			rutaTabop (String): La ruta del archivo que contiene la tabla de operaciones
			Inicializa un diccionario (self.tabop) que contiene la tabla de operaciones
			El diccionario tendrá la estructura siguiente:
			self.tabop = {
				'CODOP':{ #En CODOP irá el código de operación, ej. ADCA, ADDB, etc
					'operando':boolean
					'modos':{
						'MODO':{ #En MODO irá el modo de direccionamiento, ej. IDX, IDX1, etc
							'codMaq':String,
							'bCalculados':Int,
							'bCalcular':Int,
							'bTotal':Int
						}
					}
				}
			}
		"""
		self.rutaTabop = rutaTabop
		self.tabop = {}
		if(Util.existeArchivo(self.rutaTabop)): #evalúa si existe el archivo con la ruta dada
			self.fileTabop = open(self.rutaTabop, "r")
			self.textTabop = self.fileTabop.read()
			self.fileTabop.close()
			for line in self.textTabop.split('\n'): #divide el archivo en líneas
				args = line.split() #divide cada línea en sus 7 componentes
				#ahora args contiene algo como
				"""[
					codop,
					operando,
					direccionamiento,
					cod.máquina,
					total calculados,
					total por calcular,
					suma total
				   ]"""
				if not args[0].upper() in self.tabop:
					"""si no se ha agregado el codop al diccionario, junto su 
					valor de operando.
					SIEMPRE los agrega en mayúsculas, por ejemplo, AdcA será
					agregado como ADCA"""
					self.tabop[args[0].upper()] = {
												   'operando' : True if args[1] == '1' else False,
												   'modos' : {}
												  }
				#En este punto ya es seguro que se encuentre el CODOP en el diccionario
				#Entonces se agregan los modos de direccionamiento
				self.tabop[args[0].upper()]['modos'][args[2]] = {
						'codMaq': args[3],
						'bCalculados': int(args[4]),
						'bCalcular': int(args[5]),
						'bTotal': int(args[6])
						}

	def cargarArchivo(self, rutaArchivo):
		"""
			Carga y evalúa un archivo que contenga código en ensamblador (HC12)
		"""
		#bandera utilizada para saber si el archivo contiene el codop END
		banderaEnd = False
		if(Util.existeArchivo(rutaArchivo)):
			archivoCorto = rutaArchivo.split("/")
			archivoCorto = archivoCorto[len(archivoCorto)-1]
			_file = open(rutaArchivo, "r")
			fileText = _file.read()
			_file.close()
			lineCount = 1
			fileTextBox = ""
			variablesTextBox = ""
			errorTextBox = ""
			for line in fileText.split('\n'):
				#agregamos el número de línea en cada línea
				fileTextBox += str(lineCount) + "\t" + str( line ) + "\n"
				lineCount += 1
				#Mandamos la línea actual a la clase Linea
				currentLine = Linea(str(line))
				if (currentLine.comentario) :
					variablesTextBox += "Comentario\n\n"
				else:
					if str(currentLine.codop).upper() == "END":
						banderaEnd = True
					"""
					#Esto asegura que la última instruccion es END
					else:
						banderaEnd = False
					"""
					atributos = currentLine.atributos()
					variablesTextBox += atributos[0] + "\n"
					variablesTextBox += atributos[1] + "\n"
					#Si la línea contiene un código de operación
					if(currentLine.codop != None):
						#Si el código de operación no se encuentra en la 
						#Tabla de operaciones
						if not currentLine.codop.text.upper() in self.tabop:
							currentLine.errores.append(currentLine.codop.text 
													   + " no se encuentra en"
													   + " la TABOP")
						else:
							#Bandera utilizada para saber si el código de
							#operación de la línea admite tener o no operando
							permiteOperando = self.tabop[currentLine.codop.text.upper()]['operando']
							if permiteOperando and currentLine.operando == None:
								currentLine.errores.append("El CODOP "
														   +currentLine.codop.text
														   +" debe tener Operando")
							if not permiteOperando and currentLine.operando != None:
								currentLine.errores.append("El CODOP "
														   +currentLine.codop.text
														   +" NO debe tener Operando")
							variablesTextBox += "  Operando: " + str(permiteOperando) + "\n"
							"""
								Guardará en modo una tupla con los valores
								modo = (modo,{propiedades})
								modo = (String,{
											'codMaq':String,
											'bCalculados':Int,
											'bCalcular':Int,
											'bTotal':Int
											}
										)
								para cada modo que encuentre para ese codop
							"""
							for modo in sorted(self.tabop[currentLine.codop.text.upper()]['modos'].iteritems()):
								variablesTextBox += "  "+ modo[0] + "-> "
								"""
									Guardará en propiedad una tupla con los 
									valores
									propiedad = (llave,valor)
									propiedad = (String, [String|Int])
									para cada propiedad encontrada en cada
									modo de direccionamiento para el codop actual
								"""
								for propiedad in sorted(modo[1].iteritems(),reverse = True):
									variablesTextBox += propiedad[0] + ": " + str(propiedad[1]) + " "
								variablesTextBox += '\n'
					variablesTextBox += atributos[2] + "\n\n"
					for error in currentLine.getErrores():
						errorTextBox += str(lineCount - 1) + ": " + error + "\n"
			if not banderaEnd:
				errorTextBox += str(lineCount - 1) + ": No se encontró el END\n"
			return archivoCorto, fileTextBox, variablesTextBox, errorTextBox
		else:
			return None