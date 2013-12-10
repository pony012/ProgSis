#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


def comp2(n,b): #retorna el complemento a 2 de n a b bits, en formato binario (0bB[B[...]])
	#n tiene que ser positivo
	if n<0:
		return None
	return  bin((n^((1<<b)-1))+1)[2:].rjust(b,"0")[-b:]


_xbrr={"X":0,"Y":1,"SP":2,"PC":3}
_xbaa={"A":0,"B":1,"D":2}

def xb5(n,r):
	r=r.upper()
	if r in _xbrr:
		xb=0
		xb|=_xbrr[r]<<6
		if n>=0:
			xb|=n
		else:
			xb|=int(comp2(-n,5),2)
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def xb9(n,r):
	r=r.upper()
	if r in _xbrr:
		xb=0
		xb|=0xe0
		xb|=_xbrr[r]<<3
		if n<0:
			xb|=1
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def idx1(n,r):
	r=r.upper()
	if r in _xbrr:
		if n>=0:
			return xb9(n,r)+hex(n)[2:].rjust(2,"0")
		else:
			return xb9(n,r)+hex(int(comp2(-n,8),2))[2:].rjust(2,"0")
	else:
		return None

def xb16(r):
	r=r.upper()
	if r in _xbrr:
		xb=0
		xb|=0xe2
		xb|=_xbrr[r]<<3
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def idx2(n,r):
	r=r.upper()
	if r in _xbrr:
		return xb16(r)+hex(n)[2:].rjust(4,"0")
	else:
		return None

def xbppid(n,r,s,p):#n=valor, r=registro, s=signo, p=Pre(True)/Post(False)
	r=r.upper()
	if r != "PC" and r in _xbrr:
		xb=0
		xb|=_xbrr[r]<<6
		xb|=0x20
		if not p:
			xb|=1<<4
		if s=="+":
			xb|=(n-1)
		else:
			xb|=0x10-n
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def xb16cplx(r):
	r=r.upper()
	if r in _xbrr:
		xb=0
		xb|=0xe3
		xb|=_xbrr[r]<<3
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def idx2cplx(n,r):
	r=r.upper()
	if r in _xbrr:
		return xb16cplx(r)+hex(n)[2:].rjust(4,"0")
	else:
		return None

def xbd(r):
	r=r.upper()
	if r in _xbrr:
		xb=0
		xb|=0xe7
		xb|=_xbrr[r]<<3
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def xbac(r,a):
	r=r.upper()
	a=a.upper()
	if r in _xbrr and a in _xbaa:
		xb=0
		xb|=0xe4
		xb|=_xbrr[r]<<3
		xb|=_xbaa[a]
		return hex(xb)[2:].rjust(2,"0")
	else:
		return None

def checkSum(s):
	#La Linea
	#Obtiene el valor hexadecimal del complemento a 1 de la suma de los pares 
	#hexadecimales (bytes) de la cadena s y lo limita a 1 byte
	return hex(sum([int(s[i:i+2],16) for i in range(0,len(s),2)])^0xff)[2:][-2:].rjust(2,"0").upper()