from distutils.core import setup
import py2exe

target = {
	'script' : "gui.py",
	'version' : "1.0",
	'company_name' : "Universidad de Guadalajara",
	'copyright' : "PonySoft",
	'name' : "Ensamblador", 
	'dest_base' : "", 
	'icon_resources': [(1, "favicon.ico")]
}

setup(
	windows=[{
		"script":'gui.py',
		"icon_resources": [(1, "favicon.ico")]
	}],
	data_files=['C:\Python27\\tcl\\tcl8.5\\init.tcl','C:\Python27\\tcl\\tk8.5\\tk.tcl']
)

#python setup.py install
#python setup.py py2exe

#install shield