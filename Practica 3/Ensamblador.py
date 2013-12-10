#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
from Linea import *
from Automata import *
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
							variablesTextBox+=atributos[2]+"\n\n"
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
							if not permiteOperando and currentLine.operando == None:
								variablesTextBox += "  Operando: Inherente " + str(self.tabop[currentLine.codop.text.upper()]['modos']['Inherente']['bTotal']) + " bytes\n\n"
								continue
							#variablesTextBox += "  Operando: " + str(permiteOperando) + "\n"
							analisisCodop = Automata(currentLine.operando.text)
							variablesTextBox += atributos[2] + "\n"
							if len(analisisCodop.errores) != 0:
								variablesTextBox+="Error (detalles en el log de errores [linea "+str(lineCount-1)+"])\n\n"
								for error in analisisCodop.errores:
									errorTextBox += str(lineCount - 1) + ": " + error + "\n"
								continue
							else:
								banderaModoEncontrado = False
								for modo in analisisCodop.modos:
									if modo in self.tabop[currentLine.codop.text.upper()]['modos'] and not banderaModoEncontrado:
										banderaModoEncontrado = True
										if modo == 'IDX':
											if analisisCodop.signo == None and analisisCodop.registroAc == None:
												variablesTextBox += "Indizado de 5 bits, (IDX), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['IDX']['bTotal']) + " bytes\n"
											elif analisisCodop.registroAc != None:
												variablesTextBox += "Indizado de acumulador, (IDX), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['IDX']['bTotal']) + " bytes\n"
											else:
												variablesTextBox += "Indizado de "
												if analisisCodop.pre:
													variablesTextBox+="pre "
												else:
													variablesTextBox+="post "
												if analisisCodop.signo == '+':
													variablesTextBox+="incremento"
												else:
													variablesTextBox+="decremento"
												variablesTextBox+=", (IDX), de " + str(self.tabop[currentLine.codop.text.upper()]['modos']['IDX']['bTotal']) + " bytes\n"
										elif modo == 'IDX1':
											variablesTextBox += "Indizado de 9 bits, (IDX1), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['IDX1']['bTotal']) + " bytes\n"
										elif modo == 'IDX2':
											variablesTextBox += "Indizado de 16 bits, (IDX2), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['IDX2']['bTotal']) + " bytes\n"
										elif modo == '[IDX2]':
											variablesTextBox += "Indizado indirecto de 16 bits, (IDX1), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['[IDX2]']['bTotal']) + " bytes\n"
										elif modo == '[D,IDX]':
											variablesTextBox += "Indizado indirecto de acumulador, ([D,IDX]), " + str(self.tabop[currentLine.codop.text.upper()]['modos']['[D,IDX]']['bTotal']) + " bytes\n"
										elif modo == 'REL':
											variablesTextBox += "Relativo de "+str(4*self.tabop[currentLine.codop.text.upper()]['modos']['REL']['bTotal'])+" bits, "+ str(self.tabop[currentLine.codop.text.upper()]['modos']['REL']['bTotal']) + " bytes\n"
										elif modo == 'Extendido':
											variablesTextBox+="Extendido, de "+str(self.tabop[currentLine.codop.text.upper()]['modos']['Extendido']['bTotal']) + " bytes\n"
										elif modo == 'Directo':
											variablesTextBox+="Directo, de "+str(self.tabop[currentLine.codop.text.upper()]['modos']['Directo']['bTotal']) + " bytes\n"
										elif modo == 'Inmediato':
											variablesTextBox+="Inmediato de "+str(8*self.tabop[currentLine.codop.text.upper()]['modos']['Inmediato']['bCalcular'])+" bits, "+str(self.tabop[currentLine.codop.text.upper()]['modos']['Inmediato']['bTotal']) + " bytes\n"
										variablesTextBox+='\n'
								if not banderaModoEncontrado:
									variablesTextBox+="No coincide con ningún modo de direccionamiento (detalles en el log de errores [linea "+str(lineCount-1)+"])"
									errorTextBox+=str(lineCount-1)+": No coincide con ningún modo de direccionameiento (modos válidos para el codop ["+currentLine.codop.text+"]: "
									b_=False
									for modo in self.tabop[currentLine.codop.text.upper()]['modos']:
										if b_:
											errorTextBox+=","+modo
										else:
											b_=True
											errorTextBox+=modo
									errorTextBox+=")\n"
					for error in currentLine.getErrores():
						errorTextBox += str(lineCount - 1) + ": " + error + "\n"
			if not banderaEnd:
				errorTextBox += str(lineCount - 1) + ": No se encontró el END\n"
			return archivoCorto, fileTextBox, variablesTextBox, errorTextBox
		else:
			return None