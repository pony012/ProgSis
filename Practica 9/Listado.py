#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Alan Andrés Sánchez Castro

class Listado:
	def __init__(self, fileName, mode):
		self.fileListado = open(fileName,str(mode))
		self.delimiter = chr(31) #▼ (Unit separator) [ASCII Contro Character]
	def write(self, contLoc, etiqueta, codop, operando, valorDec, modo, codMaq, bCalculados, bCalcular, bTotal):
		#contLoc
		self.fileListado.write(hex(contLoc)[2:].rjust(4,"0").upper())
		self.fileListado.write(self.delimiter)
		#etiqueta
		if(etiqueta == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(etiqueta))
		self.fileListado.write(self.delimiter)
		#codop
		self.fileListado.write(str(codop).upper())
		self.fileListado.write(self.delimiter)
		#operando
		if(operando == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(operando))
		self.fileListado.write(self.delimiter)
		#valorDec
		if(valorDec == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(hex(valorDec)[2:])
		self.fileListado.write(self.delimiter)
		#modo
		if(modo == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(modo))
		self.fileListado.write(self.delimiter)
		#codMaq
		if(codMaq == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(codMaq))
		self.fileListado.write(self.delimiter)
		#bCalculados
		if(bCalculados == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(bCalculados))
		self.fileListado.write(self.delimiter)
		#bCalcular
		if(bCalcular == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(bCalcular))
		self.fileListado.write(self.delimiter)
		#bTotal
		if(bTotal == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(bTotal))
		self.fileListado.write("\n")
	def close(self):
		self.fileListado.close()
	def lines(self):
		return self.fileListado.read().split('\n')[0:-1]
	def read(self, line):
		split = line.split(self.delimiter)
		listDict = {
				'contLoc':str(split[0]),
				'etiqueta':str(split[1]),
				'codop':str(split[2]),
				'operando':str(split[3]),
				'valorHex':str(split[4]),
				'modo':str(split[5]),
				'codMaq':str(split[6]),
				'bCalculados':str(split[7]),
				'bCalcular':str(split[8]),
				'bTotal':str(split[9])
			}
		return listDict