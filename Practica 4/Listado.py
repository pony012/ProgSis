class Listado:
	def __init__(self, fileName):
		self.fileListado = open(fileName,"w")
	def write(self, contLoc, etiqueta, codop, operando):
		self.fileListado.write(hex(contLoc)[2:].rjust(4,"0").upper())
		self.fileListado.write("\t")
		if(etiqueta == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(etiqueta))
		self.fileListado.write("\t")
		self.fileListado.write(str(codop).upper())
		self.fileListado.write("\t")
		if(operando == None):
			self.fileListado.write("NULL")
		else:
			self.fileListado.write(str(operando))
		self.fileListado.write("\n")
	def close(self):
		self.fileListado.close()
		