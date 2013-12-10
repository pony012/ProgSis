#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

from Tkinter import *
from Linea import *
from Automata import *
from Tabsim import *
from Listado import *
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
		#Bandera utilizada para saber si el archivo contiene el codop END
		banderaEnd = False
		#Bandera utilizada para saber si la tabla de símbolos ya fue creada
		banderaTabsimCreada = False
		#Bandera utilizada para saber si ya se usó la directiva ORG por lo menos
		#una vez
		banderaOrg = False
		#Las variables "direccionInicial" y "contLoc" estarán en base decimal 
		#pero a la hora de escribirlo en el archivo se hará de manera Hexadecimal
		#de 4 bytes
		#Variable utilizada para guardar el valor inicial del archivo de listado
		direccionInicial = 0
		#Variable utilizada para llevar la cuenta de en qué localidad se encuentra
		#la instrucción actual en el archivo de listado
		contLoc = 0
		if(Util.existeArchivo(rutaArchivo)):
			#Guardará la información de la instrucción que esté evaluando
			infoInstr = None
			#Guardará la información de la instrucción actual, en el modo actual
			infoInstrModo = None
			#Lista de directivas CONSTANTES y de RESERVA DE ESPACIO DE MEMORIA
			directivas = ["DW","DB","DC.W","DC.B","FCB","FDB","FCC","DS","DS.B","DS.W","RMB","RMW"]
			archivoCorto = rutaArchivo.split("/")
			archivoCorto = archivoCorto[len(archivoCorto)-1]
			nombreListado = str.join(".",archivoCorto.split(".")[0:-1]) + "tmp.txt"
			fileListado = Listado(nombreListado,"w")
			nombreTabsim = str.join(".",archivoCorto.split(".")[0:-1]) + "tabsim.txt"
			#nombreTabsim = "tabsim.txt"
			_file = open(rutaArchivo, "r")
			fileText = _file.read()
			_file.close()
			lineCount = 1
			fileTextBox = ""
			codMaqGenerado = ""
			variablesTextBox = ""
			errorTextBox = ""
			#Iterar sobre todas las lineas del archivo
			for line in fileText.split('\n'):
				#agregamos el número de línea en cada línea
				fileTextBox += str(lineCount) + "\t" + str( line ) + "\n"
				lineCount += 1

				#Mandamos la línea actual a la clase Linea
				currentLine = Linea(str(line))
				if (currentLine.comentario) :
					variablesTextBox += "Comentario\n\n"
				else:
					if contLoc > 65535:
						errorTextBox += str(lineCount - 2) + ": Desbordamiento del contador de localidades [valor máximo: 65535] [valor actual: "+str(contLoc)+"] (Se reiniciará a 0)\n"
						contLoc=0
					"""
					INICIO DIRECTIVAS
					"""
					#Validar EQU
					if str(currentLine.codop).upper() == "EQU":
						if(currentLine.etiqueta != None and currentLine.operando != None):
							#Sacar el valor del operando
							analisisCodop = Automata(currentLine.operando.text)
							if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
								if("Directo" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
									errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva EQU es de 0 a 65535, el valor actual es "+str(analisisCodop.valor)+"\n"
									continue
								elif("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva EQU tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
									continue
								#Ya se cuenta con el valor, ahora se trata de insertar en la tabsim
								elif(not banderaTabsimCreada):
									tabsim = Tabsim(nombreTabsim)
									banderaTabsimCreada = True
								elif(not tabsim.write(currentLine.etiqueta, analisisCodop.valor)):
									errorTextBox += str(lineCount - 1) + ": La etiqueta "+str(currentLine.etiqueta)+" ya fue usada\n"
								else:
									#Se escribe en el archivo de listado
									fileListado.write(analisisCodop.valor,currentLine.etiqueta,"EQU",currentLine.operando,None,"DVA",None,None,None,None)
						else:
							errorTextBox += str(lineCount - 1) + ": Para la directiva EQU tanto la etiqueta como el operando tienen que ser diferentes de NULL\n"
						continue
					
					#Validar ORG
					if str(currentLine.codop).upper() == "ORG":
						if(currentLine.operando == None):
							errorTextBox += str(lineCount - 1) + ": La directiva ORG debe de tener operando\n"
						else:
							if(banderaOrg):
								errorTextBox += str(lineCount - 1) + ": La directiva ORG debe existir una sola vez\n"
								continue
							analisisCodop = Automata(currentLine.operando.text)
							if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
								if("Directo" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
									errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva ORG es de 0 a 65535, el valor actual es "+str(analisisCodop.valor)+"\n"
									continue
								if("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva ORG tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
									continue
								#Si se llegó a éste punto quiere decir que la directiva ORG no había sido usada con anterioridad y
								#su operando es un número válido
								banderaOrg = True
								direccionInicial = analisisCodop.valor					
								contLoc = analisisCodop.valor
								fileListado.write(contLoc,currentLine.etiqueta,"ORG",currentLine.operando,None,"DVA",None,None,None,None)
							else:
								errorTextBox += str(lineCount - 1) + ": El operando de la directiva ORG tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"

					#Escribir etiqueta en TABSIM, si es que existe
					if(currentLine.etiqueta != None):
						if(not banderaTabsimCreada):
							tabsim = Tabsim(nombreTabsim)
							banderaTabsimCreada = True
						if(not tabsim.write(currentLine.etiqueta, contLoc)):
							errorTextBox += str(lineCount - 1) + ": La etiqueta "+str(currentLine.etiqueta)+" ya fue usada\n"
							continue
					
					#Validar END
					if str(currentLine.codop).upper() == "END":
						if(currentLine.operando != None):
							errorTextBox += str(lineCount - 1) + ": La directiva END no puede tener operando\n"
							continue
						#if(banderaEnd):
							#errorTextBox += str(lineCount - 1) + ": La instrucción END puede existir una sola vez\n"
						if not banderaOrg:
							errorTextBox += str(lineCount - 1) + ": La directiva END no puede estar antes de ORG\n"
							continue
						banderaEnd = True
						fileListado.write(contLoc,currentLine.etiqueta,"END",currentLine.operando,None,"DVA",None,None,None,None)
						continue

					if str(currentLine.codop).upper() in directivas:
						if not banderaOrg:
							errorTextBox += str(lineCount - 1) + ": La directiva "+str(currentLine.codop)+" no puede estar antes de ORG\n"
						if currentLine.operando != None:
							analisisCodop = Automata(currentLine.operando.text)
							#DB, DC.B, FCB
							if str(currentLine.codop).upper() == "DB" or str(currentLine.codop).upper() == "DC.B" or str(currentLine.codop).upper() == "FCB":
								if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
									if("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
										errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
										continue
									if(analisisCodop.valor > 255):
										errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva "+str(currentLine.codop).upper()+" es de 0 a 255, el valor actual es "+str(analisisCodop.valor)+"\n"
									else:
										fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"DVA",None,None,None,None)
										contLoc+=1
								else:
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
								continue
							#DW, DC.W, FDB
							if str(currentLine.codop).upper() == "DW" or str(currentLine.codop).upper() == "DC.W" or str(currentLine.codop).upper() == "FDB":
								if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
									if("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
										errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
										continue
									if(analisisCodop.valor > 65535):
										errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva "+str(currentLine.codop).upper()+" es de 0 a 65535, el valor actual es "+str(analisisCodop.valor)+"\n"
									else:
										fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"DVA",None,None,None,None)
										contLoc+=2
								else:
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
								continue
							#FCC
							if str(currentLine.codop).upper() == "FCC":
								try:
									str(currentLine.operando).decode('ascii')
								except:
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser una cadena de caracteres ASCII\n"
									continue
								else:
									if str(currentLine.operando)[0]=="\"" and str(currentLine.operando)[-1]=="\"" and (len(str(currentLine.operando))>1):
										fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"DVA",None,None,None,None)
										contLoc += len(str(currentLine.operando))-2
									else:
										errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser una cadena de caracteres ASCII que comience y termine con \" (no puede terminar en espacios)\n"
									continue
							#DS, DS.B, RMB 
							if str(currentLine.codop).upper() == "DS" or str(currentLine.codop).upper() == "DS.B" or str(currentLine.codop).upper() == "RMB":
								if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
									if("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
										errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
										continue
									if(analisisCodop.valor > 65535):
										errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva "+str(currentLine.codop).upper()+" es de 0 a 65535, el valor actual es "+str(analisisCodop.valor)+"\n"
									else:
										fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"DVA",None,None,None,None)
										contLoc+=analisisCodop.valor
								else:
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
								continue
							#DS.W, RMW
							if str(currentLine.codop).upper() == "DS.W" or str(currentLine.codop).upper() == "RMW":
								if("Directo" in analisisCodop.modos or "Extendido" in analisisCodop.modos):
									if("REL" in analisisCodop.modos and "Extendido" in analisisCodop.modos):
										errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
										continue
									if(analisisCodop.valor > 65535):
										errorTextBox += str(lineCount - 1) + ": El rango de números válidos para la directiva "+str(currentLine.codop).upper()+" es de 0 a 65535, el valor actual es "+str(analisisCodop.valor)+"\n"
									else:
										fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"DVA",None,None,None,None)
										contLoc+=analisisCodop.valor*2
								else:
									errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser un número en cualquier representación válida (binario, octal, decimal o hexadecimal)\n"
								continue
						else:
							errorTextBox += str(lineCount - 1) + ": El operando de la directiva "+str(currentLine.codop).upper()+" tiene que ser diferente de NULL\n"
						continue
					"""
					FIN DIRECTIVAS
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
							infoInstr = self.tabop[currentLine.codop.text.upper()]
							if not banderaOrg:
								errorTextBox += str(lineCount - 1) + ": La directiva "+str(currentLine.codop)+" no puede estar antes de ORG\n"
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
								infoInstrModo = infoInstr['modos']['Inherente']
								fileListado.write(contLoc,currentLine.etiqueta,str(currentLine.codop).upper(),currentLine.operando,None,"Inherente",infoInstrModo['codMaq'],infoInstrModo['bCalculados'],infoInstrModo['bCalcular'],infoInstrModo['bTotal'])
								contLoc += infoInstrModo['bTotal']
								variablesTextBox += "  Operando: Inherente " + str(infoInstrModo['bTotal']) + " bytes\n\n"
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
									infoInstr = self.tabop[currentLine.codop.text.upper()]
									if modo in infoInstr['modos'] and not banderaModoEncontrado:
										banderaModoEncontrado = True
										infoInstrModo = infoInstr['modos']
										if modo == 'IDX':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['IDX']['bTotal']
											if analisisCodop.signo == None and analisisCodop.registroAc == None:
												variablesTextBox += "Indizado de 5 bits, (IDX), " + str(infoInstrModo['IDX']['bTotal']) + " bytes\n"
											elif analisisCodop.registroAc != None:
												variablesTextBox += "Indizado de acumulador, (IDX), " + str(infoInstrModo['IDX']['bTotal']) + " bytes\n"
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
												variablesTextBox+=", (IDX), de " + str(infoInstrModo['IDX']['bTotal']) + " bytes\n"
										elif modo == 'IDX1':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['IDX1']['bTotal']
											variablesTextBox += "Indizado de 9 bits, (IDX1), " + str(infoInstrModo['IDX1']['bTotal']) + " bytes\n"
										elif modo == 'IDX2':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['IDX2']['bTotal']
											variablesTextBox += "Indizado de 16 bits, (IDX2), " + str(infoInstrModo['IDX2']['bTotal']) + " bytes\n"
										elif modo == '[IDX2]':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['[IDX2]']['bTotal']
											variablesTextBox += "Indizado indirecto de 16 bits, (IDX1), " + str(infoInstrModo['[IDX2]']['bTotal']) + " bytes\n"
										elif modo == '[D,IDX]':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['[D,IDX]']['bTotal']
											variablesTextBox += "Indizado indirecto de acumulador, ([D,IDX]), " + str(infoInstrModo['[D,IDX]']['bTotal']) + " bytes\n"
										elif modo == 'REL':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['REL']['bTotal']
											variablesTextBox += "Relativo de "+str(4*infoInstrModo['REL']['bTotal'])+" bits, "+ str(infoInstrModo['REL']['bTotal']) + " bytes\n"
										elif modo == 'Extendido':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['Extendido']['bTotal']
											variablesTextBox+="Extendido, de "+str(infoInstrModo['Extendido']['bTotal']) + " bytes\n"
										elif modo == 'Directo':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['Directo']['bTotal']
											variablesTextBox+="Directo, de "+str(infoInstrModo['Directo']['bTotal']) + " bytes\n"
										elif modo == 'Inmediato':
											fileListado.write(contLoc,currentLine.etiqueta,currentLine.codop,currentLine.operando,analisisCodop.valor,modo,infoInstrModo[modo]['codMaq'],infoInstrModo[modo]['bCalculados'],infoInstrModo[modo]['bCalcular'],infoInstrModo[modo]['bTotal'])
											contLoc += infoInstrModo['Inmediato']['bTotal']
											variablesTextBox+="Inmediato de "+str(8*infoInstrModo['Inmediato']['bCalcular'])+" bits, "+str(infoInstrModo['Inmediato']['bTotal']) + " bytes\n"
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
			fileListado.close()
			if(banderaTabsimCreada):
				tabsim.close()

			fileListado = Listado(nombreListado,"r")
			for line in fileListado.lines():
				currentLine = fileListado.read(line)
				analisisCodop = Automata(currentLine['operando'])
				codMaqGenerado+=str(currentLine['contLoc'])+" "+str(currentLine['etiqueta']).rjust(9)+" "+str(currentLine['codop']).rjust(5)+" "+str(currentLine['operando']).rjust(9)+"\t"
				if(currentLine['modo']=="Inherente"):
					codMaqGenerado+=str(currentLine['codMaq'])
				elif(currentLine['modo']=="Directo"):
					codMaqGenerado+=str(currentLine['codMaq'])+currentLine['valorHex'].rjust(2,"0").upper()
				elif(currentLine['modo']=="Extendido"):
					if analisisCodop.etiqueta!=None:
						#Implementar la búsqueda en la tabla de símbolos :)
						codMaqGenerado+=""
					else:
						codMaqGenerado+=str(currentLine['codMaq'])+currentLine['valorHex'].rjust(4,"0").upper()
				elif(currentLine['modo']=="Inmediato"):
					if(currentLine['bCalcular']=='1'):
						codMaqGenerado+=str(currentLine['codMaq'])+currentLine['valorHex'].rjust(2,"0").upper()
					elif(currentLine['bCalcular']=='2'):
						codMaqGenerado+=str(currentLine['codMaq'])+currentLine['valorHex'].rjust(4,"0").upper()
				elif(currentLine['modo']=="IDX"):
					if analisisCodop.pre==None and analisisCodop.registroAc==None and analisisCodop.etiqueta==None:
						codMaqGenerado+=str(currentLine['codMaq']+Util.xb5(analisisCodop.valor,analisisCodop.registro).upper())
					elif analisisCodop.pre!=None and analisisCodop.etiqueta==None:
						codMaqGenerado+=str(currentLine['codMaq']+Util.xbppid(analisisCodop.valor,analisisCodop.registro,analisisCodop.signo,analisisCodop.pre).upper())
					else:
						codMaqGenerado+=str(currentLine['codMaq']+Util.xbac(analisisCodop.registro,analisisCodop.registroAc).upper())
				elif(currentLine['modo']=="IDX1"):
					codMaqGenerado+=str(currentLine['codMaq']+Util.idx1(analisisCodop.valor,analisisCodop.registro).upper())
				elif(currentLine['modo']=="IDX2"):
					codMaqGenerado+=str(currentLine['codMaq']+Util.idx2(analisisCodop.valor,analisisCodop.registro).upper())
				elif(currentLine['modo']=="[IDX2]"):
					codMaqGenerado+=str(currentLine['codMaq']+Util.idx2cplx(analisisCodop.valor,analisisCodop.registro).upper())
				elif(currentLine['modo']=="[D,IDX]"):
					codMaqGenerado+=str(currentLine['codMaq']+Util.xbd(analisisCodop.registro).upper())
				else:
					codMaqGenerado+="No encontrado"
				codMaqGenerado+="\n"
			errorTextBox += "Longitud del código (en bytes): "+str(contLoc - direccionInicial)+"\n"
			return archivoCorto, fileTextBox, variablesTextBox, errorTextBox, codMaqGenerado
		else:
			return None

#TODO
#	-Búsqueda en la tabla de símbolos
#	-Relativos