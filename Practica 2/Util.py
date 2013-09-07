def existeArchivo( archivo ):
	if not(stringIsNullOrEmpty(archivo)):
		try:
			f = open( archivo , "r" )
			f.close()
			return True
		except IOError:
			return False
	else:
		return False
def stringIsNullOrEmpty( st ):
	return not(st is not None and len( st ) > 0)