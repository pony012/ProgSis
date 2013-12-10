#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Etiqueta:
	'''
		Define una etiqueta 
	'''
	def __init__(self, text, errorList):
		self.text = text
		self.errorList = errorList
		self.errores = []
		self.validar()
	def __str__(self):
		return self.text
	def validar(self):
		tam = len(self.text)
		if tam > 0:
			if (not self.text[0].islower()) and (not self.text[0].isupper()):
				self.errores.append("La Etiqueta debe iniciar con letra mayúscula o minúscula")
				self.errores.append("La Etiqueta no puede contener '"+ self.text[0] +"', sólo puede incluir letras (mayúsculas/minúsculas), números (0 .. 9) y _")
		if tam > 1:
			for caracter in self.text[1:]:
				if (not caracter.islower()) and (not caracter.isupper()) and (not caracter.isdigit()) and caracter != '_':
					self.errores.append("La Etiqueta no puede contener '"+ caracter +"', sólo puede incluir letras (mayúsculas/minúsculas), números (0 .. 9) y _")
		if tam > 8:
			self.errores.append("La Etiqueta puede contener máximo 5 caracteres")
		self.errorList.extend(self.errores)
	def getErrores(self):
		return self.errores