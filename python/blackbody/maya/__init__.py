import sys
import os
import os.path
import re
from blackbody.maya import ui

def __normpath(path):
	return re.sub(r'\\', '/', path)

def __get_modules(filepath):
	path, file = os.path.split(__normpath(filepath))
	mdict = {}
	for mname, mod in sys.modules.items():
		if '__file__' not in dir(mod):
			continue
		if re.match('%s.*' % path, __normpath(mod.__file__)):
			mdict[mname] = mod
	return mdict

def reload_modules():
	mfiles = __get_modules(__file__)
	for mname, mod in mfiles.items():
		if os.path.isfile(mod.__file__):
			reload(mod)
			print('>> Reload: [%s] %s' % (mname, mod.__file__))
		else:
			print('# File not found: %s' % mod.__file__)
	print('- Finish all reloading')

def __set_argv():
	argv = {}
	argv['name'] = 'blackbody'
	argv['title'] = 'Black Body'
	argv['version'] = '0.2'
	argv['latestUpdate'] = 'Oct 7, 2012'
	argv['author'] = 'Tai Komatsu'
	argv['license'] = '(C) Copyright 2011 Tai Komatsu All Rights Reserved.'
	argv['description'] = 'To make blackbody radiation based color ramps.'
	return argv

def main(dev=False):
	if dev:
		reload_modules()
	argv = __set_argv()
	ui.open(argv)

