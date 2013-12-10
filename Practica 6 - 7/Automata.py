#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Automata:
	def __init__(self, s = None):
		W = 48
		E = 20
		self.W = W
		self.E = E

		self.modos = []
		self.valor = None
		self.etiqueta = None
		self.registro = None
		self.signo = None
		self.pre = None #True para pre, False para post
		self.registroAc = None
		self.errores = []
		self.bits = None
		self.tabla = [
						[1 ,9 ,11,13,15,15,15,15,W,16, W, W, W, W, 20,W, 22,W ,33,33,W],
						[45, 2, 4, 6, 8, 8, 8, 8,45,45,45,45,45,45,45,45,45,45,45,45,45],
						[40,40,40,40, 3, 3, 3, 3, 3,40,40,40,40, 3,40,40,40,40, 3, 3,40],
						[40,40,40,40, 3, 3, 3, 3, 3,40,40,40,40, 3,40,40,40,40, 3, 3,40],
						[41,41,41,41, 5, 5, 5,41,41,41,41,41,41,41,41,41,41,41,41,41,41],
						[41,41,41,41, 5, 5, 5,41,41,41,41,41,41,41,41,41,41,41,41,41,41],
						[42,42,42,42, 7, 7,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42],
						[42,42,42,42, 7, 7,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42],
						[39,39,39,39, 8, 8, 8, 8,39,39,39,39,39,39,39,39,39,39,39,39,39],
						[40,40,40,40,10,10,10,10,10,40,40,40,40,10,40,40,40,40,10,10,40],
						[40,40,40,40,10,10,10,10,10,40,40,40,40,10,40,40,40,40,10,10,40],
						[41,41,41,41,12,12,12,41,41,41,41,41,41,41,41,41,41,41,41,41,41],
						[41,41,41,41,12,12,12,41,41,41,41,41,41,41,41,41,41,41,41,41,41],
						[42,42,42,42,14,14,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42],
						[42,42,42,42,14,14,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42],
						[39,39,39,39,15,15,15,15,39,16,39,39,39,39,39,39,39,39,39,39,39],
						[44,44,44,44,44,44,44,44,44,44,17,18,19,44,29,29,44,44,44,44,44],
						[44,44,44,44,44,44,44,44,44,44,44,44,44,44,31,31,44,44,44,44,44],
						[44,44,44,44,44,44,44,44,44,44,44,44,17,44,46,46,44,44,44,44,44],
						[44,44,44,44,44,44,44,44,44,44,44,44,44,32,46,46,44,44,44,44,44],
						[W, W, W, W, W,21,21,21, W, W, W, W, W, W, W, W, W, W, W, W, W],
						[39,39,39,39,21,21,21,21,39,16,39,39,39,39,39,39,39,39,39,39,39],
						[47,47,47,47,23,23,23,23,47,47,47,47,47,47,47,47,47,47,47,38,47],
						[39,39,39,39,23,23,23,23,39,24,39,39,39,39,39,39,39,39,39,39,39],
						[47,47,47,47,47,47,47,47,47,47,27,25,26,47,47,47,47,47,47,47,47],
						[47,47,47,47,47,47,47,47,47,47,47,47,27,47,47,47,47,47,47,47,47],
						[47,47,47,47,47,47,47,47,47,47,47,47,47,27,47,47,47,47,47,47,47],
						[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,28,47,47,47],
						[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47],
						[46,46,46,46,46,46,46,46,46,46,31,30,46,46,46,46,46,46,46,46,46],
						[46,46,46,46,46,46,46,46,46,46,46,46,31,46,46,46,46,46,46,46,46],
						[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46],
						[44,44,44,44,44,44,44,44,44,44,44,44,44,44,46,46,44,44,44,44,44],
						[W, W, W, W, W, W, W, W, W,34, W, W, W, W, W, W, W, W, W, W, W],
						[43,43,43,43,43,43,43,43,43,43,37,35,36,43,43,43,43,43,43,43,43],
						[43,43,43,43,43,43,43,43,43,43,43,43,37,43,43,43,43,43,43,43,43],
						[43,43,43,43,43,43,43,43,43,43,43,43,43,37,43,43,43,43,43,43,43],
						[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43],
						[47,47,47,47,47,47,47,47,47,24,47,47,47,47,47,47,47,47,47,47,47], 
						[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39],
						[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40],
						[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41],
						[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42],
						[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43],
						[44,44,44,44,44,44,44,44,44,44,44,44,44,44,46,46,44,44,44,44,44],
						[45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45,45],
						[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46],
						[47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47,47],
						[W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]
						]
		if s != None:
			self.analizar(s)

	def evaluarC(self, c):
		c=c.upper()
		if c=='#':
			return 0
		if c=='$':
			return 1
		if c=='@':
			return 2
		if c=='%':
			return 3
		if c=='0':
			return 4
		if c=='1':
			return 5
		if c>='2' and c <='7':
			return 6
		if c=='8' or c =='9':
			return 7
		if c =='E' or c=='F':
			return 8
		if c==',':
			return 9
		if c=='X' or c=='Y':
			return 10
		if c=='S':
			return 11
		if c=='P':
			return 12
		if c=='C':
			return 13
		if c=='-':
			return 14
		if c=='+':
			return 15
		if c=='[':
			return 16
		if c==']':
			return 17
		if c=='A' or c=='B':
			return 18
		if c=='D':
			return 19
		return self.E

	def analizar(self, s):
		self.modos = []
		self.valor = None
		self.etiqueta = None
		self.registro = None
		self.signo = None
		self.pre = None #True para pre, False para post
		self.registroAc = None
		self.errores = []
		self.bits = None

		estado = 0

		if len(s)==0:
			self.modos.append("Inherente")
			return self
		for c in s:
			#print "Estado Actual = " + str(estado) + " Val = " +str(self.evaluarC(c))+ " C = " +c+ " Estado siguiente = " + str(self.tabla[estado][self.evaluarC(c)])
			estado = self.tabla[estado][self.evaluarC(c)]

		#Inmediatos
		if estado == 3 or estado == 5 or estado == 7 or estado == 8:
			if estado == 3:
				self.valor = int(s[2:],16)
				self.modos.append("Inmediato")
			if estado == 5:
				self.valor = int(s[2:],8)
				self.modos.append("Inmediato")
			if estado == 7:
				self.valor = int(s[2:],2)
				self.modos.append("Inmediato")
			if estado == 8:
				self.valor = int(s[1:])
				self.modos.append("Inmediato")

			if self.valor >=0 and self.valor <= 65535:
				self.bits = 16
			elif self.valor >=0 and self.valor <=255:
				self.bits = 8
			else:
				self.errores.append("Error en modo inmediato, fuera de rango. El rango aceptado para 1 byte es de 0 a 255, para 2 bytes es de 0 a 65535 (El valor actual es: " + str(self.valor) +")")
			return self

		#Directo, extendido
		if estado == 10 or estado == 12 or estado == 14 or estado == 15:
			if estado == 10:
				self.valor = int(s[1:],16)
			if estado == 12:
				self.valor = int(s[1:],8)
			if estado == 14:
				self.valor = int(s[1:],2)
			if estado == 15:
				self.valor = int(s)
				
			if self.valor >=0 and self.valor <=255:
				self.modos.append("Directo")
			elif self.valor >=256 and self.valor <= 65535:
				self.modos.append("Extendido")
			else:
				self.modos.append("Directo")
				self.modos.append("Extendido")
				self.errores.append("Los rangos válidos para los modos Directo y Extendido son, respectivamente: 0 a 255 y 256 a 65535 (El valor actual es: " + str(self.valor) +")")
			return self

		#Indizados
		if estado == 17 or estado == 32:
			self.registro = s[s.find(',')+1:]
			if s.find(',')!=0:
				self.valor = int(s[0:s.find(',')])
				if self.valor >= -16 and self.valor <=15:
					self.modos.append("IDX")
				elif (self.valor >= -256 and self.valor <= -17) or (self.valor >= 16 and self.valor <= 255):
					self.modos.append("IDX1")
				elif self.valor >= 256 and self.valor <= 65535:
					self.modos.append("IDX2")
				else:
					self.modos.append("IDX")
					self.modos.append("IDX1")
					self.modos.append("IDX2")
					self.errores.append("Los rangos válidos para los modos IDX, IDX1 e IDX2 son: IDX -16 a 15, IDX1 -256 a -17 y 16 a 255, IDX2 256 a 65535 (El valor actual es: " + str(self.valor) +")")
			else:
				self.valor = 0
				self.modos.append("IDX")
			return self

		#Indizado indirecto/Indizado de ac. indirecto ??
		if estado == 28:
			self.registro = s[s.find(',')+1:s.find(']')]
			if s[1].upper()=='D':
				self.registroAc = s[1]
				self.modos.append("[D,IDX]")
			else:
				self.valor = int(s[1:s.find(',')])
				self.modos.append("[IDX2]")
				if self.valor < 0 or self.valor > 65535:
					self.errores.append("El rango válido para [IDX2] es de 0 a 65535 (El valor actual es: " + str(self.valor) +")")
			return self

		#Indizado pre/post incremento/decremento
		if estado == 31:
			self.valor = int(s[0:s.find(',')])
			self.modos.append("IDX")
			if s.find(',')==1:
				if self.valor > 0 and self.valor < 9:
					if s[s.find(',')+1] == '+':
						self.signo = '+'
						self.pre = True
						self.registro = s[s.find(',')+2:]
					elif s[s.find(',')+1] == '-':
						self.signo = '-'
						self.pre = True
						self.registro = s[s.find(',')+2:]
					elif s[-1] == "+":
						self.signo = '+'
						self.pre = False
						self.registro = s[s.find(',')+1:-1]
					elif s[-1] == "-":
						self.signo = '-'
						self.pre = False
						self.registro = s[s.find(',')+1:-1]
				else:
					self.errores.append("El rango válido para el modo indizado de acumulador es de 1 a 8")	
			else:
				self.errores.append("Los caracteres de inicio válidos para el modo indizado de acumulador son: 1..8, después tiene que existir una coma y posteriormente un registro válido (x, y, sp) con pre/post incremento/decremento")
			return self

		#Indizado de acumulador
		if estado ==37:
			self.registroAc = s[0]
			self.registro = s[s.find(',')+1:]
			self.modos.append("IDX")
			return self

		#Etiqueta (Relativo, Extendido)
		tam = len(s)
		band = True
		if tam > 0:
			if (s[0].islower() or s[0].isupper()):
				for c in s[1:]:
					if (not c.islower()) and (not c.isupper()) and (not c.isdigit()) and c != '_':
						band = False
				if band and tam <= 8:
					self.etiqueta = s
					self.modos.append("REL")
					self.modos.append("Extendido")
				else:
					self.errores.append("Los caractéres válidos para una etiqueta son a..z, A..Z, 0..9, _, además tiene que comenzar con letra, y la longitud máxima de una etiqueta son 8 caracteres")
				return self

		#ERRORES
		if estado == 1 or estado == 45:
			self.errores.append("Después del # debes especificar un número válido positivo en cualquiera de las cuatro bases válidas (dec, oct, bin, hex)")
			return self
		if estado == 2 or estado == 9 or estado == 40:
			self.errores.append("Después del $ debes especificar un número válido positivo para la base hexadecimal, los caracteres válidos son: 0..9,a..f,A..F")
			return self
		if estado == 4 or estado == 11 or estado == 41:
			self.errores.append("Después del @ debes especificar un número válido positivo para la base octal, los caracteres válidos son: 0..7")
			return self
		if estado == 6 or estado == 13 or estado == 42:
			self.errores.append("Después del % debes especificar un número válido positivo para la base binaria, los caracteres válidos son: 0 o 1")
			return self
		if estado == 39:
			self.errores.append("Los enteros válidos (base decimal) sólo aceptan 0..9 como caracteres válidos")
			return self
		if estado == 21:
			self.errores.append("Los únicos negativos válidos (en base decimal) son para IDX e IDX1, y después del número tiene que existir una ,")
			return self
		if estado == 34 or estado == 35 or estado == 36 or estado == 43:
			self.errores.append("Los registros del modo indi acumulador válidos son x, y, pc o sp")
			return self
		if estado == 20:
			self.errores.append("Después del - tiene que haber un número en base decimal válido")
			return self
		if estado == 16:
			self.errores.append("Después de la , tiene que existir un registro válido (x, y, pc, sp) o bien un pre/post incremento/decremento de (x, y, sp)")
			return self
		if estado == 18 or estado == 19 or estado == 44:
			self.errores.append("Los registros válidos para los modos indizados son (x, y, pc, sp)")
			return self
		if estado == 29 or estado == 30 or estado == 46:
			self.errores.append("Las formas válidas para los registros pre/post incremento/decremento son [+|-]x, [+|-]y, [+|-]sp, x[+|-], y[+|-], sp[+|-]")
			return self
		if estado == 22:
			self.errores.append("Después del [ tiene que ir un número decimal válido (0-65535) o el registro d")
			return self
		if estado == 23 or estado == 38 or estado == 24 or estado == 25 or estado == 26 or estado == 27 or estado == 47:
			self.errores.append("Después del número o el registro d, tiene que ir una coma, seguido por un registro válido (x, y, pc, sp) y el corchete de cierre (])")
			return self
		self.errores.append("No cumple con las reglas de escritura de una etiqueta (comenzar con letra, seguido de letras, 0..9 o _ y una longitud máxima de 8 caracteres)")
		return self

	def __str__(self):
		return str(self.modos)+","+ str(self.valor)+","+str(self.etiqueta)+","+str(self.registro)+","+str(self.signo)+","+str(self.pre)+","+str(self.registroAc)+","+str(self.bits)+","+str(self.errores)