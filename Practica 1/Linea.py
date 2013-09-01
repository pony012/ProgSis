#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Etiqueta import *
from Codop import *
from Operando import *

class Linea:
	'''
		Evalúa una línea y guarda sus variables individualmente
	'''
	def __init__(self, text):
		self.text = text
		self.etiqueta = None
		self.codop = None
		self.operando = None
		self.comentario = False
		self.errores = []
		if len(self.text) == 0: #salto de línea símple
			pass
		elif self.text[0] == ';' : #comentario
			self.comentario = True
		else: #Tratar la cadena
			self._text = text.replace("\t"," ")	#convierto los tabuladores a espacios para poder partir la cadena
			self.bloques = self._text.split()	#parte la cadena cada que encuentra espacios en blanco
			if self._text[0] == ' ':	#la línea no empieza con una letra, por lo tanto no tiene etiqueta
				if len(self.bloques) >= 1:	#primer bloque, por lo tanto es codop
					self.codop = Codop(self.bloques[0],self.errores)
				if len(self.bloques) >= 2:	#tiene dos o más bloques, por lo tanto el primero es codop y los demás son el operando
					_cadAux = self.text.replace(self.bloques[0],"",1) #se saca el texto del texto original (incluye '\t')
					self.operando = Operando(_cadAux[_cadAux.find(self.bloques[1]):],self.errores)
			else:
				if len(self.bloques) >= 1:	#primer bloque, por lo tanto es etiqueta
					self.etiqueta = Etiqueta(self.bloques[0],self.errores)
				if len(self.bloques) >= 2:	#segundo bloque, por lo tanto el primero es etiqueta y el segundo es codop
					self.codop = Codop(self.bloques[1],self.errores)
				if len(self.bloques) >= 3:	#tiene tres o más bloques, por lo tanto el primero es etiqueta, el segundo es codop y los demás son el operando
					_cadAux = self.text.replace(self.bloques[0],"",1).replace(self.bloques[1],"",1) #se saca el texto del texto original (incluye '\t')
					self.operando = Operando(_cadAux[_cadAux.find(self.bloques[2]):],self.errores)
			if self._text[-1:] == " ":
				print "error"
				if not self.etiqueta is None and not self.codop is None and self.operando is None:
					self.errores.append("Después del operando sólo puede haber retorno de carro")
				elif not self.etiqueta is None and not self.codop is None:
					self.errores.append("Después del código de opreación sólo puede haber retorno de carro")
				elif not self.codop is None and not self.operando is None:
					self.errores.append("Después del operando sólo puede haber retorno de carro")
				elif not self.codop is None:
					self.errores.append("Después del código de opreación sólo puede haber retorno de carro")
		if self.codop is None:
			self.errores.append("La línea no contiene un código de operación")

	def atributos(self):
		text = "Etiqueta = "
		if self.etiqueta is not None:
			text += str(self.etiqueta) + "\n"
			"""
			for error in self.etiqueta.getErrores():
				text+=" "+error+"\n"
			"""
		else:
			text += "NULL\n"
		text +="Codop = "
		if self.codop is not None:
			text += str(self.codop) + "\n"
			"""
			for error in self.codop.getErrores():
				text+=" "+error+"\n"
			"""
		else:
			text += "NULL\n"
		text += "Operando = "
		if self.operando is not None:
			text += str(self.operando) + "\n"
			"""
			for error in self.operando.getErrores():
				text+=" "+error+"\n"
			"""
		else:
			text += "NULL\n"
		"""
		if self.codop is None:
			text += " La línea no contiene un código de operación\n"
		"""
		return text

	def getErrores(self):
		return self.errores