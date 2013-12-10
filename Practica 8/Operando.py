#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Operando:
	'''
		Define un Operando 
	'''
	def __init__(self, text, errorList):
		self.text = text
		self.errorList = errorList
		self.errores = []
		self.validar()
	def __str__(self):
		return self.text
	def validar(self):
		pass
	def getErrores(self):
		return self.errores