class Tabsim:
	def __init__(self, fileName):
		self.fileTabsim = open(fileName,"w")
		self.etiquetasTabsim = {}
	def write(self, etiqueta, contLoc):
		if(etiqueta != None):
			if(not (str(etiqueta) in self.etiquetasTabsim)):
				self.etiquetasTabsim[str(etiqueta)] = hex(contLoc)[2:].rjust(4,"0").upper()
				self.fileTabsim.write(str(etiqueta))
				self.fileTabsim.write("\t")
				self.fileTabsim.write(hex(contLoc)[2:].rjust(4,"0").upper())
				self.fileTabsim.write("\n")
				return True
			else:
				return False
	def close(self):
		self.fileTabsim.close()
		