#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Codop:
	'''
		Define un Codop 
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
		banderaPunto = False
		banderaErrorPunto = False
		if tam > 0:
			if (not self.text[0].islower()) and (not self.text[0].isupper()):
				self.errores.append("El código de operación debe iniciar con letra mayúscula o minúscula")
				if self.text[0] == '.':
					banderaPunto = True
			if (not self.text[0].islower()) and (not self.text[0].isupper()) and self.text[0] != '.':
					self.errores.append("El código de operación no puede contener '"+ self.text[0] +"', sólo puede incluir letras (mayúsculas/minúsculas) y .")
		if tam > 1:
			for caracter in self.text[1:]:
				if (not caracter.islower()) and (not caracter.isupper()) and caracter != '.':
					self.errores.append("El código de operación no puede contener '"+ caracter +"', sólo puede incluir letras (mayúsculas/minúsculas) y .")
				elif (caracter == '.'):
					if banderaPunto:
						if not banderaErrorPunto:
							self.errores.append("El código de operación sólo puede incluir el caracter '.' una sola vez")
							banderaErrorPunto = True
					else:
						banderaPunto = True
		if tam > 5:
			self.errores.append("El código de operación puede contener máximo 5 caracteres")
		self.errorList.extend(self.errores)
	def getErrores(self):
		return self.errores