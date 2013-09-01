#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Automata:
	'''
		Genera un autómata de estados finitos
	'''
	def __init__(self, ini, table, final):
		'''
			@param ini int: Estado inicial del autómata
			@param table list(dictionary): Tabla de transiciones con la forma [{"regla",estado},{"regla",estado}]
			@param final list(int): Estados de aceptación
			@return None
		'''
		self.estadoInicial = ini
		self.tabla = table
		self.final = final
	def evaluar(self, cadena):
		'''
			Evalúa una cadena con el autómata que tenga cargado
			@param cadena string: Cadena a evaluar
			@return Retorna 1 si pasó el test, 
			TODO Códigos de error
		'''
		estadoActual = self.estadoInicial
		for caracter in cadena:
			#codigo = 
			if self.table[estadoActual].has_key(caracter):
				estadoActual = self.table[estadoActual].has_key(caracter)
			else: #Estado de error
				pass
